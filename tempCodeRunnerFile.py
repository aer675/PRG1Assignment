# S10273247G Assignment.py
# Aerica Gan
# P12
# 10 August 2025
# Description: A text-based mining game where the player mines for minerals, 
# sells them, and upgrades their equipment to reach a goal of 500 GP to win the game.

from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = {1: 50, 2: 150} # Key is the pickaxe level, value is the price to upgrade

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(LEVEL1, map_struct):
    map_file = open(LEVEL1, 'r')
    lines = map_file.readlines()

    map_struct.clear() # Clear the existing map structure 
    
    # TODO: Add your map loading code here
    for line in lines: 
        line = line.strip() 
        if line:
            map_struct.append(list(line)) # Convert the line to a list of characters

# Change the two main variables to keep track of the map size
    global MAP_WIDTH 
    global MAP_HEIGHT    

# Calculate the width and height of the map
    if map_struct:  # Check if the map_struct is not empty
        MAP_WIDTH = len(map_struct[0])
        MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function initializes the fog of war
    # TODO: initialize fog
def initialize_fog():
    new_fog = []
    for y in range(MAP_HEIGHT):
        row = ['?'] * MAP_WIDTH  # Initialize each row with '?' to represent fog
        new_fog.append(row)
    return new_fog

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    # Clear the fog around the player
    for y in range(max(0, player['y'] - 1), min(MAP_HEIGHT, player['y'] + 2)):
        for x in range(max(0, player['x'] - 1), min(MAP_WIDTH, player['x'] + 2)):
            fog[y][x] = ' '
    return

# This function initializes the game state
def initialize_game(game_map, fog, player):
    # initialize map
    load_map("PRG1Assignment/LEVEL1.txt", game_map)

    new_fog = initialize_fog()  # Initialize the fog of war
    fog.clear()
    fog.extend(new_fog)  # Set the fog to the new initialized fog

    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player.clear()  # Clear the existing player data
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 1
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['name'] = "" # Player's name
    player['backpack'] = 10 # Game start with 10 item capacity
    player['pickaxe'] = 1 # Game starts with pickaxe level 1
    player['portalx'] = 0 # Portal position x
    player['portaly'] = 0 # Portal position y

    clear_fog(fog, player) # Clear the fog around the player at the start of the game
    
# This function draws the entire map, covered by the fog
def draw_map(game_map, fog, player):
    print("----- Mine Map -----")
    print("+" + "-" * MAP_WIDTH + "+")
    for y in range(MAP_HEIGHT):
        row_to_print = []
        for x in range(MAP_WIDTH):
            if fog[y][x] == '?':
                row_to_print.append('?')
            elif player ['y'] == y and player['x'] == x:
                row_to_print.append('M')
            elif player['portalx'] == x and player['portaly'] == y:
                row_to_print.append('P')
            else:
                row_to_print.append(game_map[y][x])
        print("|" + ''.join(row_to_print) + "|")
    print("+" + "-" * MAP_WIDTH + "+")
    print()
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    print("+" + "-" * 3 + "+")
    for y_offset in range(-1, 2):
        row_str = "|"
        for x_offset in range(-1, 2):
            y = player['y'] + y_offset
            x = player['x'] + x_offset
            if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                if player['y'] == y and player ['x'] == x:
                    row_str += ' M '

                elif player['portalx'] == x and player['portaly'] == y:
                    row_str += ' P '

                elif fog[y][x]=='?':
                    row_str += ' ? '

                else:
                    row_str += ' ' + game_map[y][x] + ' '
            else:
                row_str += ' # ' #Wall of mine
        row_str += "|"
        print(row_str)
    print("+" + "-" * 3 + "+")
    return

