import random

from app.person import Fellow, Staff
from app.room import Office, LivingSpace


class Amity(object):
    """Main class for amity app

    Attributes:
    allocated_members: dictionary of people, both fellows and staff
    who have been allocated rooms.
    unallocated_members: dictionary of people, both fellows and staff
    who have not been allocated rooms.

    Methods:
    load_state(): load data from the database into the app
    save_state(sqlite_db): Persist all  data stored in the app to a SQLite database.
    """

    unallocated_members = []
    allocated_members = {}
    list_of_rooms = []

    def __init__(self):
        pass

    def add_person(self, first_name, last_name, role, wants_accomodation='N'):

        # check if person already exists.
        # check that the category is valid.
        # if above checks pass, add person to unallocated_members dictionary.
        # check that there are available rooms. if no, raise alert and break.
        # check that there are available rooms suitable for the person. if no, raise alert.
        # if yes, if person is a fellow and wants_accomodation = 'Y', allocate
        # them a random living space.
        # if there is no available living space, allocate them any available room.
        # if person is staff/wants_accomodation = 'N',
        # allocate them a random office.
        # how to allocate a room:
        # get the room_name(key) from rooms dic. Append person_name to list_of_occupants
        # if member is successfully allocated a room, transfer them
        # from unallocated_members dictionary to allocated_members.
        # Key = person_name, value = room eg {John: Closure}
        # if room allocation is unsuccessful, alert the user.
        # return message:
        # person_name allocated to room_name
        # Create a person instance and their identifier

        if role.upper() == "STAFF":
            person = Staff(first_name, last_name)
        elif role.upper() == "FELLOW":
            person = Fellow(first_name, last_name, wants_accomodation)
        else:
            print("Invalid person role: " + role)
            return

        allocated = False
        while not allocated:
            # Check if there are rooms
            if len(Amity.list_of_rooms):
                # Allocate person a room randomly
                room = random.choice(Amity.list_of_rooms)
                if room.room_type == "Living Space":
                    if room.capacity < 5:
                        room.occupants.append(person)
                        allocated = True
                        break
                elif room.room_type == "Office":
                    if room.capacity < 7:
                        room.occupants.append(person)
                        allocated = True
                        break

            else:
                print("No rooms available")
                break
        if not allocated:
            Amity.unallocated_members.append(person)
            print("{} was added to the waiting list".format(
                person.first_name))
        else:
            print("{} successfully allocated {}".format(
                person.first_name, room.room_name))

    def reallocate_person(self, person_name, new_room_name):

        # check that person and room exist. Raise alert if necessary
        # get the person's current room from allocated_members dictionary
        # call the allocate room function in add_person()
        # if successful, alert the user of the change,
        # eg, you've been reallocated to Java from Swift
        # set the new value of the dic to new_room_name
        # return message:
        # person_name transferred from former_room to new_room
        pass

    def print_unallocated(self):

        # get the dictionary of unallocated_members
        # loop through the dic and print each name
        # save the data to a txt if specified
        pass

    def create_room(self, room_name):
        """Create a new room"""

        # check if the room_type is allowed, return an error if not
        # check if the room already exists, if yes return an error

        r_type = random.choice(["Office", "LivingSpace"])
        if r_type == "Office":
            room = Office(room_name)
        else:
            room = LivingSpace(room_name)
        Amity.list_of_rooms.append(room)
        print("Created {0}: Type is {1}".format(
            room.room_name, room.room_type))

        # print("Total rooms: {}".format(len(Amity.list_of_rooms)))

    def print_room(self, room_name):
        """Print names of all people in room_name"""

        room = [room for room in Amity.list_of_rooms if
                room.room_name.upper() == room_name.upper()]
        if room:
            room = room[0]
            print("{} OCCUPANTS \n".format(room.room_name.upper()))
            print("-----------------------------------------------------")
            for occupant in room.occupants:
                print("\t{0} {1}\n".format(
                    occupant.first_name, occupant.last_name)
                )
        else:
            print("{} does not exist in Amity".format(room_name))
            return

    def print_allocations(self):

        # get the dictionary of rooms from living space and office
        # for each item, if a room has occupants,
        # print the key(room_name) and its occupants
        # if a room has no occupants, skip printing
        # format the output as required and print
        for room in Amity.list_of_rooms:
            print(room.room_name.upper() + '\n')
            print("-----------------------------------------------------")
            for occupant in room.occupants:
                print((occupant.first_name + " " +
                       occupant.last_name + '\t'), end=" ")
            print('\n')

    def load_people(self, path):

        # check that file path is valid and file exists
        # check that the format is valid , ie
        # Two names, category, want_room(optional)
        # raise alert if this is not the case
        # else, load the file
        # for each name in file, call add_person()
        # return a summary of the process
        # eg successful allocations and unsuccessful allocations
        pass

    def load_state(self):

        # connect to db
        # load rooms, person and amity data
        pass

    def save_state(self, sqlite_db):

        # check that the sqlite db exists
        # create connection
        # save current data, ie
        # rooms data(livingspace_and_accupants, office_and_occupants)
        # person_data()
        pass


if __name__ == '__main__':
    Amity.create_room("Go", "Swift", "Krypton", "Oculus", "Valhala")
    Amity.add_person("self", "John", "Doe", "Fellow", 'Y')
    Amity.add_person("self", "Mary", "Jane", "Staff", 'N')
