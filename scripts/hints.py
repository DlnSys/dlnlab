from scripts.state import load_current, load_progress, save_progress
from scripts.catalog import load_catalog
from scripts.colors import YELLOW, RED, RESET


def get_challenge(name):
    catalog = load_catalog()
    for c in catalog:
        if c["name"] == name:
            return c
    return None


def show_hint():
    current = load_current()
    if not current:
        print(f"{RED}\n   No active challenge. Start one with: dlnlab start{RESET}")
        return
    
    challenge = get_challenge(current["name"])
    if not challenge:
        print(f"{RED}\n   Error: current challenge not found in catalog.{RESET}")
        return
    
    hints = challenge.get("hints", [])
    if not hints:
        print(f"{RED}\n   No hints available for this challenge.\n{RESET}")
        return
    
    progress = load_progress()
    hints_used = progress("hints_used", {})
    used = hints_used.get(current["name"], [])

    next_index = len(used)

    if next_index >= len(hints):
        print(f"{RED}\n   All hints have been used.\n{RESET}")
        return
    
    hint = hints[next_index]
    print(f"\n {YELLOW}Hint {next_index + 1}/{len(hints)}{RESET} : {hint}\n")

    if next_index + 1 < len(hints):
        answer = input("    Unlock next hint ? [y/N] ").strip().lower()
        if answer == "y":
            used.append(next_index)
            hints_used[current["name"]] = used
            progress["hints_used"] = hints_used
            save_progress(progress)
            show_hint()
    
    else:
        used.append(next_index)
        hints_used[current["name"]] = used
        progress["hints_used"] = hints_used
        save_progress(progress)