# This function shows the information for the player
def show_information(player):
    print()
    print("----- Player Information -----")
    print(f"Name: {player['name']}")
    print(f"Portal position: ({player['portalx']}, {player['portaly']})")
     # Level of the pickaxe and the minerals it can mine
    print(f"Pickaxe level: {player['pickaxe']}")
    print("------------------------------")
    print(f"Load: {player['copper'] + player['silver'] + player['gold']} / {player ['backpack']}")
    print("------------------------------")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    print("------------------------------")
    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    with open('save_game.txt', 'w') as f:
        f.write(f"Map Width: {MAP_WIDTH}\n")
        f.write(f"Map Height: {MAP_HEIGHT}\n")
        # Save the map
        for row in game_map:
            f.write(''.join(row) + '\n')
        f.write('\n')  # Add a newline to separate map from player data
        # Save the fog
        for row in fog:
            f.write(''.join(row) + '\n')
        f.write('\n')  # Add a newline to separate fog from player data
        # Save the player data
        for key, value in player.items():
            f.write(f"{key}:{value}\n")
    print("Game saved successfully.")
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    with open('save_game.txt', 'r') as f:
        lines = f.readlines()      
    # Load the map
    game_map.clear()
    for line in lines:
        line = line.strip()
        if line and not line.startswith('?'):
            game_map.append(list(line))  # Convert the line to a list of characters
    # Load the fog
    fog.clear()
    for line in lines:
        line = line.strip()         
        if line and line.startswith('?'):
            fog.append(list(line))  # Convert the line to a list of characters          
    # Load the player data
    for line in lines:
        line = line.strip()
        if line and ':' in line:
            key, value = line.split(':', 1) 
            if key in player:
                if value.isdigit():     
                    player[key] = int(value)  # Convert to integer if it's a number
                else:
                    player[key] = value  # Keep as string otherwise
    print("Game loaded successfully.")
    return 

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    #    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu():
    print()
    # TODO: Show Day
    print(f"DAY {player['day']}")
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

#This function shows the buy menu
def show_buy_menu():
    print()
    print("----------------------- Shop Menu -------------------------")
    if player['pickaxe'] < len(minerals):
        next_pickaxe = player['pickaxe'] + 1
        upgrade_cost = pickaxe_price.get(next_pickaxe, 0)
        next_mineral = minerals[player['pickaxe']]
        print(f"(P)ickaxe upgrade to level {next_pickaxe} ({upgrade_cost} GP) - can mine {next_mineral}")
    else:
        print("Your pickaxe is already at the highest level.")
    bcost = player['backpack'] * 2 # Cost of the backpack upgrade
    print(f"(B)ackpack upgrade to carry {player['backpack'] + 2} items for ({bcost} GP)")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP {player['GP']}")
    print("-----------------------------------------------------------")

# This function shows the mine menu
def show_mine_menu():
    print()
    print("---------------------------------------------------")
    print(f"                       DAY {player['day']}                       ")
    print("---------------------------------------------------")
    # print mini map 
    draw_view(game_map, fog, player)
    print(f"Turns left: {player['turns']}    Load: {player['copper'] + player['silver'] + player['gold']} / {player['backpack']}    Steps: {player['steps']}    ")
    print("(WASD) to move")
    print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")

def sell_all_ores():
    total_gp = 0

    if player['copper'] > 0:
        copper_gp = randint(prices['copper'][0], prices['copper'][1]) * player['copper']
        player['GP'] += copper_gp
        total_gp += copper_gp
        print(f"You sold {player['copper']} pieces of copper ore for {copper_gp} GP.")
        player['copper'] = 0
    
    if player['silver'] > 0:
        silver_gp = randint(prices['silver'][0], prices['silver'][1]) * player['silver']
        player['GP'] += silver_gp
        total_gp += silver_gp
        print(f"You sold {player['silver']} pieces of silver ore for {silver_gp} GP.")
        player['silver'] = 0
    
    if player['gold'] > 0:
        gold_gp = randint(prices['gold'][0], prices['gold'][1]) * player['gold']
        player['GP'] += gold_gp
        total_gp += gold_gp
        print(f"You sold {player['gold']} pieces of gold ore for {gold_gp} GP.")
        player['gold'] = 0

    # Total GP earned from selling ores
    if total_gp > 0:
        print(f"Total GP earned from selling ores: {total_gp}")
           
    # Check if player has enough GP to win
    if player['GP'] >= WIN_GP:
        print(f"Congratulations, {player['name']}! You have earned {player['GP']} GP and won the game!")
        return 'quit'
    
    return 'town'  # Return to the town menu after selling ores


#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 500 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!  
#Below are the functions that handle the different game states

# This function handles the main menu
def handle_main_menu():
    show_main_menu()
    choice = input("Your choice? ").strip().lower()
    if choice == 'n':
        # Initialize the game state
        initialize_game(game_map, fog, player)
        player['day'] = 1
        name = str(input("Greetings, miner! What is your name? "))
        print(f"Pleased to meet you, {name}. Welcome to Sundrop Town!")
        player['name'] = name
        return 'town'
    elif choice == 'l':
        load_game(game_map, fog, player)
        print("Game loaded successfully.")
        return 'load' # This will return to the town menu after loading
    elif choice == 'q':
        return 'quit'
    else:
        print ('Error. Please enter a valid choice.')
        return 'main' # This will return to the main menu if the input is invalid to prevent breaking the game loop

