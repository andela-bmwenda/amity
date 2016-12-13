import os
import random
import pickle
import sqlite3
from .person import Fellow, Staff
from .room import Office, LivingSpace
import app.db as db


class Amity(object):
    """Main class for amity app.

    Attributes:
    allocated_members:  dictionary of people, both fellows and staff
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

    def add_person(self, first_name, last_name, role, wants_accomodation='N'):
        """Create a person instance and allocates them a room."""

        person_name = first_name.upper() + " " + last_name.upper()

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
        """Allocate a random room to person."""

        person = person
        wants_accomodation = wants_accomodation
        allocated = False
        # Check if there are rooms
        if len(Amity.list_of_rooms):
            # Make a list of available rooms depending on person role
            available_rooms = []
            for room in Amity.list_of_rooms:
                if (room.room_type == "Office" and len(room.occupants) < 6) \
                        or (room.room_type == "Living Space" and len(room.occupants) < 4):
                    available_rooms.append(room)

            if person.role == "Staff":
                available_rooms = [room for room in available_rooms if
                                   room.room_type == "Office" and len(room.occupants) < 6]
            if available_rooms:
                room = random.choice(available_rooms)
            else:
                print("sorry, we don't have available rooms at the moment")
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
                    break
        else:
            print("There are no rooms to allocate")

        if not allocated:
            Amity.unallocated_members.append(person)
            print("Sorry {}. We couldn't find a suitable room for you"
                  .format(person.person_name))
            print("{} was added to the waiting list".format(
                person.person_name))
        else:
            person.current_room = room.room_name
            Amity.allocated_members.append(person)
            print("{} successfully allocated {}".format(
                person.person_name, room.room_name))

    def reallocate_person(self, person_name, room_name):
        """Transfer person to a different room."""

        room = [room for room in Amity.list_of_rooms
                if room_name.upper() == room.room_name.upper()]
        person = [person for person in Amity.allocated_members
                  if person_name.upper() == person.person_name.upper()]
        if not person:
            print("{} has no room in Amity".format(person_name))
            return
        elif not room:
            print("{} is not a room in Amity".format(room_name))
            return
        elif [occupant for occupant in room[0].occupants
                if person_name.upper() == occupant.person_name.upper()]:
            print("{0} is already in {1}".format(
                person_name, room[0].room_name))
            return

        elif room[0].room_type == "Living Space" and person[0].role == "Staff":
            print("{} is a living space. Staff can only be allocated offices"
                  .format(room[0].room_name))
        elif (room[0].room_type == "Living Space" and len(room[0].occupants) > 3) \
                or (room[0].room_type == "Office" and len(room[0].occupants) > 5):
            print("{} is full. Try again later".format(room[0].room_name))
        else:
            current_room = [room for room in Amity.list_of_rooms
                            if person[0] in room.occupants]
            room[0].occupants.append(person[0])
            current_room[0].occupants.remove(person[0])
            person[0].current_room = room[0].room_name
            print("{0} was moved from {1} to {2}".format(
                person[0].person_name, current_room[0].room_name,
                room[0].room_name))

    def print_unallocated(self):
        """Print members without rooms."""

        if len(Amity.unallocated_members):
            print("UNALLOCATED PEOPLE")
            for person in Amity.unallocated_members:
                print("\t{}".format(person.person_name))
        else:
            print("Awesome! There are no people in the waiting list")

    def create_room(self, room_name):
        """Create a new room."""

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
        """Print names of all people in a room."""

        room = [room for room in Amity.list_of_rooms if
                room.room_name.upper() == room_name.upper()]
        if room:
            room = room[0]
            print("{} OCCUPANTS \n".format(room.room_name.upper()))
            print("--" * 25)
            for occupant in room.occupants:
                print("\t{0}\n".format(occupant.person_name))
        else:
            print("{} does not exist in Amity".format(room_name))
            return

    def print_allocations(self, filename):
        """Print rooms and their occupants"""

        if not Amity.list_of_rooms:
            print("No rooms to display")
            return
        output = ""
        for room in Amity.list_of_rooms:
            if len(room.occupants):
                output += room.room_name.upper() + '\n\n'
                output += "---" * 25 + '\n'
                for occupant in room.occupants:
                    output += occupant.person_name + ", "
                output += ('\n\n\n')

        print(output)

        if filename:
            path = os.path.join(os.path.dirname(__file__), filename)
            with open(path, 'w') as f:
                f.write(output)

    def load_people(self, filename):
        """Allocate people rooms from a plain text file."""

        path = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(path):
            with open(path, 'r') as f:
                people = f.readlines()
            for person in people:
                params = person.split() + ['N']
                self.add_person(params[0], params[1], params[2], params[3])
        else:
            print("File not found. Remember to add the file extension, \
                eg .txt or .csv"
                  )

    def save_state(self, db_name):
        """"Save application data to database."""

        if not Amity.list_of_rooms and not Amity.allocated_members and not Amity.unallocated_members:
            print("There is no data to save at the moment")
            return
        path = os.path.dirname(__file__)

        print("Saving app data to {}....".format(path + '/' + db_name))

        # db = "../" + db_name + ".db"
        # Create a tuple of rooms
        amity_rooms = []
        for room in Amity.list_of_rooms:
            residents = []
            for occupant in room.occupants:
                residents.append(occupant.person_name)
            tp = (room.room_name, room.room_type,
                  room.capacity, ", ".join(residents))
            amity_rooms.append(tp)

        # tuple of allocated people
        allocated = []
        for person in Amity.allocated_members:
            tp = (person.identifier, person.person_name,
                  person.role, person.current_room)
            allocated.append(tp)

        # tuple of unallocated members
        unallocated = []
        for person in Amity.unallocated_members:
            tp = (person.identifier, person.person_name,
                  person.role, person.current_room)
            unallocated.append(tp)

        # Save state
        app_data = (Amity.list_of_rooms, Amity.allocated_members, Amity.unallocated_members)
        state = sqlite3.Binary(pickle.dumps(app_data))

        db.write_data(amity_rooms,
                      allocated,
                      unallocated,
                      state)

    def load_state(self):
        """Load application data from the database."""

        if db.read_data():
            app_data = pickle.loads(db.read_data())
            Amity.list_of_rooms = app_data[0]
            Amity.allocated_members = app_data[1]
            Amity.unallocated_members = app_data[2]
            print("Successfully loaded app data from database")
        else:
            print("Sorry. No saved state was found")
