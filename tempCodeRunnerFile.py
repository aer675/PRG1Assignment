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
pickaxe_price = {2: 50, 3: 150} # Key is the pickaxe level, value is the price to upgrade

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(level_1, map_struct):
    map_file = open('PRG1Assignment\level_1.txt', 'r')
    lines = map_file.readlines()
    global MAP_WIDTH, MAP_HEIGHT
    
    map_struct.clear()
    
    for line in lines:
        line = line.strip()
        if line:
            map_struct.append(list(line))
    
    if map_struct:
        MAP_WIDTH = len(map_struct[0])
        MAP_HEIGHT = len(map_struct)
    else:
        MAP_WIDTH = 0
        MAP_HEIGHT = 0

    map_file.close()

def initialize_fog():
    new_fog = []
    for y in range(MAP_HEIGHT):
        row = ['?'] * MAP_WIDTH
        new_fog.append(row)
    return new_fog

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    for y in range(max(0, player['y'] - 1), min(MAP_HEIGHT, player['y'] + 2)):
        for x in range(max(0, player['x'] - 1), min(MAP_WIDTH, player['x'] + 2)):
            if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                fog[y][x] = game_map[y][x]
    return

# This function initializes the game state
def initialize_game(game_map, fog, player):
    # initialize map
    load_map("PRG1Assignment\level_1.txt", game_map)

    fog.clear()
    fog.extend(initialize_fog())

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
    print("+" + "-" * MAP_WIDTH + "+")
    for y in range(MAP_HEIGHT):
        row = []
        for x in range(MAP_WIDTH):
            if player['x'] == x and player['y'] == y:
                row.append('M')
            elif player['portalx'] == x and player['portaly'] == y:
                row.append('P')
            elif fog[y][x] == '?':
                row.append('?')
            else:
                row.append(game_map[y][x])
        print("|" + "".join(row) + "|")
    print("+" + "-" * MAP_WIDTH + "+")

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    print("+" + "---" + "+")
    for y_offset in range(-1, 2):
        row = "|"
        for x_offset in range(-1, 2):
            y = player['y'] + y_offset
            x = player['x'] + x_offset
            
            if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                if y == player['y'] and x == player['x']:
                    row += "M"
                else:
                    row += fog[y][x]
            else:
                row += "#"
        row += "|"
        print(row)
    print("+" + "---" + "+")

# This function shows the information for the player
def show_information(player):
    print()
    print("----- Player Information -----")
    print(f"Name: {player['name']}")
    if 'portalx' in player and 'portaly' in player:
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
    f = open('savegame.txt', 'w')
    f.write(f"MAP_WIDTH:{MAP_WIDTH}\n")
    f.write(f"MAP_HEIGHT:{MAP_HEIGHT}\n")
    
    for row in game_map:
        f.write(''.join(row) + '\n')
        
    for row in fog:
        f.write(''.join(row) + '\n')
        
    for key, value in player.items():
        f.write(f"{key}:{value}\n")
    
    f.close()
    print("Game saved.")
        
# This function loads the game
def load_game(game_map, fog, player):
    try:
        f = open('savegame.txt', 'r')
        lines = f.readlines()
        f.close()
        
        global MAP_WIDTH, MAP_HEIGHT
        
        MAP_WIDTH = int(lines[0].strip().split(':', 1)[1])
        MAP_HEIGHT = int(lines[1].strip().split(':', 1)[1])
        
        game_map.clear()
        for i in range(2, 2 + MAP_HEIGHT):
            game_map.append(list(lines[i].strip()))
        
        fog.clear()
        for i in range(2 + MAP_HEIGHT, 2 + MAP_HEIGHT * 2):
            fog.append(list(lines[i].strip()))
        
        player.clear()
        for line in lines[2 + MAP_HEIGHT * 2:]:
            if ':' in line:
                key, value = line.strip().split(':', 1)
                if key in ['x', 'y', 'copper', 'silver', 'gold', 'GP', 'day', 'steps', 'turns', 'backpack', 'pickaxe', 'portalx', 'portaly']:
                    player[key] = int(value)
                else:
                    player[key] = value
        
        print("Game loaded.")
        return True
    except (IOError, IndexError, ValueError):
        print("Error: Could not load saved game.")
        return False

#This function shows the main menu
def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    #    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