# This function handles the town menu
def handle_town_menu():
    print()
    show_town_menu()
    choice = input("Your choice? ").strip().lower()
    if choice == 'b':
        return 'buy'
    elif choice == 'i':
        show_information(player)
        handle_town_menu ()
    elif choice == 'm':
        draw_map(game_map, fog, player)
        handle_town_menu()
    elif choice == 'e':
        print("You enter the mine, ready to start your adventure.")
        return 'in_mine'
    elif choice == 'v':
        save_game(game_map, fog, player)
        print("Game saved successfully.")
        handle_town_menu()
    elif choice == 'q':
        return 'main' # This will return to the main menu

# This function handles the buy menu
# i Omfg this is soooo wcwcnsjodcbsxjin
def handle_buy_menu():
    while True:
        bcost = player['backpack'] * 2 # Cost of the backpack upgrade
        pcost = pickaxe_price.get(player['pickaxe'], 0) # Cost of the pickaxe upgrade

        show_buy_menu()
        choice = input("Your choice? ").strip().lower()
        if choice == 'p' and player['GP'] >= pcost:
            player['GP'] -= pcost
            player['pickaxe'] += 1
            if player['pickaxe'] == 1:
                print("Congratulations! You can now mine copper!")
            elif player['pickaxe'] == 2:
                print("Congratulations! You can now mine silver!")
            elif player['pickaxe'] == 3:
                print("Congratulations! You can now mine gold!")
            continue

        elif choice == 'b' and player['GP'] >= bcost:
            print(f"Congratulations! You can now carry {player['backpack'] + 2} items!")
            player['GP'] -= bcost
            player['backpack'] += 2            

            continue

        elif choice =='l':
            return 'town'
        
        else:
            print("Error. Please enter a valid choice.")
            continue 

