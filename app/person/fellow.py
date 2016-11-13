class Fellow(object):
    """
    Class that constructs fellows

    Attributes:
    category - Sets the classification of the person to fellow
    wants_accomadation - A boolean that describes if a fellow wants
    living space.

    """

    def __init__(self, name, wants_accomodation='N'):
        self.name = name
        self.category = "fellow"
        self.wants_accomodation = wants_accomodation
