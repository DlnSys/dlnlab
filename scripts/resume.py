from InquirerPy import inquirer

from scripts.state import load_current, load_progress
from scripts.catalog import load_catalog
from scripts.colors import CYAN, YELLOW, RED, RESET


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
        print(f"{RED}\n   No Unfinished challenges.\n{RESET}")
        return
    
    choices = []
    for name in unfinished:
        challenge = get_challenge(name)
        if challenge:
            hints_used = progress.get("hints_used", {}).get(name, [])
            hints_total = len(challenge.get("hints", []))
            label = f"{name}  [{challenge.get('theme', '')} / {challenge.get('difficulty', '')}]  hints: {len(hints_used)}/{hints_total}"
            choices.append({"name": label, "value": name})
        
        else:
            choices.append({"name": name, "value": name})

    selection = inquirer.select(
        message="Resume which challenge ?",
        choices=choices,
    ).execute()

    challenge = get_challenge(selection)
    if challenge:
        from scripts.start import launch_challenges
        launch_challenges(challenge)
    else:
        print(f"{RED}\n  Challenge {selection} not found in catalog.\n{RESET}")