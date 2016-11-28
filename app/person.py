import random


class Person(object):
    """
    This class is the base class for Fellow and Staff.
    It defines common attributs below Fellow and Staff
    and initialises them.
    """

    def __init__(self, first_name, last_name, role=None):
        """Initializes Person class"""

        self.identifier = random.randint(0, 9999)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role


class Fellow(Person):
    """Creates fellows, and inherits from Person class"""

    def __init__(self, first_name, last_name, wants_accomodation='N'):
        super(Fellow, self).__init__(first_name, last_name)
        self.role = "Fellow"
        self.wants_accomodation = wants_accomodation


class Staff(Person):
    """Creates Staff members and inherits from Person"""

    def __init__(self, first_name, last_name):
        super(Staff, self).__init__(first_name, last_name)
        self.role = "Staff"


# f = Fellow("John", "Doe", 'Y')
# print(f.identifier, f.first_name, f.last_name, f.role, f.wants_accomodation)
# s = Staff("Mike", "Lanes")
# print(s.identifier, s.role, s.first_name, s.last_name)
