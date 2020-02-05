# Make a nested array representing the map
import json
from adventure.models import Room, Map

def make_map(Map, Room, json):
    # create an empty matrix
    grid = [None] * 25
    width = 25
    height = 25
    for i in range( len(grid) ):
        grid[i] = [None] * 25


    # get the rooms in the db to iterate over
    dungeon = list(Room.objects.values())
    # for each room, add it to the correct position
    for room in dungeon:
        grid[room['x']][room['y']] = room

    # store the matrix as string in the db
    dungeon_map = json.dumps(grid)
    new_map = Map()
    new_map.map_string = dungeon_map
    new_map.save()

Map.objects.all().delete()
make_map(Map, Room, json)