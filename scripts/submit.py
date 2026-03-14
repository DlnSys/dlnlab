import hashlib
import os

from scripts.state import load_current, load_progress, save_progress, clear_current
from scripts.config import load_config
from scripts.catalog import load_catalog
from scripts.stop import stop_runtime


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
        print(" Correct Flag! Challenge completed.")

        progress = load_progress()
        progress["completed"].append(current["name"])
        if current["name"] in progress.get("unfinished", []):
            progress["unfinished"].remove(current["name"])
        save_progress(progress)
        stop_runtime(current)
        clear_current()

        config = load_config()
        writeup_path = challenge.get("writeup", "")
        if writeup_path:
            full_path = os.path.join(os.path.dirname(__file__), "..", writeup_path)
            if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
                print(f"\n  Write-Up unlocked -> {writeup_path}")
                answer = input("    Open Write-Up? [y/N] ").strip().lower()
                if answer == "y":
                    os.system(f"cat '{full_path}'")
            else:
                print("\n   No Write-Up available for this challenge yet.")
        print()
    else:
        print()
        print(" Wrong Flag. Keep trying.")
        print()