class Person(object):
    """This class is the base class for Fellow and Staff.
    It defines common attributs below Fellow and Staff
    and initialises them.
    """

    total = 0

    def __init__(self, person_name, role=None):
        """Initialize Person class."""

        self.person_name = person_name
        self.role = role
        self.current_room = None
        Person.total += 1


class Fellow(Person):
    """Creates fellows, and inherits from Person class."""

    def __init__(self, person_name, wants_accomodation='N'):
        super(Fellow, self).__init__(person_name)
        self.identifier = Person.total
        self.role = "Fellow"
        self.wants_accomodation = wants_accomodation


class Staff(Person):
    """Creates Staff members and inherits from Person."""

    def __init__(self, person_name):
        super(Staff, self).__init__(person_name)
        self.identifier = Person.total
        self.role = "Staff"
