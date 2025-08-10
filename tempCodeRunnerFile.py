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
def load_map(level1, map_struct):
    map_file = open(level1, 'r')
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
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    # Clear the fog around the player
    for y in range(max(0, player['y'] - 1), min(MAP_HEIGHT, player['y'] + 2)):
        for x in range(max(0, player['x'] - 1), min(MAP_WIDTH, player['x'] + 2)):
            fog[y][x] = ' '
    return

# This function initializes the fog of war
    # TODO: initialize fog
def initialize_fog(fog, width, height):
    for y in range(height):
        row = []
        for x in range(width):
            row.append('?') # representing fog
        fog.append(row)

# This function initializes the game state
def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    initialize_fog(fog, MAP_WIDTH, MAP_HEIGHT)

    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
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
    player['mineral'] = player['copper'] + player['silver'] + player['gold'] # Total mineral count

    clear_fog(fog, player) # Clear the fog around the player at the start of the game
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    return

# This function shows the information for the player
def show_information(player):
    print()
    print("----- Player Information -----")
    print(f"Name: {player['name']}")
    print(f"Portal position: ({player['x']}, {player['y']})")
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
    print(f"(P)ickaxe upgrade to Level {player['pickaxe_level'] + 1} to mine {minerals} ore for 150 GP")
    print(f"(B)ackpack upgrade to carry {player['backpack']} items for {player['backpack_price']} GP")
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


#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!  
#Below are the functions that handle the different game states

# This function handles the main menu
def handle_main_menu():
    show_main_menu()
    choice = input("Your choice? ").strip().lower()
    if choice == 'n':
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
    #sell the ores
    total_gp_earned = 0
    for mineral in minerals:
        if player['mineral']> 0:
            min_price, max_price = prices[mineral]
            gp_earned = randint(min_price, max_price) * player[mineral]
            total_gp_earned += gp_earned
            print(f"You sold {player[mineral]} {mineral} ore for {gp_earned} GP.")
            player[mineral] = 0
    
    if total_gp_earned > 0:
        player['GP'] += total_gp_earned
        print(f"You earned a total of {total_gp_earned} GP from selling your ores.")
           
    # Check if player has enough GP to win
    if player['GP'] >= WIN_GP:
        print(f"Congratulations, {player['name']}! You have earned {player['GP']} GP and won the game!")
        return 'quit'

    print()
    show_town_menu()
    choice = input("Your choice? ").strip().lower()
    if choice == 'b':
        return 'buy'
    elif choice == 'i':
        show_information(player)
    elif choice == 'm':
        draw_map(game_map, fog, player)
    elif choice == 'e':
        print("You enter the mine, ready to start your adventure.")
        return 'in_mine'
    elif choice == 'v':
        save_game(game_map, fog, player)
        print("Game saved successfully.")
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

    elif game_state == 'load':
        load_game(game_map, fog, player)
        print("Game Loaded.")
        game_state = 'town'