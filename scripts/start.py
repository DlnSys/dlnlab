import random

from InquirerPy import inquirer

from scripts.catalog import load_catalog
from scripts.state import load_progress, load_current, save_current, save_progress, clear_current
from scripts.stop import stop_runtime
from scripts.colors import CYAN, RED, RESET, BOLD, YELLOW


CATEGORIES = ["web", "reverse", "crypto", "forensics", "pwn", "misc"]
DIFFICULTIES = ["easy", "medium", "hard"]


def start_challenge():
    category = inquirer.select(
        message="Category:",
        choices=[c.capitalize() for c in CATEGORIES] + ["Random"],
    ).execute()

    difficulty = inquirer.select(
        message="Difficulty:",
        choices=[d.capitalize() for d in DIFFICULTIES] + ["Random"],
    ).execute()

    catalog = load_catalog()
    progress = load_progress()

    completed = progress.get("completed", [])
    current = load_current()
    current_name = current.get("name")

    cat_filter = None if category == "Random" else category.lower()
    diff_filter = None if difficulty == "Random" else difficulty.lower()

    candidates = [
        c for c in catalog
        if (cat_filter is None or c.get("theme") == cat_filter or c.get("category") == cat_filter)
        and (diff_filter is None or c.get("difficulty") == diff_filter)
        and c.get("name") not in completed
        and c.get("name") != current_name 
    ]

    if not candidates:
        print("\nNo challenges available for this selection.")
        return
    
    choices = ["Random"] + [c["name"] for c in candidates]

    selection = inquirer.select(
        message="Challenge:",
        choices=choices,
    ).execute()

    if selection == "Random":
        challenge = random.choice(candidates)
    else:
        challenge = next(c for c in candidates if c["name"] == selection)
    
    if current_name:
        confirm = inquirer.confirm(
            message=f"'{current_name}' is active. Replace it (kept as unfinished)?",
            default=False,
        ).execute()
        if not confirm:
            return
        progress = load_progress()
        if current_name not in progress.get("unfinished", []):
            progress.setdefault("unfinished", []).append(current_name)

        save_progress(progress)
        stop_runtime(current)
        clear_current()
        
    launch_challenges(challenge)


def launch_challenges(challenge):
    from scripts.runtime import launch_runtime

    runtime_info = launch_runtime(challenge)

    print()                                                                                                                                                                                                     
    print(f"{CYAN}╔══════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}         CHALLENGE STARTED            {RESET}  {CYAN}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════╝{RESET}")
    print()
    print(f"  Name       : {challenge['name']}")                                                                                                                                                                
    print(f"  Category   : {challenge.get('theme', '')} / {challenge.get('category', '')}")                                                                                                                     
    print(f"  Difficulty : {YELLOW}{challenge.get('difficulty', '').capitalize()}{RESET}")                                                                                                                                     
    print(f"  Source     : {challenge.get('source', '').capitalize()}")                                                                                                                                         
    print()                                                                                                                                                                                                     
    print(f"  Brief :\n    {challenge.get('description', '').strip()}")
    print() 

    if runtime_info.get("target"):
        print(f"  Target     : {BOLD}{runtime_info['target']}{RESET}")

    print(f"  Flag format: {challenge.get('flag', {}).get('format', '???')}")                                                                                                                                   
    print()                                                                                                                                                                                                     
    print("  Commands:")                                                                                                                                                                                        
    print("    dlnlab submit <flag>   → submit a flag")   
    print("    dlnlab hint            → get a hint")                                                                                                                                                            
    print("    dlnlab stop            → stop the challenge")
    print()

    save_current({
        "name": challenge["name"],
        "runtime": challenge.get("runtime"),
        "started_at": __import__("datetime").datetime.now().isoformat(),
        "container_id": runtime_info.get("container_id")
    })