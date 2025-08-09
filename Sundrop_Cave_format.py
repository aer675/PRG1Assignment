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

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fof
def draw_map(game_map, fog, player):
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    return

# This function shows the information for the player
def show_information(player):
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
    print("(P)ickaxe upgrade to Level 2 to mine silver ore for 50 GP")
    print("(B)ackpack upgrade to carry 12 items for 20 GP")
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP {player['GP']}")

# TODO: The game!  
#Below are the functions that handle the different game states

# This function handles the main menu
def handle_main_menu():
    show_main_menu()
    choice = input("Your choice? ").strip().lower()
    if choice == 'n':
        name = str(input("Greetings, miner! What is your name? "))
        print(f"Pleased to meet you, {name}. Welcome to Sundrop Town!")
        return 'town'
    elif choice == 'l':
        load_game(game_map, fog, player)
        print("Game loaded successfully.")
        return 'town'
    else:
        return 'quit'

# This function handles the town menu
def handle_town_menu():
    print(f"DAY {player['day']}")
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
        return 'main'

#This function handles the mine menu
def handle_mine_menu():

#This function handles the in-mine menu
def handle_in_mine_menu():

# This function handles the buy menu
def handle_buy_menu():


while True:
    if game_state == 'main':
        game_state = handle_main_menu()

    elif game_state == 'town':
        game_state = handle_town_menu()

    elif game_state == 'mine':
        game_state = handle_mine_menu()

    elif game_state == 'in_mine':
        game_state = handle_in_mine_menu()

    elif game_state == 'buy':
        choice = input("Your choice? ").strip().lower()
        game_state = show_buy_menu()

    elif game_state == 'quit':
        print("Thank you for playing Sundrop Caves!")
        break

    elif game_state == 'load':
        load_game(game_map, fog, player)
        print("Game Loaded.")
        game_state = 'town'
    
 

