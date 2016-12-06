import random


class Person(object):
    """
    This class is the base class for Fellow and Staff.
    It defines common attributs below Fellow and Staff
    and initialises them.
    """

    def __init__(self, person_name, role=None):
        """Initializes Person class"""

        self.identifier = random.randint(0, 9999)
        self.person_name = person_name
        self.role = role


class Fellow(Person):
    """Creates fellows, and inherits from Person class"""

    def __init__(self, person_name, wants_accomodation='N'):
        super(Fellow, self).__init__(person_name)
        self.role = "Fellow"
        self.wants_accomodation = wants_accomodation


class Staff(Person):
    """Creates Staff members and inherits from Person"""

    def __init__(self, person_name):
        super(Staff, self).__init__(person_name)
        self.role = "Staff"
