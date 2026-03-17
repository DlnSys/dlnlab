from scripts.catalog import load_catalog
from scripts.state import load_progress
from scripts.colors import CYAN, GREEN, YELLOW, BOLD, RESET


def list_challenges():
    catalog = load_catalog()
    progress = load_progress()
    completed = progress.get("completed", [])
    unfinished = progress.get("unfinished", [])

    categories = ["web", "reverse", "crypto", "forensics", "pwn", "misc"]

    print()
    print(f"{CYAN}╔══════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}           CHALLENGE LIST             {RESET}  {CYAN}║{RESET}")
    print(f"{CYAN}╚══════════════════════════════════════════╝{RESET}")

    for cat in categories:
        challenges = [c for c in catalog if c.get("theme") == cat or c.get("category") == cat]
        if not challenges:
            continue
        print(f"\n  {CYAN}{cat.upper()}{RESET}")
        for c in challenges:
            name = c["name"]
            diff = c.get("difficulty", "?")
            if name in completed:
                status = f"{GREEN}✓{RESET}"
            elif name in unfinished:
                status = f"{YELLOW}~{RESET}"
            else:
                status = "○"
            print(f"    {status} {name}  [{diff}]")
    print()