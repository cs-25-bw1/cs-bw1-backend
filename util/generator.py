# Sample Python code that can be used to generate rooms in
# a zig-zag pattern.
#
# You can modify generate_rooms() to create your own
# procedural generation algorithm and use print_rooms()
# to see the world.

from adventure.models import Room

class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0


    def generate_rooms(self, size_x, size_y, num_rooms, Room):
        '''
        Fill up the grid, bottom to top, in a zig-zag pattern
        '''

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range( len(self.grid) ):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1 # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west


        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction
            room = Room(title="A Generic Room", description="This is a generic room.")
            # Note that in Django, you'll need to save the room after you create it
            room.save()

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            if previous_room is not None:
                reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
                reverse_dir = reverse_dirs[room_direction]
                previous_room.connectRooms(room, room_direction)
                room.connectRooms(previous_room, reverse_dir)

            # Update iteration variables
            previous_room = room
            room_count += 1

Room.objects.all().delete()
w = World()
num_rooms = 44
width = 8
height = 7
w.generate_rooms(width, height, num_rooms, Room)