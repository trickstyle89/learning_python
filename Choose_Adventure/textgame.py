import time

race_names = {1: "Human", 2: "Elf", 3: "Orc"}
class_names = {1: "Warrior", 2: "Mage", 3: "Healer"}

# room is the key for dungeon_rooms, room_descriptions and level_complete
room = None

dungeon_rooms = {
  1: "Training Room",
  2: "Slime Room",
  3: "Chimera Room",
  4: "Demon Room"
}

room_descriptions = {
  1: """You are standing in the knight's training chambers.
In front of you lies your master-at-arms.""",

  2: """You enter the room. You can barely make out anything
from this dark area. However, you see a glowing blue light
straight ahead of you.

The light burns greater... it begins to make the shape of a
creature... a slime!""",

  3: """As you proceed into the room, you hear eerie noises from
all across the room, followed by a dark shape that moves too fast
for you to catch. You stand in the middle of the round room, you
hear a loud growl behind you.

You turn around to fight a lion, no...
It's a two-headed creature, both a lion and a giant serpent.""",

  4: """As you step into the room, you find it hard to stand, as
if an unknown force is pushing your body down into the ground. You
start shaking, your teeth grinding.

It takes you a moment, but you are finally able to regain control of
your body. Already tired from your previous trials, you push ahead
and find an empty throne.

You blink and all of a sudden there is a dark figure sitting on the
chair. He, no... It smiles and stands up, then walks toward you...
This is your final challenge."""
}

level_complete = {
  1: """After several excruciating blows, your sparring session is over.
Your teacher guides you to the gate where your first true challenge
begins to become a full-pledged knight.""",

  2: """You fight it off and you (surprisingly) beat your first real enemy.

Behind the gooey carcass of the now-defeated slime lies another room
with the doorknob of a lion""",

  3: """You fight it off and you barely beat this vicious creature.
You reach the edge of the room to find a dark door.
Red mist flows through the gaps of the door.

Do you proceed? This may be your final choice""",

  4: """With great struggle, you defeat your final challenge.
Now you are ready to become a full-fledged knight."""
}

class Monster:
    def __init__(self):
        self.health = 100
        self.attack = 20

class Hero:
    def __init__(self, name, race, class_int):
        self.name = name
        self.race = race
        self.class_int = class_int
        # FIXTHIS - should make health and attack depend on race and class
        self.health = 100
        self.attack = 50

    # FIXTHIS - could have functions for healing, agility, defense, etc
    # that depend on race and class, and are used for encounters

hero = None

def create_hero():
    global hero

    print("What is your name?")
    hero_name = input("My name is: ")

    print("Choose a race")
    print("1- Human\t\t2- Elf\t\t3- Orc")
    race_choice = int(input("My race is: "))

    print("Choose a class.")
    print("1- Warrior\t\t2- Mage\t\t3- Healer")
    class_choice = int(input("My class is: "))

    hero = Hero(hero_name, race_choice, class_choice)
    return


def save_game():
    global hero
    global room

    game_data = "%s&%s&%s&%s&%s" % (hero.name, hero.race, hero.class_int,
                  hero.health, room)

    f = open("knight-data.txt", "w")
    f.writelines(game_data)
    f.close()


# returns 1 on error
def load_game():
    global hero
    global room

    try:
        f = open("knight-data.txt", "r")
        line = f.readline()
        f.close()
    except FileNotFoundError:
        print('Error reading save file ("knight-data.txt").')
        return None

    game_data = str.split(line, "&")

    hero_name = game_data[0]
    race_int = int(game_data[1])
    class_int = int(game_data[2])
    hero_health = int(game_data[3])
    room = int(game_data[4])

    hero = Hero(hero_name, race_int, class_int)
    hero.health = hero_health
    return 0


def status():
    global hero
    print("Welcome back %s the %s %s, you have %s health" % \
            (hero.name, race_names[hero.race],
            class_names[hero.class_int], hero.health))
    return


def encounter():
    global hero
    global room

    if room < 5:
        print("You are in the: == %s ==\n" % dungeon_rooms[room])

        print(room_descriptions[room])
        battle()
        if hero.health <= 0:
            print("You died!")
        else:
            print(level_complete[room])
    return


# returns "exit" if the user selected 'Exit'
def get_input():
    global hero
    global room
    while 1:
        print("1- Proceed\t2- Status\t3- Save\t4- Exit")
        input_choice = int(input("What should I do?... "))
        if input_choice == 1:
            room += 1
            return "proceed"
        elif input_choice == 2:
            status()
        elif input_choice == 3:
            save_game()
        elif input_choice == 4:
            return "exit"


def battle():
    global hero

    monster = Monster()
    print("++++++++++++++\nPrepare to battle!\n...")
    time.sleep(3)
    while monster.health > 0 and hero.health > 0:
        print("  Prepare for monster attack! ....")
        time.sleep(2)
        print("    Monster attacks you for {} damage".format(monster.attack))
        hero.health -= monster.attack
        print("    You have {} health remaining".format(hero.health))
        time.sleep(1)
        print("  Your turn to fight back!\n...")
        time.sleep(2)
        print("    You attack the monster for {} damage!".format(hero.attack))
        monster.health -= hero.attack
        print("    Monster has only {} health remaining".format(monster.health))


def main():
    global room

    while 1:
        print("1- New Game\n2- Load Game\n3- Exit")
        start_choice = int(input())

        if start_choice == 3:
            print("See you next time...")
            break

        if start_choice == 1:
            create_hero()
            room = 1
            while room < 5:
                encounter()
                if hero.health <= 0:
                    print("Better luck next time!")
                    return
                if get_input() == "exit":
                    break
            print("To be continued.")
            break

        elif start_choice == 2:
            # if there is no save file, load_game returns None
            load_game()
            if not hero:
                continue
            while room < 5:
                if get_input() == "exit":
                    break
                encounter()
                if hero.health <= 0:
                    print("Better luck next time!")
                    return
            print("To be continued.")
            break

        else:
            print("Please enter 1, 2, or 3")

if __name__ == "__main__":
    main()