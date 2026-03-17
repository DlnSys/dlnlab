import hashlib
import os

from datetime import datetime

from scripts.state import load_current, load_progress, save_progress, clear_current
from scripts.config import load_config
from scripts.catalog import load_catalog
from scripts.stop import stop_runtime
from scripts.colors import RED, RESET, BOLD, GREEN, YELLOW


def hash_flag(flag):
    return hashlib.sha256(flag.strip().encode()).hexdigest()


def get_challenge(name):
    catalog = load_catalog()
    for c in catalog:
        if c["name"] == name:
            return c
    return None


def submit_flag(flag):
    if not flag:
        print("Usage: dlnlab submit <flag>")
        return
    
    current = load_current()
    if not current:
        print("No active challenge. Start one with: dlnlab start")
        return
    
    challenge = get_challenge(current["name"])
    if not challenge:
        print("Error: current challenge not found in catalog.")
        return
    
    expected_hash = challenge.get("flag", {}).get("value", "")
    submitted_hash = hash_flag(flag)

    if submitted_hash == expected_hash:
        print()
        print(f"{GREEN} Correct Flag! Challenge completed.{RESET}")
        started_at = current.get("started_at")
        minutes, seconds = 0, 0
        if started_at:
            delta = datetime.now() - datetime.fromisoformat(started_at)
            minutes, seconds = divmod(int(delta.total_seconds()), 60)
            print(f"  Time       : {BOLD}{minutes}m {seconds}s{RESET}")

        progress = load_progress()
        progress["completed"].append(current["name"])
        history_entry = {
            "name": current["name"],
            "completed_at": datetime.now().isoformat(),
            "time": f"{minutes}m {seconds}s" if started_at else "?" 
        }
        progress.setdefault("history", []).append(history_entry)

        if current["name"] in progress.get("unfinished", []):
            progress["unfinished"].remove(current["name"])
        save_progress(progress)
        stop_runtime(current, cleanup=True)
        clear_current()

        config = load_config()
        writeup_path = challenge.get("writeup", "")
        if writeup_path:
            full_path = os.path.join(os.path.dirname(__file__), "..", writeup_path)
            if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
                print(f"\n  {YELLOW}Write-Up unlocked{RESET} -> {writeup_path}")
                answer = input("    Open Write-Up? [y/N] ").strip().lower()
                if answer == "y":
                    os.system(f"cat '{full_path}'")
            else:
                print("\n   No Write-Up available for this challenge yet.")
        print()
    else:
        print()
        print(f"{RED} Wrong Flag. Keep trying.{RESET}")
        print()