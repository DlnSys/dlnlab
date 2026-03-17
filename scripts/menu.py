from InquirerPy import inquirer

from scripts.state import load_current
from scripts.colors import CYAN, BOLD, RED, RESET


def main_menu():
    current = load_current()

    print()
    print(f"{CYAN}╔══════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}       D L N L A B        {RESET}  {CYAN}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════╝{RESET}")
    print()

    choices = [
        "Start new challenge",
        "Resume unfinished challenges",
        "Show progress",
        "Exit",
    ]

    choice = inquirer.select(
        message="",
        choices=choices,
    ).execute()

    if choice == "Start new challenge":
        from scripts.start import start_challenge
        start_challenge()

    elif choice == "Resume unfinished challenges":
        from scripts.resume import resume_challenge
        resume_challenge()
    
    elif choice == "Show progress":
        from scripts.progress import show_progress
        show_progress()

    elif choice == "Exit":
        print()
        exit(0)