import random

from scripts.catalog import load_catalog
from scripts.state import load_progress, load_current, save_current
from scripts.config import load_config


CATEGORIES = ["web", "reverse", "crypto", "forensics", "pwn", "misc"]
DIFFICULTIES = ["easy", "medium", "hard"]


def select_category():
    print("\nCategory:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i} - {cat.capitalize()}")
    print(f"  {len(CATEGORIES)+1} - Random")
    choice = input("\n> ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(CATEGORIES):
            return CATEGORIES[idx]
    return None # Random


def select_difficulty():
    print("\nDifficulty:")
    for i, diff in enumerate(DIFFICULTIES, 1):
        print(f"  {i} - {diff.capitalize()}")
    print(f"  {len(DIFFICULTIES)+1} - Random")
    choice = input("\n> ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(DIFFICULTIES):
            return DIFFICULTIES[idx]
    return None # Random


def start_challenge():
    category = select_category()
    difficulty = select_difficulty()

    catalog = load_catalog()
    progress = load_progress()

    completed = progress.get("completed", [])
    current = load_current()
    current_name = current.get("name")

    candidates = [
        c for c in catalog
        if (category is None or c.get("theme") == category or c.get("category") == category)
        and (difficulty is None or c.get("difficulty") == difficulty)
        and c.get("name") not in completed
        and c.get("name") != current_name 
    ]

    if not candidates:
        print("\nNo challenges available for this selection.")
        return
    
    challenge = random.choice(candidates)
    launch_challenges(challenge)


def launch_challenges(challenge):
    from scripts.runtime import launch_runtime

    runtime_info = launch_runtime(challenge)

    print()                                                                                                                                                                                                     
    print("╔══════════════════════════════════════════╗") 
    print("║           CHALLENGE STARTED              ║")                                                                                                                                                       
    print("╚══════════════════════════════════════════╝")                                                                                                                                                       
    print()                                                                                                                                                                                                     
    print(f"  Name       : {challenge['name']}")                                                                                                                                                                
    print(f"  Category   : {challenge.get('theme', '')} / {challenge.get('category', '')}")                                                                                                                     
    print(f"  Difficulty : {challenge.get('difficulty', '').capitalize()}")                                                                                                                                     
    print(f"  Source     : {challenge.get('source', '').capitalize()}")                                                                                                                                         
    print()                                                                                                                                                                                                     
    print(f"  Brief :\n    {challenge.get('description', '').strip()}")
    print() 

    if runtime_info.get("target"):
        print(f"  Target     : {runtime_info['target']}")

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