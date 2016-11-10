
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

    unallocated_members = {}
    allocated_members = {}

    def __init__(self):
        pass

    def load_state(self):
        pass

    def save_state(self, sqlite_db):

        # check that the sqlite db exists
        # create connection
        # save current data, ie
        # rooms data(livingspace_and_accupants, office_and_occupants)
        # person_data()
        pass
