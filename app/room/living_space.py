class LivingSpace(object):
    """Class that models living space

    Attributes:
    room_name: name of the room
    living_space_and_occupants: dictionary that stores room_name
    as key and a list of occupants as the value. {room_name: list_of_occupants}
    capacity: maximum capacity of the living space
    """
    living_and_occupants = {}

    def __init__(self, room_name):
        self.room_name = room_name
        self.capacity = 4
