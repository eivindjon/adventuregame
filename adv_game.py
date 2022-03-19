from json import loads, dump
from logging import critical
from re import L
import time
import random
from math import floor

def h()->None:
    """
    Prints available commands
    """
    print("Available commands:\n'status': Shows character health, potions and equipped weapons\n'equip': Shows available weapons and allows you to equip them\n'heal': Consumes a potion that heals for 30 health\n'h': Show this message again")

def read_page(pn:int) -> list:
    """Reads content of the page

    Args:
        pn (int): page number.

    Returns:
        list: List of list of alternatives
    """
    with open("game.json") as file:
        data = file.read()
    lst = loads(data)
    print(lst[pn][0])
    return lst[pn][1]

def read_alternatives(page: list) -> None:
    """Reads alternatives from list within page

    Args:
        page (list): list of alternatives
    """
    for alternative in page:
        print("(" + alternative[0] + ")", alternative[1])
    
    
    user_choice = choice().upper()
    while True:
        for alternative in page:
            if user_choice == alternative[0]:
                return alternative[2]
        user_choice = choice().upper()
def visited_before(page:int)->bool:
    """Check if user has visited page in story before. To prevent item duplication.

    Args:
        page (int): which page in story to check.

    Returns:
        bool: True if user has visited page in story before. False otherwise.
    """
    save = read_character_data()
    if page in save["pages_visited"]:
        return True
    else:
        return False

def choice(text = "Select: ") -> None:
    """Takes input from user and calls appropriate functions

    Args:
        text (str, optional):. Defaults to "Select: ".
    """
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
    elif user_choice == "h":
        h()
    elif user_choice == "p":
        if character_data["last_page_number"] == 2 and not visited_before(3):
            character_data = read_character_data()
            character_data["weapons"]["Rusty sword (+30dmg)"] = 1
            save_character_data(character_data)
    elif user_choice == "f":
        if character_data["last_page_number"] == 1:
            fight = fight_scenario(character_data,"Ogre", 100)
            character_data=read_character_data()
            if fight == -1:
                return "Q"
    elif user_choice == "o":
        if character_data["last_page_number"] == 4 and not visited_before(5):
            character_data["weapons"]["Sword (+50dmg)"] = 1
            character_data["potions"] += 2
            save_character_data(character_data)
    return user_choice

def new_game(character) -> None:
    """Resets all character data to default values

    Args:
        character (dict): Contains info about character.
    """
    character["last_page_number"] = 0
    character["health"] = 100
    character["potions"] = 0
    character["weapons"]["Sword (+50dmg)"] = 0
    character["weapons"]["Bow"] = 0
    character["weapons"]["Dagger"] = 0
    character["weapons"]["Club"] = 0
    character["weapons"]["Rusty sword (+30dmg)"] = 0
    character["equipped weapon"] = ""
    character["pages_visited"] = []
    save_character_data(character)

def read_character_data()-> dict:
    """Reads from save file and returns character data

    Returns:
        dict: dictionary with character data
    """
    with open("save.json") as save_file:
        save_data = save_file.read()
    character_data = loads(save_data)
    return character_data

def save_character_data(character)-> None:
    """Saves character data to file

    Args:
        character (dict): character info
    """
    with open("save.json", "w") as save_file:
        save_file.truncate()
        dump(character, save_file, indent=4)

def equip_character(character)-> None:
    """Equips weapons to character

    Args:
        character (dict): current character info
    """
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

def fight_scenario(character, enemy:str, enemy_health):
    health = character["health"]
    def attack(weapon, entity):
        if weapon == "":
            weapon = "Unarmed"
        weapon_damage = {
        "Sword (+50dmg)": 50,
        "Bow": 10,
        "Dagger": 15,
        "Club": 45,
        "Rusty sword (+30dmg)": 30,
        "Unarmed": 1
        }
        entities = {
            "Ogre": 10,
            "Elf": 72,
            "Troll": 50
        }
        critical = random.randint(0, 1)
        if entity == "self":
            damage = weapon_damage[weapon]
            if critical:
                damage = floor(damage * 1.4)
                print("You hit for", damage, "(Critical!)")
                time.sleep(1)
                return damage
            else:
                print("You hit for", damage)
                time.sleep(1)
                return damage

        else:
            damage = entities[entity]
            if critical:
                damage = floor(damage * 1.4)
                print("Critical hit!")
                print("Enemy hit you for", damage, "(Critical!)")
                time.sleep(1)
                return damage
            else:
                print("Enemy hit you for", damage)
                time.sleep(1)
                return damage
            

    while not(character["health"] < 0 or enemy_health < 0):
        print(enemy + " health:", enemy_health)
        print("-"*30)
        print("Your health:", character["health"])
        print("-"*30)
        if character["equipped weapon"] != "":
            user_action = input("Choose action:\n(A) Attack with: " + character["equipped weapon"] + "\n(D) Drink potion\nSelect: ").upper()
        else:
            user_action = input("Choose action:\n(A) Attack with: " + "Unarmed (+1dmg)" + "\n(D) Drink potion\nSelect: ").upper()
        if user_action == "D":
            drink_potion(character)
        else:
            #Your attack
            enemy_health -= attack(character["equipped weapon"], "self")
            #Enemy attack
            character["health"] -= attack("Ogre", enemy)
    if character["health"] > 0:
        print("You have slain " + enemy)
        save_character_data(character)
        return
    else:
        print("You have died..")
        new_game(character)
        character["health"] = -1
        time.sleep(0.2)
        loading_string = "#####GAME OVER#####\n"
        for c in loading_string:
                print(c, end='')
                time.sleep(0.1)
        return -1

def drink_potion(character)-> None:
    """Uses potions to heal a character.

    Args:
        character (dict): current character data
    """
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
    
def character_status(character)-> None:
    """Shows current health, potions and equipped weapons.

    Args:
        character (dict): current character info
    """

    health = ["Health: ", str(character["health"])]
    potions = ["Potions: ", str(character["potions"])]
    eq_weapons = ["Equipped weapon: ", str(character["equipped weapon"])]
    status = [health, potions, eq_weapons]
    print("Character status: ")
    print("-"*40)
    for s in status:
        print("%-20s %s" % (s[0], s[1]))
        print("-"*40)


def main()-> None:
    """Main game loop
    """
    #Initialize:
    character_data = read_character_data()
    page_number  = character_data["last_page_number"]
    start_game = False
    while not start_game:
        new_game_choice = str(choice("(N) New game\n(L) Load game\nSelect: ").upper())
        if new_game_choice == "N":
            new_game(character_data)
            character_data = read_character_data()
            page_number = character_data["last_page_number"] 
            start_game = True
        elif new_game_choice == "L":
            loading_string = "#####LOADING#####\n"
            for c in loading_string:
                print(c, end='')
                time.sleep(0.1)
            start_game = True

    h()
    while page_number >= 0:
        page_number = read_alternatives(read_page(page_number))
        if not page_number == -1:
            character_data = read_character_data()
            character_data["last_page_number"] = page_number
            character_data["pages_visited"].append(page_number)
            save_character_data(character_data)
        character_data = read_character_data()
        if character_data["health"] < 0:
            page_number = 0

main()
