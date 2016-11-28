import unittest
from app.person.person import Person
from mock import patch


class TestPersonClass(unittest.TestCase):
    """Tests for Person class"""

    def setUp(self):
        self.person = Person()

    @patch.dict('app.amity.amity.Amity.unallocated_members', {"John Doe": "FELLOW"})
    def test_add_duplicate_person(self):
        """Test that adding duplicate member raises an error"""

        ret_value = self.person.add_person("John Doe", "FELLOW", "Y")
        self.assertEqual(ret_value, "John Doe already exists",
                         msg="John Doe is already an Amity member")

    def test_add_person_accepts_valid_persons(self):
        """Test that add_person only accepts fellows or staff"""

        message = self.person.add_person("John Moss", "GARDENER")
        self.assertEqual(message, "Invalid entry",
                         msg="Person can only be Fellow or Staff")

    @patch.dict('app.room.office.Office.office_and_occupants',
                {"Oculus": ["Eeny", "Meeny", "Many", "More"]}
                )
    def test_maximum_office_capacity_is_not_exceeded(self):
        """Test office occupants can only be four or less"""

        ret_message = self.person.add_person("Paul", "STAFF")
        self.assertEqual(ret_message, "Oculus is full. Check later",
                         msg="Offices cannot hold more than four people")

    @patch.dict('app.room.living_space.LivingSpace.living_and_occupants',
                {"Swift":
                    ["Oin", "Gloin", "Bimbur", "Bofur", "Boromir", "Faramir"]}
                )
    def test_maximum_living_space_capacity_is_not_exceeded(self):
        """Test living space occupants can only be six or less"""

        ret_message = self.person.add_person("Merry", "FELLOW", "Y")
        self.assertEqual(ret_message, "Swift is full. Check later",
                         msg="Living spaces cannot hold more than six people")

    @patch.dict('app.amity.amity.Amity.unallocated_members', {})
    def test_fellow_is_successfully_added_to_amity(self):
        """Test person is added to Amity system"""

        ret_value = self.person.add_person("John Doe", "FELLOW", "Y")
        self.assertEqual(ret_value, {"John Doe": "FELLOW"},
                         msg="Person was not successfully added to Amity")

    @patch.dict('app.amity.amity.Amity.unallocated_members', {})
    def test_staff_member_is_successfully_added_to_amity(self):
        """Test member of staff is added to Amity system"""

        ret_value = self.person.add_person("Mary Jane", "STAFF")
        self.assertEqual(ret_value, {"Mary Jane": "STAFF"},
                         msg="Person was not successfully added to Amity")

    @patch.dict('app.room.living_space.LivingSpace.living_and_occupants',
                {"Dojo": ["John Doe"], "Go": []})
    def test_person_to_reallocate_room_exists(self):
        """Test that person to reallocate room exists"""

        return_msg = self.person.reallocate_person(
            "None Existent", "Dojo")
        self.assertEqual(return_msg, "Error: Person does not exist",
                         msg="None Existent person does not have a room in Amity")

    @patch.dict('app.room.office.Office.office_and_occupants',
                {"Camelot": ["Jane Doe"], "Snow": []})
    def test_room_to_reallocate_to_exists(self):
        """Test room to reallocate person exists"""

        return_msg = self.person.reallocate_person(
            "Jane Doe", "False room")
        self.assertEqual(return_msg, "Error: Room does not exist",
                         msg="False room does not exist in Amity")

    @patch.dict('app.room.office.Office.office_and_occupants',
                {"Camelot": ["Jane Doe"], "Snow": []})
    def test_person_is_reallocated_successfully(self):
        """Test that a person is reallocated to a room successfully"""

        return_msg = self.person.reallocate_person("Jane Doe", "Snow")
        self.assertEqual(return_msg, "Jane Doe successfully reallocated to Snow")



if __name__ == '__main__':
    unittest.main()
