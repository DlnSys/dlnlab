from scripts.state import load_progress
from scripts.colors import CYAN, GREEN, YELLOW, BOLD, RESET


def show_history():
    progress = load_progress()
    history = progress.get("history", [])

    print()
    print(f"{CYAN}╔══════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}            HISTORY                   {RESET}  {CYAN}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════╝{RESET}")
    print()

    if not history:
        print(f"  No completed challenges yet.\n")
        return
    
    for entry in history:
        name = entry.get("name", "?")
        completed_at = entry.get("completed_at", "?")[:10]
        time = entry.get("time", "?")
        print(f"  {GREEN}✓{RESET} {BOLD}{name}{RESET}")
        print(f"      Date : {completed_at}")
        print(f"      Time : {YELLOW}{time}{RESET}")
        print()