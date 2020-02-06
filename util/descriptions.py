import random

titles = [
[
"Cloudy", "Dusty", "Warm", "Crumbling", "Dank", "Musty", "Moldy", "Funerial", "Dread", "Lost", "Black", "Dark", "Grand", "Narrow", "Lost", "Forsaken", "Gauntlet", "Mighty", "Tormented", "Demented", "Brick", "Rusty", "Decaying", "Reeking"
],
[
"Great Room", "Alter", "Hallway", "Chamber", "Cavern", "Expanse", "Overlook", "Foyer", "Library", "Laboratory", "Crypt", "Catacombs", "Archway", "Shrine", "Sanctum", "Lair", "Temple", "Halls", "Cave", "Divide", "Quicksand", "Realm"
],
[
"Death", "Annihiliation", "Torture", "Tranquility", "Secrets", "Chaos", "Desecration", "Blood", "Destruction", "Despair", "Ascendance", "Mortality"
]
]


def create_title():
    title = ""
    for i in range(3):
        if i == 0:
            first_word = random.choice(titles[i])
            title += first_word
        elif i == 1:
            second_word = random.choice(titles[i])
            title += " " + second_word + " of"
        else:
            third_word = random.choice(titles[i])
            title += " " + third_word
    return title



# You'll see any of these items in a room.

items = ['candle', 'compass', 'quill', 'ink', 'scroll', 'note', 'book', 'matches', 'toad', 'llama', 'broken glass', 'beanie']



def random_items():
    # Select a random number from 1 to 5.
    num = random.randint(0, 5)
    # Select a sample of items from the list.
    item_list = random.sample(items, num)

    return item_list
