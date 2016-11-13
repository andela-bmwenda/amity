class Office(object):
    """Class that models an office

    Attributes:
    room_name: name of the room
    capacity: maximum capacity of the room
    office_and_occupants: a dictionary that stores room as
    the key and a list of occupants as the value.
    office_and_occupants = {room_name: list_of_occupants}
    """

    office_and_occupants = {}

    def __init__(self, room_name):
        self.room_name = room_name
        self.capacity = 6
