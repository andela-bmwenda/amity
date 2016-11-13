from app.room.office import Office
from app.room.living_space import LivingSpace
# import random


class Room(Office, LivingSpace):
    """Room class that models rooms in amity

    Attributes:
    name: name of the room

    Methods:
    create_room: creates as many rooms as possible
    print_room: prints names of people in a room
    print_allocations: prints rooms that have been allocated,
    and the names of people in the room.
    """

    def __init__(self):
        pass

    def create_room(self, room_name, room_type):
        """Create a new room"""

        # check if the room_type is allowed, return an error if not
        # check if the room already exists, if yes return an error
        # if not check room to dictionary of room_type as the key and set
        # the value as an empty list
        pass

    def print_room(self, room_name):
        """Print names of all people in room_name"""

        # check if the room_name exists. if not return an error
        # if yes get room details from the respective room types
        # print names of the people in the room.
        pass

    def print_allocations(self):

        # get the dictionary of rooms from living space and office
        # for each item, if a room has occupants,
        # print the key(room_name) and its occupants
        # if a room has no occupants, skip printing
        # format the output as required and print
        pass
