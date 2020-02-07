from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    location = {'x': room.x, 'y': room.y}
    items = json.loads(room.items)
    players = room.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'items': items, 'location': location}, safe=True)

@csrf_exempt
@api_view(["GET"])
def rooms(request):
    # rooms = list(Map.objects.values())
    # array = json.loads(rooms[0]['map_string'])
    # return JsonResponse(array, safe=False)
    world = {}
    rooms = Room.objects.all()
    for room in rooms:

        exits = {}
        if room.n_to != 0:
            exits['n'] = room.n_to
        if room.s_to != 0:
            exits['s'] = room.s_to
        if room.e_to != 0:
            exits['e'] = room.e_to
        if room.w_to != 0:
            exits['w'] = room.w_to


        items = json.loads(room.items)
        
    # array = json.loads(rooms[0]['map_string'])
    # return JsonResponse(array, safe=False)

        # items = []
        # if int(room.id) % 2 == 0:
        #     items.append('candle')
        # if int(room.id) % 5 == 0:
        #     items.append('marble')


        world[room.id] = [{"x": room.x,"y": room.y}, exits, {'title': room.title}, {'description': room.description}, {'items': items}]
    return JsonResponse(world, safe=True)

# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    items = json.loads(room.items)
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        new_items = json.loads(nextRoom.items)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({"x": nextRoom.x,"y": nextRoom.y, 'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, "items": new_items, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'x': room.x, 'y': room.y, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, "items": items, 'error_msg':"You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)
