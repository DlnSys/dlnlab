import subprocess
import os

from InquirerPy import inquirer

from scripts.state import load_current, load_progress, save_progress, clear_current
from scripts.config import load_config
from scripts.colors import CYAN, GREEN, YELLOW, RED, RESET


def stop_challenge():
    current = load_current()
    if not current:
        print(f"{RED}\n   No active challenge.\n{RESET}")
        return
    
    name = current.get("name")

    choice = inquirer.select(
        message=f"Stop '{name}': ",
        choices=["Mark as completed", "Keep as unfinished", "Cancel"],
        default=0,
    ).execute()

    if choice == "Mark as completed":
        progress = load_progress()
        if name not in progress["completed"]:
            progress["completed"].append(name)
        if name in progress.get("unfinished", []):
            progress["unfinished"].remove(name)
        
        save_progress(progress)
        stop_runtime(current, cleanup=True)
        clear_current()

        print(f"\n   {GREEN}Challenge {name} marked as completed.\n{RESET}")

    elif choice == "Keep as unfinished":
        progress = load_progress()
        if name not in progress.get("unfinished", []):
            progress.setdefault("unfinished", []).append(name)
        
        save_progress(progress)
        stop_runtime(current)
        clear_current()
        print(f"\n  {YELLOW}Challenge {name} kept as unfinished.\n{RESET}")

    elif choice == "Cancel":
        print(f"{RED}\n   Cancelled.\n{RESET}")

def stop_runtime(current, cleanup=False):
    Runtime = current.get("runtime")
    if Runtime in ("docker", "netcat"):
        config = load_config()
        boxes_dir = os.path.join(os.path.dirname(__file__), "..", config["boxes_dir"])
        compose_dir = os.path.join(boxes_dir, current["name"])
        if os.path.exists(compose_dir):
            cmd = ["docker", "compose", "down"]
            if cleanup:
                cmd += ["--rmi", "all"]
            subprocess.run(cmd, cwd=compose_dir)
            override_path = os.path.join(compose_dir, "docker-compose.override.yml")
            if os.path.exists(override_path):
                os.remove(override_path)
    elif Runtime == "file" and cleanup:
        config = load_config()
        workspace = os.path.expanduser(config.get("workspace_dir", "~/dlnlab/workspace"))
        name = current.get("name", "")
        from scripts.catalog import load_catalog
        catalog = load_catalog()
        challenge = next((c for c in catalog if c["name"] == name), None)
        if challenge:
            file_field = challenge.get("file", "")
            files = file_field if isinstance(file_field, list) else [file_field]
            for filename in files:
                dst = os.path.join(workspace, filename)
                if os.path.exists(dst):
                    os.remove(dst)