#This function shows the town menu
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
    if player['pickaxe'] < 3:
        next_pickaxe = player['pickaxe'] + 1
        upgrade_cost = pickaxe_price.get(next_pickaxe, 0)
        next_mineral = minerals[player['pickaxe']]
        print(f"(P)ickaxe upgrade to Level {next_pickaxe} to mine {next_mineral} ore for {upgrade_cost} GP")
    else:
        print("Your pickaxe is already at the highest level.")
    
    bcost = player['backpack'] * 2
    print(f"(B)ackpack upgrade to carry {player['backpack'] + 2} items for {bcost} GP")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP: {player['GP']}")
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

#def this function sell all ores when user is in town
def sell_all_ores():
    total_gp_earned = 0
    sold_any = False

    if player['copper'] > 0:
        copper_gp = randint(prices['copper'][0], prices['copper'][1]) * player['copper']
        player['GP'] += copper_gp
        total_gp_earned += copper_gp
        print(f"You sell {player['copper']} copper ore for {copper_gp} GP.")
        player['copper'] = 0
        sold_any = True
    
    if player['silver'] > 0:
        silver_gp = randint(prices['silver'][0], prices['silver'][1]) * player['silver']
        player['GP'] += silver_gp
        total_gp_earned += silver_gp
        print(f"You sell {player['silver']} silver ore for {silver_gp} GP.")
        player['silver'] = 0
        sold_any = True
    
    if player['gold'] > 0:
        gold_gp = randint(prices['gold'][0], prices['gold'][1]) * player['gold']
        player['GP'] += gold_gp
        total_gp_earned += gold_gp
        print(f"You sell {player['gold']} gold ore for {gold_gp} GP.")
        player['gold'] = 0
        sold_any = True

    if sold_any:
        print(f"You now have {player['GP']} GP!")
           
    if player['GP'] >= WIN_GP:
        print()
        print(f"Woo-hoo! Well done, {player['name']}, you have {player['GP']} GP!")
        print("You now have enough to retire and play video games every day.")
        print(f"And it only took you {player['day']} days and {player['steps']} steps! You win!")
        return 'win'
    
    return 'town'

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
    while True:
        show_main_menu()
        choice = input("Your choice? ").strip().lower()
        if choice == 'n':
            initialize_game(game_map, fog, player)
            name = input("Greetings, miner! What is your name? ")
            player['name'] = name
            print(f"Pleased to meet you, {name}. Welcome to Sundrop Town!")
            return 'town'
        elif choice == 'l':
            if load_game(game_map, fog, player):
                print(f"Welcome back, {player['name']}!")
                return 'town'
            else:
                continue
        elif choice == 'q':
            return 'quit'
        else:
            print('Error. Please enter a valid choice.')

# This function handles the town menu
def handle_town_menu():
    next_state = sell_all_ores()
    if next_state == 'win':
        return 'win'
    
    while True:
        show_town_menu()
        choice = input("Your choice? ").strip().lower()
        if choice == 'b':
            return 'buy'
        elif choice == 'i':
            show_information(player)
            continue
        elif choice == 'm':
            draw_map(game_map, fog, player)
            continue
        elif choice == 'e':
            print("You enter the mine, ready to start your adventure.")
            player['x'] = player['portalx']
            player['y'] = player['portaly']
            clear_fog(fog, player)
            return 'in_mine'
        elif choice == 'v':
            save_game(game_map, fog, player)
            continue
        elif choice == 'q':
            return 'main'
        else:
            print("Invalid input. Please try again.")

# This function handles the buy menu
def handle_buy_menu():
    while True:
        show_buy_menu()
        choice = input("Your choice? ").strip().lower()
        bcost = player['backpack'] * 2
        pcost = pickaxe_price.get(player['pickaxe'] + 1, 0)
        
        if choice == 'p':
            if player['pickaxe'] >= 3:
                print("Your pickaxe is already at the highest level.")
            elif player['GP'] >= pcost:
                player['GP'] -= pcost
                player['pickaxe'] += 1
                next_mineral = minerals[player['pickaxe'] - 1]
                print(f"Congratulations! You can now mine {next_mineral}!")
            else:
                print("Not enough GP to upgrade your pickaxe.")
        
        elif choice == 'b':
            if player['GP'] >= bcost:
                player['GP'] -= bcost
                player['backpack'] += 2
                print(f"Congratulations! You can now carry {player['backpack']} items!")
            else:
                print("Not enough GP to upgrade your backpack.")
        
        elif choice == 'l':
            return 'town'
        
        else:
            print("Error. Please enter a valid choice.")

