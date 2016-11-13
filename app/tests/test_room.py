import unittest
from mock import patch
# import logging as log
from app.room.room import Room


class TestRoomClass(unittest.TestCase):
    """Tests for Room class"""

    def setUp(self):
        self.room = Room()

    @patch.dict('app.room.living_space.LivingSpace.living_and_occupants', {})
    def test_create_living_space(self):
        """Test that a living space is created successfully"""

        ret_livingspace = self.room.create_room("Dojo", "livingspace")
        self.assertEqual(ret_livingspace,
                         "Dojo created successfully as livingspace")

    @patch.dict('app.room.office.Office.office_and_occupants', {})
    def test_create_office(self):
        """Test that an office is created successfully"""

        ret_office = self.room.create_room("Valhala", "office")
        self.assertEqual(
            ret_office, "Created Valhala successfully as an office")

    @patch.dict('app.room.living_space.LivingSpace.living_and_occupants',
                {"Go": ["Barry", "Tom", "Martin", "Luther"]})
    def test_print_living_space_occupants(self):
        """Test that names of all people in  a living space are printed"""

        occupants = self.room.print_room("Go")
        self.assertEqual(occupants, "BARRY, TOM, MARTIN, LUTHER")

    @patch.dict('app.room.office.Office.office_and_occupants',
                {"Krypton": ["Harry", "Jerry", "James"]})
    def test_print_office_occupants(self):
        """Test that names of all people in  an office are printed"""

        occupants = self.room.print_room("Krypton")
        self.assertEqual(occupants, "HARRY, JERRY, JAMES")

    def test_print_allocations(self):
        """Test that allocations are printed in the correct format"""

        # out_put = "ROOM NAME" + '\n\n' + "-------------------------------------" + \
        #     '\n' + "MEMBER 1, MEMBER 2, MEMBER 3"
        # self.assertEqual(self.room.print_allocations(),
        #                  out_put, msg="Incorrect format")
        pass


if __name__ == '__main__':
    unittest.main()
