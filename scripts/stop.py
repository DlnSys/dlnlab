import subprocess
import os

from scripts.state import load_current, load_progress, save_progress, clear_current
from scripts.config import load_config


def stop_challenge():
    current = load_current()
    if not current:
        print("\n   No active challenge.\n")
        return
    
    name = current.get("name")
    print(f"\n  Stop current challenge: {name}")          
    print()                                                                                                                                                                                                     
    print("    1 - Mark as completed")                                                                                                                                                                          
    print("    2 - Keep as unfinished")                                                                                                                                                                         
    print("    3 - Cancel")                                                                                                                                                                                     
    print()
    choice = input("  > ").strip()


    if choice == "1":
        progress = load_progress()
        if name not in progress["completed"]:
            progress["completed"].append(name)
        if name in progress.get("unfinished", []):
            progress["unfinished"].remove(name)
        
        save_progress(progress)
        stop_runtime(current)
        clear_current()
        print("\n   Challenge {name} marked as completed.\n")

    elif choice == "2":
        progress = load_progress()
        if name not in progress.get("unfinished", []):
            progress.setdefault("unfinished", []).append(name)
        save_progress(progress)
        stop_runtime(current)
        clear_current()
        print(f"\n  Challenge {name} kept as unfinished.\n")

    elif choice == "3":
        print("\n   Cancelled.\n")

    else:
        print("\n   Invalid choice.\n")


def stop_runtime(current):
    Runtime = current.get("runtime")
    if Runtime in ("docker", "netcat"):
        config = load_config()
        boxes_dir = os.path.join(os.path.dirname(__file__), "..", config["boxes_dir"])
        compose_dir = os.path.join(boxes_dir, current["name"])
        if os.path.exists(compose_dir):
            result = subprocess.run(
                ["docker", "compose", "down"],
                cwd=compose_dir,
            )