# This function handles the mine menu
#BEUHEUICNOINXCDSIJNCIDNDUIDNMKSx
def handle_mine_menu():
    # only 20 turns per day
    while player['turns'] > 0:
        show_mine_menu()
        choice = input("Action? ").strip().lower()

        # W, A, S, D for movement, 
        #If player steps onto a mineral, a random number pieces of ore will be added to their inventory
        # If player runs out of turns, they will be teleported to the town
        # If player step on the 'T' square at (0, 0), they will be teleported to the town
        # All in if/elif statements of w a s d
        if choice == 'w':
            if player['y'] > 0:
                player['y'] -= 1
                player['steps'] += 1
                player['turns'] -= 1
                cell = game_map[player['y']][player['x']]
                if cell == 'C' and player['pickaxe'] >= 1:
                    pieces = randint(1, 3)  # Random number of pieces of copper ore
                    player['copper'] += pieces
                    print(f"You mined {pieces} pieces of copper ore!")
                elif cell == 'S'and player['pickaxe'] >= 2:
                    pieces = randint(1, 2)  # Random number of pieces of silver ore
                    player['silver'] += pieces
                    print(f"You mined {pieces} pieces of silver ore!")
                elif cell == 'G' and player['pickaxe'] >= 3:
                    pieces = randint(1, 1)  # Random number of pieces of gold ore
                    player['gold'] += pieces
                    print(f"You mined {pieces} pieces of gold ore!")
                elif cell == 'T':
                    print("You stepped on the teleport square! You are being teleported to Sundrop Town!")
                    player['turns'] = TURNS_PER_DAY # Reset turns for the next day
                    player['day'] += 1
                    return 'town'
                else:
                    print("You moved north.")  
            else:
                print("You can't move north, you are at the top of the mine.")

        elif choice == 'a':
            if player['x'] > 0:
                player['x'] -= 1
                player['steps'] += 1
                player['turns'] -= 1
                if game_map[player['y']][player['x']] == 'C':
                    pieces = randint(1, 3)  # Random number of pieces of copper ore
                    player['copper'] += pieces
                    print(f"You mined {pieces} pieces of copper ore!")  
                elif game_map[player['y']][player['x']] == 'S':
                    pieces = randint(1, 2)  # Random number of pieces of silver ore
                    player['silver'] += pieces
                    print(f"You mined {pieces} pieces of silver ore!")
                elif game_map[player['y']][player['x']] == 'G':
                    pieces = randint(1, 1)  # Random number of pieces of gold ore
                    player['gold'] += pieces
                    print(f"You mined {pieces} pieces of gold ore!")
                elif game_map[player['y']][player['x']] == 'T':
                    print("You stepped on the teleport square! You are being teleported to Sundrop Town!")
                    player['turns'] = TURNS_PER_DAY # Reset turns for the next day
                    player['day'] += 1
                    return 'town'
                else:
                    print("You moved west.")    
            else:
                print("You can't move west, you are at the left edge of the mine.") 
        
        elif choice == 's':
            if player['y'] < MAP_HEIGHT - 1:
                player['y'] += 1
                player['steps'] += 1
                player['turns'] -= 1
                if game_map[player['y']][player['x']] == 'C':
                    pieces = randint(1, 3)  # Random number of pieces of copper ore
                    player['copper'] += pieces
                    print(f"You mined {pieces} pieces of copper ore!")
                elif game_map[player['y']][player['x']] == 'S':
                    pieces = randint(1, 2)  # Random number of pieces of silver ore
                    player['silver'] += pieces
                    print(f"You mined {pieces} pieces of silver ore!")
                elif game_map[player['y']][player['x']] == 'G':
                    pieces = randint(1, 1)
                    player['gold'] += pieces
                    print(f"You mined {pieces} pieces of gold ore!")
                elif game_map[player['y']][player['x']] == 'T':
                    print("You stepped on the teleport square! You are being teleported to Sundrop Town!")
                    player['turns'] = TURNS_PER_DAY
                    player['day'] += 1
                    return 'town'
                else:
                    print("You moved south.")
            else:
                print("You can't move south, you are at the bottom of the mine.")

        elif choice == 'd':
            if player['x'] < MAP_WIDTH - 1:
                player['x'] += 1
                player['steps'] += 1
                player['turns'] -= 1
                if game_map[player['y']][player['x']] == 'C':
                    pieces = randint(1, 3)  # Random number of pieces of copper ore
                    player['copper'] += pieces
                    print(f"You mined {pieces} pieces of copper ore!")
                elif game_map[player['y']][player['x']] == 'S':
                    pieces = randint(1, 2)  # Random number of pieces of silver ore
                    player['silver'] += pieces
                    print(f"You mined {pieces} pieces of silver ore!")
                elif game_map[player['y']][player['x']] == 'G':
                    pieces = randint(1, 1)  # Random number of pieces of gold ore
                    player['gold'] += pieces
                    print(f"You mined {pieces} pieces of gold ore!")                 
                elif game_map[player['y']][player['x']] == 'T':
                    print("You stepped on the teleport square! You are being teleported to Sundrop Town!")
                    player['turns'] = TURNS_PER_DAY # Reset turns for the next day
                    player['day'] += 1
                    return 'town'       
                else:
                    print("You moved east.")
            else:
                print("You can't move east, you are at the right edge of the mine.")    

        # Map, Information, Portal, Quit
        elif choice == 'm':
            draw_map(game_map, fog, player)

        elif choice == 'i':
            show_information(player)

        elif choice == 'p': # Set the portal's coordinates to the player's current location and then return to the town menu
            player['portalx'] = player['x']
            player['portaly'] = player['y']
            print(f"Portal set to ({player['portalx']}, {player['portaly']}).")
            print("You have been teleported to Sundrop Town!")
            player['turns'] = TURNS_PER_DAY # Reset turns for the next day
            player['day'] += 1
            return 'town'

        elif choice == 'q':
            return 'main' # This will return to the main menu
        
        # For invalid input
        else:
            print("Error. Please enter a valid choice.")
            continue
       
# Main game loop :D
# Must have values for game_state, game_map, fog, and player else the game will break
while True: 
    if game_state == 'main':
        game_state = handle_main_menu() #this will return to the main menu after loading , same for the rest

    elif game_state == 'town':
        game_state = handle_town_menu()

    elif game_state == 'in_mine':
        game_state = handle_mine_menu()

    elif game_state == 'buy':
        game_state = handle_buy_menu()

    elif game_state == 'quit':
        print("Thank you for playing Sundrop Caves!")
        break
