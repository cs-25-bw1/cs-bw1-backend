# Generate rooms in a random pattern on a grid.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

from adventure.models import Room
import random

def create_title(random):
    titles = ([
[
"Cloudy", "Dusty", "Warm", "Crumbling", "Dank", "Musty", "Moldy", "Funerial", "Dread", "Lost", "Black", "Dark", "Grand", "Narrow", "Lost", "Forsaken", "Gauntlet", "Mighty", "Tormented", "Demented", "Brick", "Rusty", "Decaying", "Reeking"
],
[
"Great Room", "Alter", "Hallway", "Chamber", "Cavern", "Expanse", "Overlook", "Foyer", "Library", "Laboratory", "Crypt", "Catacombs", "Archway", "Shrine", "Sanctum", "Lair", "Temple", "Halls", "Cave", "Divide", "Quicksand", "Realm"
],
[
"Death", "Annihiliation", "Torture", "Tranquility", "Secrets", "Chaos", "Desecration", "Blood", "Destruction", "Despair", "Ascendance", "Mortality"
]
])

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


def random_items(random):
    import json
    items = (['candle', 'compass', 'quill', 'ink', 'scroll', 'note', 'book', 'matches', 'toad', 'llama', 'broken glass', 'beanie'])

    # Select a random number from 1 to 5.
    num = random.randint(0, 5)
    # Select a sample of items from the list.
    item_list = random.sample(items, num)
    item_list = json.dumps(item_list)

    return item_list


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0


    def generate_rooms(self, size_x, size_y, num_rooms, Room, create_title, random_items):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''
        import random

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        list_of_rooms = []

        # create a starting room at origin
        room = Room()
        room.title = create_title(random)
        room.items = random_items(random)
        room.save()
        room.x = size_x // 2
        room.y = size_y // 2
        number_rooms_created = 1
        self.grid[room.x][room.y] = room
        list_of_rooms.append(room)
        # until we have enough rooms
        while number_rooms_created < num_rooms:
            # pick an existing room
            current_room = random.choice(list_of_rooms)
            x = current_room.x
            y = current_room.y
            # find the viable paths
            # start with all four directions as options
            options = ['n', 's', 'e', 'w']
            # for room.x: if x == 0, no west; if x == size_x - 1, no east
            if current_room.x == 0:
                options.remove('w')
            if current_room.x == size_x - 1:
                options.remove('e')
            # for room.y: if y == 0, no south; if y == size_y - 1, no north
            if current_room.y == 0:
                options.remove('s')
            if current_room.y == size_y - 1:
                options.remove('n')
            # for the directions remaining check if space is open - remove from list if not open
            # if west: check self.grid[x-1][y] -> if not None, remove west
            if 'w' in options and self.grid[x-1][y]is not None:
                options.remove('w')
            # if east: check self.grid[x+1][y] -> if not None, remove east
            if 'e' in options and self.grid[x+1][y] is not None:
                options.remove('e')
            # if south: check self.grid[x][y-1] -> if not None, remove south
            if 's' in options and self.grid[x][y-1]is not None:
                options.remove('s')
            # if north: check self.grid[x][y+1] -> if not None, remove north
            if 'n' in options and self.grid[x][y+1]is not None:
                options.remove('n')

            # if zero paths, continue
            if len(options) == 0:
                continue
            # choose one or more paths
            num_options = random.randint(1, len(options))
            # create a new room for each path, including x and y positions
            for _ in range(num_options):
                direction = random.choice(options)
                options.remove(direction)
                new_room = Room()
                new_room.title = create_title(random)
                new_room.items = random_items(random)
                new_room.save()
                number_rooms_created += 1
                if direction == 'w':
                    new_room.x = x - 1
                    new_room.y = y
                if direction == 'e':
                    new_room.x = x + 1
                    new_room.y = y
                if direction == 's':
                    new_room.x = x
                    new_room.y = y + 1
                if direction == 'n':
                    new_room.x = x
                    new_room.y = y - 1
                # update grid and list of rooms
                self.grid[new_room.x][new_room.y] = new_room
                list_of_rooms.append(new_room)
                # create connections for each pair of rooms
                # get connecting room
                reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
                reverse_dir = reverse_dirs[direction]
                current_room.connectRooms(new_room, direction)
                new_room.connectRooms(current_room, reverse_dir)

            # remove current room to get better pathing
            list_of_rooms.remove(current_room)

    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''
        for row in self.grid:
            for space in row:
                if space is None:
                    print('. ', end='')
                else:
                    print('+ ', end='')
            print()


Room.objects.all().delete()
w = World()
num_rooms = 100
width = 16
height = 16
w.generate_rooms(width, height, num_rooms, Room, create_title, random_items)
w.print_rooms()