#Moving in the mines 
def moving_in_mine(dx, dy): 
    new_x = player['x'] + dx
    new_y = player['y'] + dy
    
    player['turns'] -= 1
    
    if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
        print("You can't move that way, you are at the edge of the mine.")
        return 'in_mine'

    current_load = player['copper'] + player['silver'] + player['gold']
    cell = game_map[new_y][new_x]

    if cell == 'T':
        player['x'] = new_x
        player['y'] = new_y
        player['steps'] += 1
        print("You stepped on the teleport square! You are being teleported to Sundrop Town!")
        player['day'] += 1
        player['turns'] = TURNS_PER_DAY
        return 'town'
    
    if cell in mineral_names:
        ore_name = mineral_names[cell]
        can_mine = False
        if ore_name == 'copper' and player['pickaxe'] >= 1:
            can_mine = True
        elif ore_name == 'silver' and player['pickaxe'] >= 2:
            can_mine = True
        elif ore_name == 'gold' and player['pickaxe'] >= 3:
            can_mine = True

        if not can_mine:
            print(f"Your pickaxe is not strong enough to mine {ore_name}.")
            return 'in_mine'
        
        if current_load >= player['backpack']:
            print("Your backpack is full! You can't carry anymore ore.")
            return 'in_mine'
    
    player['x'] = new_x
    player['y'] = new_y
    player['steps'] += 1
    clear_fog(fog, player)
    
    if cell == 'C' and player['pickaxe'] >= 1:
        pieces = randint(1, 5)
        space_left = player['backpack'] - current_load
        mined_pieces = min(pieces, space_left)
        player['copper'] += mined_pieces
        print(f"You mined {mined_pieces} piece(s) of copper.")
        if mined_pieces < pieces:
            print(f"...but you could only carry {mined_pieces} piece(s)!")
        game_map[player['y']][player['x']] = ' '
    
    elif cell == 'S' and player['pickaxe'] >= 2:
        pieces = randint(1, 3)
        space_left = player['backpack'] - current_load
        mined_pieces = min(pieces, space_left)
        player['silver'] += mined_pieces
        print(f"You mined {mined_pieces} piece(s) of silver.")
        if mined_pieces < pieces:
            print(f"...but you could only carry {mined_pieces} piece(s)!")
        game_map[player['y']][player['x']] = ' '
    
    elif cell == 'G' and player['pickaxe'] >= 3:
        pieces = randint(1, 2)
        space_left = player['backpack'] - current_load
        mined_pieces = min(pieces, space_left)
        player['gold'] += mined_pieces
        print(f"You mined {mined_pieces} piece(s) of gold.")
        if mined_pieces < pieces:
            print(f"...but you could only carry {mined_pieces} piece(s)!")
        game_map[player['y']][player['x']] = ' '
        
    return 'in_mine'

# This function handles the mine menu
#BEUHEUICNOINXCDSIJNCIDNDUIDNMKSx
def handle_mine_menu():
    while True:
        show_mine_menu()
        choice = input("Action? ").strip().lower()

        state = 'in_mine'
        if choice == 'w':
            state = moving_in_mine(0, -1)
        elif choice == 'a':
            state = moving_in_mine(-1, 0)
        elif choice == 's':
            state = moving_in_mine(0, 1)
        elif choice == 'd':
            state = moving_in_mine(1, 0)
        elif choice == 'm':
            draw_map(game_map, fog, player)
            continue
        elif choice == 'i':
            show_information(player)
            continue
        elif choice == 'p':
            print("You place your portal stone here and zap back to town.")
            player['portalx'] = player['x']
            player['portaly'] = player['y']
            player['x'] = 0
            player['y'] = 0
            player['day'] += 1
            player['turns'] = TURNS_PER_DAY
            print(f"Portal set to ({player['portalx']}, {player['portaly']}).")
            return 'town'
        elif choice == 'q':
            return 'main'
        else:
            print("Error. Please enter a valid choice.")
            continue
            
        if player['turns'] <= 0 and state == 'in_mine':
            print("You are exhausted.")
            print("You place your portal stone here and zap back to town...")
            player['portalx'] = player['x']
            player['portaly'] = player['y']
            player['x'] = 0
            player['y'] = 0
            player['day'] += 1
            player['turns'] = TURNS_PER_DAY
            print(f"Portal set to ({player['portalx']}, {player['portaly']}).")
            return 'town'
        
        if state == 'town':
            return 'town'
    
# Main game loop :D
# Must have values for game_state, game_map, fog, and player else the game will break
while True: 
    if game_state == 'main':
        game_state = handle_main_menu()
    elif game_state == 'town':
        game_state = handle_town_menu()
    elif game_state == 'in_mine':
        game_state = handle_mine_menu()
    elif game_state == 'buy':
        game_state = handle_buy_menu()
    elif game_state == 'win':
        game_state = 'main'
    elif game_state == 'quit':
        print("Thank you for playing Sundrop Caves!")
        break