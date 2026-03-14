import os
import subprocess

from scripts.config import load_config


def launch_runtime(challenge):
    runtime = challenge.get("runtime")
    config = load_config()
    boxes_dir = os.path.join(os.path.dirname(__file__), "..", config["boxes_dir"])

    if runtime == "file":
        return launch_file(challenge, config)
    
    elif runtime == "docker":
        return launch_docker(challenge, boxes_dir)
    
    elif runtime == "netcat":
        return launch_netcat(challenge, boxes_dir)

    else:
        print(f"Unknown runtime: {runtime}")
        return {}
    

def launch_file(challenge, config):
    challenges_dir = os.path.join(os.path.dirname(__file__), "..", config["challenges_dir"])
    file_path = os.path.join(challenges_dir, challenge.get("file", ""))
    print(f"\n  File : {file_path}")
    return {}


def launch_docker(challenge, boxes_dir):
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
    
    print(f"    Docker Started.")
    return {"target": f"http://127.0.0.1:{port}"}


def launch_netcat(challenge, boxes_dir):
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
    
    print(f"    Netcat Started.")
    return {"target": f"nc {host} {port}"}