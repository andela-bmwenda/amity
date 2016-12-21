import os
import pickle
import random
import sqlite3
from termcolor import cprint
from app.db import AmityDb
from environment import ROOT_DIR
from .person import Fellow, Staff
from .room import Office, LivingSpace

global db


class Amity(object):
    """Main class for Amity app.

    Attributes:
    allocated_members   list of persons with rooms
    unallocated_members list of people with no room allocation
    list_of_rooms       list of rooms in amity
    """

    def __init__(self):
        self.unallocated_members = []
        self.allocated_members = []
        self.list_of_rooms = []

    def add_person(self, first_name, last_name, role, wants_accomodation='N'):
        """Creates a person instance and allocates them a room."""

        person_name = first_name.upper() + " " + last_name.upper()

        person = [
            person for person in self.allocated_members
            if person_name.upper() == person.person_name.upper() and
            person.role.upper() == role.upper()
        ]
        if person:
            print("Warning! {0} exists in Amity. ID: {1}".format(
                person_name, person[0].identifier)
            )
            ans = input("Is this a different person? y/n\n")
            if ans == 'y':
                pass
            else:
                return "Person exists in Amity"
        if role.upper() == "STAFF":
            person = Staff(person_name)
        elif role.upper() == "FELLOW":
            person = Fellow(person_name, wants_accomodation)
        else:
            cprint("Invalid person role: " + role, 'red')
            return "{} is not a valid person role".format(role)
        self.allocate_room(person, wants_accomodation)

    def allocate_room(self, person, wants_accomodation):
        """Allocates a random room to person."""

        person = person
        wants_accomodation = wants_accomodation
        has_office = False
        has_living = False
        # Check if there are rooms
        if len(self.list_of_rooms):
            # Make a list of available rooms
            offices = []
            living_spaces = []
            for room in self.list_of_rooms:
                if (room.room_type == "Office" and not room.full()):
                    offices.append(room)
                elif (room.room_type == "Living Space" and not room.full()):
                    living_spaces.append(room)
            # Allocate person an office
            if offices:
                room = random.choice(offices)
                room.occupants.append(person)
                has_office = True
            else:
                cprint("There are no offices available at the moment",
                       'yellow')
            # Allocate person living space if wants accomodation
            if (living_spaces and person.role == "Fellow" and
                    person.wants_accomodation == "Y"):
                room = random.choice(living_spaces)
                room.occupants.append(person)
                has_living = True

            if ((person.role == "Staff" and has_office) or
                (person.role == "Fellow" and person.wants_accomodation == "N"
                 and has_office) or (person.role == "Fellow" and
                                     person.wants_accomodation == "Y" and has_office and has_living)):
                person.current_room = room.room_name
                self.allocated_members.append(person)
                cprint("{} successfully allocated {}".format(
                    person.person_name, room.room_name), 'green')
            elif ((person.role == "Fellow" and person.wants_accomodation == "Y"
                   and has_office and not has_living)):
                person.current_room = room.room_name
                self.unallocated_members.append(person)
                cprint("Your office is {}. Living space was not found"
                       .format(room.room_name), 'green')
                cprint("{} was added to the waiting list".format(
                    person.person_name), 'green')
            else:
                self.unallocated_members.append(person)
        else:
            cprint("There are no rooms to allocate. {} was added to"
                   .format(person.person_name) + " the waiting list", 'yellow')
            self.unallocated_members.append(person)
            return "No rooms available"

    def reallocate_person(self, person_name, room_name):
        """Transfers person to a different room."""

        room = [room for room in self.list_of_rooms
                if room_name.upper() == room.room_name.upper()]
        person = [person for person in self.allocated_members
                  if person_name.upper() == person.person_name.upper()]
        if not person:
            cprint("{} has no room in Amity".format(person_name), 'yellow')
            return "Person not found"
        elif not room:
            cprint("{} is not a room in Amity".format(room_name), 'yellow')
            return "Room not found"
        elif [occupant for occupant in room[0].occupants
                if person_name.upper() == occupant.person_name.upper()]:
            cprint("{0} is already in {1}".format(
                person_name, room[0].room_name), 'yellow')
            return "Person is already in room"

        elif room[0].room_type == "Living Space" and person[0].role == "Staff":
            cprint("{} is a living space. Staff can only be allocated offices"
                   .format(room[0].room_name), 'yellow')
            return "Staff cannot be allocated living space"
        elif (room[0].room_type == "Living Space" and room[0].full()) \
                or (room[0].room_type == "Office" and room[0].full()):
            cprint("{} is full. Try again later".format(
                room[0].room_name), 'yellow')
            return "Room is full"
        else:
            current_room = [room for room in self.list_of_rooms
                            if person[0] in room.occupants]
            room[0].occupants.append(person[0])
            current_room[0].occupants.remove(person[0])
            person[0].current_room = room[0].room_name
            cprint("{0} was moved from {1} to {2}".format(
                person[0].person_name, current_room[0].room_name,
                room[0].room_name), 'green')
            return "Reallocation successful"

    def print_unallocated(self, file):
        """Prints out members without rooms."""

        if len(self.unallocated_members):
            text = ""
            text += "UNALLOCATED PEOPLE" + '\n'
            for person in self.unallocated_members:
                text += ("\t{}\n".format(person.person_name))
            print(text)
        else:
            cprint("Awesome! There are no people in the waiting list", 'green')

        if file:
            path = os.path.join(os.path.dirname(__file__), file)
            with open(file, 'w') as f:
                f.write(text)
            cprint("Successfully saved unallocated people to {} ".format(
                path), 'green')
            return "Unallocated people successfully saved to file"
        return "Print unallocations successful"

    def create_room(self, room_name, room_type):
        """Creates a new room."""

        # Check if the room exists
        if [room for room in self.list_of_rooms if room_name.upper() == room.room_name.upper()]:
            cprint("{0} already exists in Amity.".format(room_name), 'yellow')
            return "Room already exists"
        if room_type.upper() == "OFFICE" or room_type.upper() == "O":
            room = Office(room_name)
        elif room_type.upper() == "LIVINGSPACE" or room_type.upper() == "L":
            room = LivingSpace(room_name)
        else:
            cprint("{} is not a valid room type.".format(room_type), 'red')
            cprint(
                "Options: 'office' | 'o' or 'livingspace' | 'l'. Not case sensitive", 'yellow')
            return "Invalid room type"
        self.list_of_rooms.append(room)
        cprint("Created {0}: Type is {1}".format(
            room.room_name, room.room_type), 'green')
        return room

    def print_room(self, room_name):
        """Prints names of all people in a room."""

        room = [room for room in self.list_of_rooms if
                room.room_name.upper() == room_name.upper()]
        if room:
            room = room[0]
            print("{} OCCUPANTS \n".format(room.room_name.upper()))
            print("--" * 25)
            for occupant in room.occupants:
                print("\t{0}\n".format(occupant.person_name))
            return "Print room successful"
        else:
            cprint("{} does not exist in Amity".format(room_name), 'red')
            return "Room does not exist"

    def print_allocations(self, filename):
        """
        Prints persons with room allocations
        and their current rooms
        """

        if not self.list_of_rooms:
            cprint("No rooms to display", 'yellow')
            return "No rooms"
        output = ""
        for room in self.list_of_rooms:
            if len(room.occupants):
                output += room.room_name.upper() + '\n\n'
                output += "---" * 25 + '\n'
                for occupant in room.occupants:
                    output += occupant.person_name + ", "
                output += ('\n\n\n')
        print(output)

        if filename:
            path = os.path.join(os.path.dirname(__file__), filename)
            with open(filename, 'w') as f:
                f.write(output)
            cprint("Successfully saved allocations data to {}".format(path), 'green')
            return "Allocations successfully saved to file"
        return "Print allocations successful"

    def load_people(self, filename):
        """Allocates people rooms from a plain text file."""

        try:
            with open(filename, 'r') as f:
                people = f.readlines()
            for person in people:
                params = person.split() + ['N']
                self.add_person(params[0], params[1], params[2], params[3])
            cprint("Successfully loaded people from {0}".format(
                ROOT_DIR + '/' + filename), 'green')
        except:
            cprint("File not found in the path specified", 'red')
            return "Error. File not found"

    def save_state(self, db_name):
        """"Saves application data to database."""

        if not self.list_of_rooms and not self.allocated_members \
                and not self.unallocated_members:
            cprint("There is no data to save at the moment", 'yellow')
            return "No data"
        # Create db
        db = AmityDb(db_name)
        db.create_tables()

        # Create a tuple of rooms
        self_rooms = []
        for room in self.list_of_rooms:
            residents = []
            for occupant in room.occupants:
                residents.append(occupant.person_name)
            tp = (room.room_name, room.room_type,
                  room.capacity, ", ".join(residents))
            self_rooms.append(tp)

        # tuple of allocated people
        allocated = []
        for person in self.allocated_members:
            tp = (person.identifier, person.person_name,
                  person.role, person.current_room)
            allocated.append(tp)

        # tuple of unallocated members
        unallocated = []
        for person in self.unallocated_members:
            tp = (person.identifier, person.person_name,
                  person.role, person.current_room)
            unallocated.append(tp)

        # Save state
        app_data = (self.list_of_rooms,
                    self.allocated_members,
                    self.unallocated_members
                    )
        state = sqlite3.Binary(pickle.dumps(app_data))

        db.write_data(self_rooms,
                      allocated,
                      unallocated,
                      state
                      )
        cprint("Saved app data to {}".format(ROOT_DIR), 'green')
        return "Save state successful"

    def load_state(self, db_path):
        """Loads application data from the database."""

        # Search for db and establish connection
        if os.path.exists(db_path):
            db = AmityDb(db_path)
            if db.read_data():
                app_data = pickle.loads(db.read_data())
                self.list_of_rooms = app_data[0]
                self.allocated_members = app_data[1]
                self.unallocated_members = app_data[2]
                cprint("Successfully loaded app data from {}".format(
                    ROOT_DIR), 'green')
                return "Load state successful"
            else:
                cprint("Error. Database does not have a saved state", 'red')
                return "Saved state not found"
        else:
            cprint("Database not found", 'red')
            return "Error. Path not found"
