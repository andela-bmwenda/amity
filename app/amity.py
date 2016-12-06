import random
import os
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
    allocated_members = []
    list_of_rooms = []

    def __init__(self):
        pass

    def add_person(self, person_name, role, wants_accomodation='N'):

        # check that there are available rooms suitable for the person. if no, raise alert.
        # if yes, if person is a fellow and wants_accomodation = 'Y', allocate
        # them a random living space.
        # if there is no available living space, allocate them any available room.
        # if person is staff/wants_accomodation = 'N',
        # allocate them a random office.
        # how to allocate a room:

        person = [
            person for person in Amity.allocated_members
            if person_name.upper() == person.person_name.upper() and
            person.role.upper() == role.upper()
        ]
        if person:
            print("Warning! {0} exists in amity. ID: {1}".format(
                person_name, person[0].identifier)
            )
            ans = input("Is this a different person? y/n\n")
            if ans == 'y':
                pass
            else:
                return
        if role.upper() == "STAFF":
            person = Staff(person_name)
        elif role.upper() == "FELLOW":
            person = Fellow(person_name, wants_accomodation)
        else:
            print("Invalid person role: " + role)
            return
        self._allocate_room(person, wants_accomodation)

    def _allocate_room(self, person, wants_accomodation):

        person = person
        wants_accomodation = wants_accomodation
        # Check if there are rooms
        if len(Amity.list_of_rooms):
            # Make a list of available rooms depending on person role
            available_rooms = []
            for room in Amity.list_of_rooms:
                if (room.room_type == "Office" and len(room.occupants) < 6) \
                        or (room.room_type == "Living Space" and len(room.occupants) < 4):
                    available_rooms.append(room)

            if person.role == "Staff":
                available_rooms = [room for room in available_rooms if room.room_type == "Office"
                                   and len(room.occupants) < 6]
            if available_rooms:
                room = random.choice(available_rooms)
            else:
                print("sorry, we don't have available rooms at the moment")
            allocated = False
            while not allocated:
                # Allocate person a room randomly
                if room.room_type == "Living Space" and len(room.occupants) < 4 \
                        and person.role == "Fellow" and wants_accomodation == 'Y':
                    room.occupants.append(person)
                    allocated = True
                    break
                elif room.room_type == "Living Space" and len(room.occupants) < 4 \
                        and person.role == "Fellow":
                    room.occupants.append(person)
                    allocated = True
                    break
                elif room.room_type == "Office" and len(room.occupants) < 6:
                    room.occupants.append(person)
                    allocated = True
                    break
                else:
                    print("Sorry. We could not find you a room at this moment")
                    break
        else:
            print("There are no rooms to allocate")

        if not allocated:
            Amity.unallocated_members.append(person)
            print("{} was added to the waiting list".format(
                person.person_name))
        else:
            Amity.allocated_members.append(person)
            print("{} successfully allocated {}".format(
                person.person_name, room.room_name))

    def reallocate_person(self, person_name, room_name):

        # if successful, alert the user of the change,
        # eg, you've been reallocated to Java from Swift
        # set the new value of the dic to new_room_name
        # return message:
        # person_name transferred from former_room to new_room

        room = [room for room in Amity.list_of_rooms
                if room_name.upper() == room.room_name.upper()]
        person = [person for person in Amity.allocated_members
                  if person_name.upper() == person.person_name.upper()]
        person, room = person[0], room[0]
        if not person:
            print("{} has no room in Amity".format(person_name))
            return
        elif not room:
            print("{} is not a room in Amity".format(room_name))
            return
        elif [occupant for occupant in room.occupants
                if person_name.upper() == occupant.person_name.upper()]:
            print("{0} is already in {1}".format(
                person_name, room.room_name))
            return

        elif room.room_type == "Living Space" and person.role == "Staff":
            print("{} is a living space. Staff can only be allocated offices"
                  .format(room.room_name))
        elif (room.room_type == "Living Space" and len(room.occupants) > 4) \
                or (room.room_type == "Office" and len(room.occupants) > 6):
            print("{} is full".format(room.room_name))
        else:
            current_room = [room for room in Amity.list_of_rooms
                            if person in room.occupants]
            room.occupants.append(person)
            current_room[0].occupants.remove(person)
            print("{0} was moved from {1} to {2}".format(
                person.person_name, current_room[0].room_name, room.room_name))

    def print_unallocated(self):

        if len(Amity.unallocated_members):
            print("UNALLOCATED PEOPLE")
            for person in Amity.unallocated_members:
                print("\t{}".format(person.person_name))
        else:
            print("Awesome! There are no people in the waiting list")

    def create_room(self, room_name):
        """Create a new room"""

        # Check if the room exists
        if [room for room in Amity.list_of_rooms if room_name.upper() == room.room_name.upper()]:
            print("{0} already exists in Amity.".format(room_name))
            return
        r_type = random.choice(["Office", "LivingSpace"])
        if r_type == "Office":
            room = Office(room_name)
        else:
            room = LivingSpace(room_name)
        Amity.list_of_rooms.append(room)
        print("Created {0}: Type is {1}".format(
            room.room_name, room.room_type))

    def print_room(self, room_name):
        """Print names of all people in room_name"""

        room = [room for room in Amity.list_of_rooms if
                room.room_name.upper() == room_name.upper()]
        if room:
            room = room[0]
            print("{} OCCUPANTS \n".format(room.room_name.upper()))
            print("-----------------------------------------------------")
            for occupant in room.occupants:
                print("\t{0}\n".format(occupant.person_name))
        else:
            print("{} does not exist in Amity".format(room_name))
            return

    def print_allocations(self, filename):

        if not Amity.list_of_rooms:
            print("No rooms to display")
            return
        if filename:
            path = os.path.join(os.path.dirname(__file__), "filename")
            with open(path, 'w') as f:
                for room in Amity.list_of_rooms:
                    if len(room.occupants):
                        f.write(room.room_name.upper() + '\n')
                        f.write(
                            "------------------------------------------------------")
                        for occupant in room.occupants:
                            f.write((occupant.person_name + ','), end=" ")
                        f.write('\n')

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
    main()
