import os
import subprocess
import socket
import time
import yaml

from scripts.config import load_config


def launch_runtime(challenge):
    runtime = challenge.get("runtime")
    config = load_config()
    boxes_dir = os.path.join(os.path.dirname(__file__), "..", config["boxes_dir"])

    if runtime == "file":
        return launch_file(challenge, config)
    
    elif runtime == "docker":
        return launch_docker(challenge, boxes_dir, config)
    
    elif runtime == "netcat":
        return launch_netcat(challenge, boxes_dir, config)

    else:
        print(f"Unknown runtime: {runtime}")
        return {}
    

def get_host_ip(config):
    host_ip = config.get("host_ip", "auto")
    if host_ip == "auto":
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
    return host_ip


def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def wait_for_port(host, port, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (ConnectionRefusedError, OSError):
            time.sleep(0.5)
    return False


def write_override(compose_dir, service, host_port, container_port):
    override = {"services": {service: {"ports": [f"{host_port}:{container_port}"]}}}
    override_path = os.path.join(compose_dir, "docker-compose.override.yml")
    with open(override_path, "w") as f:
        yaml.dump(override, f, default_flow_style=False)


def get_container_port(compose_dir, service):
    compose_path = os.path.join(compose_dir, "docker-compose.yml")
    try:
        with open(compose_path) as f:
            data = yaml.safe_load(f)
        ports = data.get("services", {}).get(service, {}).get("ports", [])
        for p in ports:
            parts = str(p).split(":")
            return int(parts[-1])
    except Exception:
        pass
    return None
    

def launch_file(challenge, config):
    import shutil
    challenges_dir = os.path.join(os.path.dirname(__file__), "..", config["challenges_dir"])
    category = challenge.get("category", "misc")
    name = challenge.get("name", "")
    file_field = challenge.get("file", "")
    files = file_field if isinstance(file_field, list) else [file_field]

    workspace = os.path.expanduser(config.get("workspace_dir", "~/dlnlab/workspace"))
    os.makedirs(workspace, exist_ok=True)

    copied = []
    for filename in files:
        src = os.path.join(challenges_dir, category, name, filename)
        dst = os.path.join(workspace, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied.append(dst)
        else:
            print(f"    Warning: file not found: {src}")
        
    return {"workspace": workspace, "files": copied}


def launch_docker(challenge, boxes_dir, config):
    compose_dir = os.path.join(boxes_dir, challenge["name"])
    port = challenge.get("port", 8080)
    service = challenge.get("service")

    free_port = get_free_port() if service else port
    if service:
        container_port = get_container_port(compose_dir, service) or port
        write_override(compose_dir, service, free_port, container_port)

    print(f"\n  Starting Docker environment...")
    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=compose_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"    Error: {result.stderr}")
        return {}
    
    if wait_for_port("127.0.0.1", free_port):
        print(f"    Docker Started.")
    else:
        print(f"    Warning: service not reachable on port {free_port}.")
    return {"target": f"http://{get_host_ip(config)}:{free_port}", "port": free_port} 


def launch_netcat(challenge, boxes_dir, config):
    compose_dir = os.path.join(boxes_dir, challenge["name"])
    host = challenge.get("host", "127.0.0.1")
    port = challenge.get("port", 4444)
    service = challenge.get("service")
    free_port = get_free_port() if service else port
    if service:
        container_port = get_container_port(compose_dir, service) or port
        write_override(compose_dir, service, free_port, container_port)

    print(f"\n  Starting netcat environment...")
    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=compose_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"    Error: {result.stderr}")
        return {}
    
    if wait_for_port("127.0.0.1", free_port):
        print(f"    Netcat Started.")
    else:
        print(f"    Warning: service not reachable on port {free_port}.")
    return {"target": f"nc {get_host_ip(config)} {free_port}", "port": free_port}