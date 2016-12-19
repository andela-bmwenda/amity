import os
import unittest
from app.db import AmityDb
from app.amity import Amity


class AmityDbTestCase(unittest.TestCase):
    """Test cases for Amity database"""

    def setUp(self):
        self.test_db = "temp"
        self.db = AmityDb(self.test_db)
        self.amity = Amity()

        # Create_rooms
        self.amity.create_room("Snow", "O")
        self.amity.create_room("Scala", "O")
        self.amity.create_room("Shire", "L")
        self.amity.create_room("Swift", "L")

        # Add_people to rooms
        self.amity.add_person("John", "Doe", "Fellow")
        self.amity.add_person("Tom", "Harry", "Fellow", "Y")
        self.amity.add_person("Jim", "Jones", "Staff")
        self.amity.add_person("Guy", "Fawkes", "Staff")

    def test_save_state_successful(self):
        """
        Tests that data is saved to database successfully
        """

        res = self.amity.save_state(self.test_db)
        self.assertEqual(res, "Save state successful")

    def test_load_state_works(self):
        """Tests data is loaded from database"""

        self.amity.save_state(self.test_db)
        res = self.amity.load_state(self.test_db)
        self.assertEqual(res, "Load state successful")

    def test_load_state_from_invalid_path_raises_error(self):
        """Tests load state does not allow invalid paths"""

        res = self.amity.load_state("invalid")
        self.assertEqual(res, "Error. Path not found")

    def tearDown(self):
        os.remove(self.test_db)


if __name__ == '__main__':
    unittest.main()
