import unittest
from app.person.person.person import Person


class TestPersonClass(unittest.TestCase):
    """Tests for Person class"""

    def setup(self):
        self.person = Person()
        pass

    def test_add_person(self):
        """Test that a person is created successfully"""
        pass

    def test_allocate_room(self):
        """Test that a person is successfully allocated a room"""

        pass

    def test_reallocate_person(self):
        """Test that a person is reallocated a room successfully"""
        pass

    def test_load_people(self):
        """
        Test that people can be added to rooms
        from a txt file.
        """

        pass

    def test_print_allocations(self):
        """Test that allocations are printed in the right format"""

        pass

    def test_print_unallocated(self):
        """Test that unallocated people are printed"""

        pass


if __name__ == '__main__':
    unittest.main()
