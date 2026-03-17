import os
import subprocess
import socket
import time

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
    

def launch_file(challenge, config):
    challenges_dir = os.path.join(os.path.dirname(__file__), "..", config["challenges_dir"])
    file_path = os.path.join(challenges_dir, challenge.get("file", ""))
    print(f"\n  File : {file_path}")
    return {}


def launch_docker(challenge, boxes_dir, config):
    compose_path = os.path.join(boxes_dir, challenge["name"], challenge.get("compose", "docker-compose.yml"))
    port = challenge.get("port", 8080)

    print(f"\n  Starting Docker environment...")
    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=os.path.dirname(compose_path),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"    Error: {result.stderr}")
        return {}
    
    if wait_for_port("127.0.0.1", port):
        print(f"    Docker Started.")
    else:
        print(f"    Warning: service not reachable on port {port}.")
    return {"target": f"http://{get_host_ip(config)}:{port}"}


def launch_netcat(challenge, boxes_dir, config):
    compose_path = os.path.join(boxes_dir, challenge["name"], challenge.get("compose", "docker-compose.yml"))
    host = challenge.get("host", "127.0.0.1")
    port = challenge.get("port", 4444)

    print(f"\n  Starting netcat environment...")
    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=os.path.dirname(compose_path),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"    Error: {result.stderr}")
        return {}
    
    if wait_for_port("127.0.0.1", port):
        print(f"    Netcat Started.")
    else:
        (f"    Warning: service not reachable on port {port}.")
    return {"target": f"nc {get_host_ip(config)} {port}"}