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
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog
    
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['backpack'] = 10 # Game start with 10 item capacity
    player['backpack_price'] = 1 # Price of the backpack upgrade
    player['pickaxe'] = 1 # Game starts with pickaxe level 1
    player['pickaxe_level'] = 1 # Game starts with pickaxe level 1
    player['pickaxe_price'] = pickaxe_price[player['pickaxe'] - 1] # Price of the pickaxe upgrade


    clear_fog(fog, player)
    
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
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
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
            
#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

#This function shows the buy menu
def show_buy_menu():
    print()
    print("----------------------- Shop Menu -------------------------")
    print(f"(P)ickaxe upgrade to Level {player['pickaxe_level'] + 1} to mine {minerals} ore for {ore price} GP")
    print(f"(B)ackpack upgrade to carry {player['backpack']} items for {player['backpack_price']} GP")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP {player['GP']}")
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
    for mineral in minerals:
        if player['copper'] > 0:
            player['GP'] += randint(prices['copper'][0], prices['copper'][1]) * player['copper']
            print(f"You sold {player['copper']} copper ore for {player['GP']} GP.")
            player['copper'] = 0
        elif player['silver'] > 0:
            player['GP'] += randint(prices['silver'][0], prices['silver'][1]) * player['silver']
            print(f"You sold {player['silver']} silver ore for {player['GP']} GP.")
            player['silver'] = 0
        elif player['gold'] > 0:
            player['GP'] += randint(prices['gold'][0], prices['gold'][1]) * player['gold']
            print(f"You sold {player['gold']} gold ore for {player['GP']} GP.")
            player['gold'] = 0
        print("You have earned some GP from selling your ores.")

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
#BRUHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHh
def handle_buy_menu():
    while True:
        show_buy_menu()
        choice = input("Your choice? ").strip().lower()
        if choice == 'p' and player['GP'] > player['pickaxe_price']:
            player['pickaxe'] += 1
            player['pickaxe_level'] += 1
            player['pickaxe_price'] = pickaxe_price[player['pickaxe'] - 1]
            player['GP'] -= player['pickaxe_price']
            print(f"Congratulations! You can now mine {ore}!")
            continue

        elif choice == 'b'and player['GP'] > player['backpack_price']:
            print(f"Congratulations! You can now carry {player['backpack'] + 2} items!")
            player['backpack'] += 2
            player['GP'] -= player['backpack_price']
            player['backpack_price'] = player['backpack'] * 2
            continue

        elif choice =='l':
            return 'town'
        
        else:
            print("Error. Please enter a valid choice.")
            continue 

#This function handles the mine menu
def handle_mine_menu():

#This function handles the in-mine menu
def handle_in_mine_menu():

       
#Main game loop :D
# Must have values for game_state, game_map, fog, and player else the game will break
while True: 
    if game_state == 'main':
        game_state = handle_main_menu() #this will return to the main menu after loading , same for the rest

    elif game_state == 'town':
        game_state = handle_town_menu()

    elif game_state == 'mine':
        game_state = handle_mine_menu()

    elif game_state == 'in_mine':
        game_state = handle_in_mine_menu()

    elif game_state == 'buy':
        game_state = handle_buy_menu()

    elif game_state == 'quit':
        print("Thank you for playing Sundrop Caves!")
        break

    elif game_state == 'load':
        load_game(game_map, fog, player)
        print("Game Loaded.")
        game_state = 'town'