from scripts.state import load_current


def main_menu():
    current = load_current()

    print()                                               
    print("╔══════════════════════════════╗")                                                                                                                                                                   
    print("║         D L N L A B          ║")                                                                                                                                                                   
    print("╚══════════════════════════════╝")                                                                                                                                                                   
    print()                                                                                                                                                                                                     
    print("  1 - Start new challenge")                                                                                                                                                                          
    print("  2 - Resume unfinished challenge")                                                                                                                                                                  
    print("  3 - Show progress")
    print("  4 - Exit")                                                                                                                                                                                         
    print()  

    choice = input("> ").strip()

    if choice == "1":
        from scripts.start import start_challenge
        start_challenge()

    elif choice == "2":
        from scripts.resume import resume_challenge
        resume_challenge()
    
    elif choice == "3":
        from scripts.progress import show_progress
        show_progress()

    elif choice == "4":
        print()
        exit(0)
    
    else:
        print("Invalid choice.")
        main_menu()