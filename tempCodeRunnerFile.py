def handle_town_menu():
    print(f"DAY {player['day']}")
    show_town_menu()
    choice = input("Your choice? ").strip().lower()
    if choice == 'b':
        game_state = 'buy'
        choice = input("Your choice? ").strip().lower()
    elif choice == 'i':
        show_information(player)
    elif choice == 'm':
        draw_map(game_map, fog, player)
    elif choice == 'e':
        print("You enter the mine, ready to start your adventure.")
        game_state = 'in_mine'
    elif choice == 'v':
        save_game(game_map, fog, player)
        print("Game saved successfully.")
    elif choice == 'q':
        game_state = 'main'