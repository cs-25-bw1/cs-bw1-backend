# Make a nested array representing the map
import json
from adventure.models import Room, Map

def make_map(Map, Room, json, width=16, height=16):
    # create an empty matrix
    grid = [0] * height
    
    for i in range( height ):
        grid[i] = [0] * width


    # get the rooms in the db to iterate over
    dungeon = list(Room.objects.values())

    # for each room, add it to the correct position
    for room in dungeon:
        exits = [room['n_to'], room['s_to'], room['e_to'], room['w_to']]
        grid[room['x']][room['y']] = exits

    # store the matrix as string in the db
    dungeon_map = json.dumps(grid)
    new_map = Map()
    new_map.map_string = dungeon_map
    new_map.save()

Map.objects.all().delete()
make_map(Map, Room, json)