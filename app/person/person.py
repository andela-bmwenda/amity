from app.person.staff import Staff
from app.person.fellow import Fellow


class Person(Staff, Fellow):
    """
    Base class for amity users.

    Methods:
    add_person
        adds a person to amity and allocates them a room randomly
    reallocate_person
        allocates a person to a new room
    load_people
        adds people to rooms from a text file
    print_unallocated
        Prints a list of unallocated people to the screen.
        Specifying the -o option outputs the information to a txt file.
    """

    def __init__(self):
        pass

    def add_person(self, person_name, category, wants_accomodation='N'):

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
        pass

    def reallocate_person(self, person_name, new_room_name):

        # check that person and room exist. Raise alert if necessary
        # get the person's current room from allocated_members dictionary
        # call the allocate room function in add_person()
        # if successful, alert the user of the change,
        # eg, you've been reallocate to Java from Swift
        # set the new value of the dic to new_room_name
        # return message:
        # person_name transferred from former_room to new_room
        pass

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

    def print_unallocated(self):

        # get the dictionary of unallocated_members
        # loop through the dic and print each name
        # save the data to a txt if specified
        pass
