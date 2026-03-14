from scripts.state import load_current, load_progress
from scripts.catalog import load_catalog


def get_challenge(name):
    catalog = load_catalog()
    for c in catalog:
        if c["name"] == name:
            return c
    return None


def resume_challenge():
    progress = load_progress()
    unfinished = progress.get("unfinished", [])

    if not unfinished:
        print("\n   No Unfinished challenges:\n")
        return
    
    print("\n   Unfinished challenges:\n")
    for i, name in enumerate(unfinished, 1):
        challenge = get_challenge(name)
        if challenge:
            hints_used = progress.get("hints_used", {}).get(name, [])
            hints_total = len(challenge.get("hints", []))
            print(f"    {i} - {name}  [{challenge.get('theme', '')} / {challenge.get('difficulty', '')}]   hints used: {len(hints_used)}/{hints_total}")
        
        else:
            print(f"    {i} - {name}")
    
    print()
    choice = input("  > ").strip()

    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(unfinished):
            name = unfinished[idx]
            challenge = get_challenge(name)
            if challenge:
                from scripts.start import launch_challenges
                launch_challenges(challenge)
            else:
                print(f"\n  Challenge {name} not found in catalog.\n")
        else:
            print("\n   Invalid choice.\n")
    else:
        print("\n   Invalide choice.\n")