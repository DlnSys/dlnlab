from scripts.state import load_progress
from scripts.catalog import load_catalog
from scripts.colors import CYAN, GREEN, BOLD, RESET


def show_progress():
    progress = load_progress()
    catalog = load_catalog()

    completed = progress.get("completed", [])
    unfinished = progress.get("unfinished", [])
    total = len(catalog)
    remaining = total - len(completed) - len(unfinished)

    print()                                                                                                                                                                                                     
    print(f"{CYAN}╔══════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}║{RESET}  {BOLD}            PROGRESSION               {RESET}  {CYAN}║{RESET}")
    print(f"{CYAN}╔══════════════════════════════════════════╗{RESET}")
    print()                                                                                                                                                                                                     
    print(f"  {GREEN}Completed{RESET}   : {len(completed)}")
    print(f"  Unfinished  : {len(unfinished)}")                                                                                                                                                                 
    print(f"  Remaining   : {remaining}")                 
    print(f"  Total       : {total}")                                                                                                                                                                           
    print()                                                                                                                                                                                                     
    print("  By category:")

    categories = ["web", "reverse", "crypto", "forensics", "pwn", "misc"]

    for cat in categories:
        cat_total = [c for c in catalog if c.get("theme") == cat or c.get("category") == cat]
        cat_done = [c for c in cat_total if c["name"] in completed]

        total_cat = len(cat_total)
        done_cat = len(cat_done)

        if total_cat == 0:
            bar = "░" * 10
        else:
            filled = int((done_cat / total_cat) * 10)
            bar = f"{GREEN}" + "█" * filled + f"{RESET}" + "░" * (10 - filled)

        print(f"  {cat:<12} {bar}  {done_cat}/{total_cat}")

    print()