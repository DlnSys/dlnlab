from scripts.state import load_current, load_progress, save_progress
from scripts.catalog import load_catalog


def get_challenge(name):
    catalog = load_catalog()
    for c in catalog:
        if c["name"] == name:
            return c
    return None


def show_hint():
    current = load_current()
    if not current:
        print("No active challenge. Start one with: dlnlab start")
        return
    
    challenge = get_challenge(current["name"])
    if not challenge:
        print("Error: current challenge not found in catalog.")
        return
    
    hints = challenge.get("hints", [])
    if not hints:
        print("\n   No hints available for this challenge.\n")
        return
    
    progress = load_progress()
    hints_used = progress("hints_used", {})
    used = hints_used.get(current["name"], [])

    next_index = len(used)

    if next_index >= len(hints):
        print("\n All hints have been used.\n")
        return
    
    hint = hints[next_index]
    print(f"\n Hint {next_index + 1}/{len(hints)} : {hint}\n")

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