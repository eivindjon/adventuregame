from json import loads, dump
import time
def help():
    print("Available commands:\n'status': Shows character health, potions and equipped weapons\n'equip': Shows available weapons and allows you to equip them\n'heal': Consumes a potion that heals for 30 health")

def read_page(pn:int) -> list:
    with open("game.json") as file:
        data = file.read()
    lst = loads(data)
    print(lst[pn][0])
    return lst[pn][1]

def read_alternatives(page: list) :
    for alternative in page:
        print("(" + alternative[0] + ")", alternative[1])
    
    
    user_choice = choice().upper()
    while True:
        for alternative in page:
            if user_choice == alternative[0]:
                return alternative[2]
        user_choice = choice().upper()

def choice(text = "Select: "):
    character_data = read_character_data()
    user_choice = input(text)
    if user_choice == "status":
        character_status(character_data)
    elif user_choice == "equip":
        equip_character(character_data)
    elif user_choice == "save":
        save_character_data(character_data)
    elif user_choice == "heal":
        drink_potion(character_data)
    elif user_choice == "help":
        help()
    return user_choice

def new_game(character):
    character["last_page_number"] = 0
    character["health"] = 100
    character["potions"] = 0
    character["weapons"]["Sword"] = 0
    character["weapons"]["Bow"] = 0
    character["weapons"]["Dagger"] = 0
    character["weapons"]["Club"] = 0
    character["weapons"]["Rusty sword"] = 0
    character["equipped weapon"] = ""
    save_character_data(character)

def read_character_data():
    with open("save.json") as save_file:
        save_data = save_file.read()
    character_data = loads(save_data)
    return character_data

def save_character_data(character):
    with open("save.json", "w") as save_file:
        save_file.flush()
        dump(character, save_file, indent=4)

def equip_character(character):
    weapons = character["weapons"]
    print("Available weapons: ")
    weapon_count = 0
    for weapon in weapons:
        if weapons[weapon] == 1:
            print("("+ weapon[0] + ")", weapon)
            weapon_count += 1
    if weapon_count == 0:
        print("No weapons available")
        return
    weapon_equipped = False
    while not weapon_equipped:
        selection = choice("What weapon would you like to equip? ").upper()
        for weapon in weapons:
            if selection == weapon[0]:
                character["equipped weapon"] = weapon
                print("Equipped weapon: " + weapon)
                save_character_data(character)
                return
    
def drink_potion(character):
    if character["potions"] >= 1:
        if character["health"] > 99:
            print("Already at full health")
            print("Health", character["health"])
            save_character_data(character)
            return
        elif character["health"] > 70:
            character["health"] = 100
            character["potions"] -= 1
            print("Health", character["health"])
            save_character_data(character)
            return
        else:
            character["health"] += 30
            character["potions"] -= 1
            print("Health", character["health"])
            save_character_data(character)
            return
    else:
        print("You have no potions left")
        save_character_data(character)
        return
    
def character_status(character):
    health = ["Health: ", str(character["health"])]
    potions = ["Potions: ", str(character["potions"])]
    eq_weapons = ["Equipped weapon: ", str(character["equipped weapon"])]
    status = [health, potions, eq_weapons]
    print("Character status: ")
    print("-"*40)
    for s in status:
        print("%-20s %s" % (s[0], s[1]))
        print("-"*40)


def main():
    #Initialize:
    character_data = read_character_data()
    page_number  = character_data["last_page_number"]
    start_game = False
    while not start_game:
        new_game_choice = str(choice("(N) New game\n(L) Load game\nSelect: ").upper())
        if new_game_choice == "N":
            new_game(character_data)
            start_game = True
        elif new_game_choice == "L":
            loading_string = "#####LOADING#####\n"
            for c in loading_string:
                print(c, end='')
                time.sleep(0.1)
            start_game = True

    help()
    while page_number >= 0:
        page_number = read_alternatives(read_page(page_number))
        if not page_number == -1:
            character_data["last_page_number"] = page_number
            save_character_data(character_data)

main()