from scripts.catalog import load_catalog
from scripts.state import load_progress
from scripts.colors import CYAN, GREEN, YELLOW, RED, BOLD, RESET


def show_info(name):
    if not name:
        print(f"{RED}Usage: dlnlab info <challenge_name>{RESET}")
        return
    
    catalog = load_catalog()
    challenge = next((c for c in catalog if c["name"] == name), None)

    if not challenge:
        print(f"{RED}Challenge '{name}' not found.{RESET}")
        return
    
    progress = load_progress()
    completed = progress.get("completed", [])
    unfinished = progress.get("unfinished", [])

    if name in completed:
        status = f"{GREEN}Completed ✓{RESET}"
    elif name in unfinished:
        status = f"{YELLOW}Unfinished ~{RESET}"
    else:
        status = "Not started ○"

    hints = challenge.get("hints", [])

    print()
    print(f"{CYAN}╔══════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}          CHALLENGE INFO              {RESET}  {CYAN}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════╝{RESET}")
    print()
    print(f"  {BOLD}Name{RESET}       : {challenge['name']}")
    print(f"  {BOLD}Category{RESET}   : {challenge.get('theme', '')} / {challenge.get('category', '')}")
    print(f"  {BOLD}Difficulty{RESET} : {YELLOW}{challenge.get('difficulty', '').capitalize()}{RESET}")
    print(f"  {BOLD}Source{RESET}     : {challenge.get('source', '').capitalize()}")
    print(f"  {BOLD}Runtime{RESET}    : {challenge.get('runtime', '')}")
    print(f"  {BOLD}Status{RESET}     : {status}")
    print(f"  {BOLD}Hints{RESET}      : {len(hints)} available")
    print()
    print(f"  {BOLD}Brief{RESET} :\n    {challenge.get('description', '').strip()}")
    print()