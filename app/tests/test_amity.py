import unittest
from mock import patch, mock_open
from app.amity import Amity
from app.person import Fellow, Staff
from app.room import Office, LivingSpace


class AmityTestCase(unittest.TestCase):
    """Test cases for Amity class"""

    def setUp(self):
        self.living_space = LivingSpace("Swift")
        self.office = Office("Scala")
        self.fellow = Fellow("Mike Jon")
        self.fellow2 = Fellow("Lucas Chan", "Y")
        self.staff = Staff("Rick Man")
        self.amity = Amity()

    def test_rooms_are_added_successfully(self):
        """Tests offices of living spaces are created"""

        self.amity.create_room("Scala", "O")
        self.amity.create_room("Go", "L")
        self.assertEqual(len(self.amity.list_of_rooms), 2)

    def test_office_is_created_successfully(self):
        """Tests offices are created"""

        office = self.amity.create_room("Office", "O")
        self.assertIsInstance(office, Office)

    def test_living_space_is_created_successfully(self):
        """Tests living_spaces are created"""

        l_space = self.amity.create_room("Keja", "L")
        self.assertIsInstance(l_space, LivingSpace)

    def test_living_space_does_not_exceed_four_people(self):
        """Tests living space does not exceed capacity"""

        self.amity.list_of_rooms.append(self.living_space)
        self.living_space.occupants = ["Tom", "Dick", "Harry", "Johny"]
        self.amity.allocate_room(self.fellow, "Y")
        self.assertEqual(len(self.amity.unallocated_members), 1)
        self.assertEqual(len(self.living_space.occupants), 4)

    def test_office_does_not_exceed_six_people(self):
        """Tests office does not exceed capacity"""

        self.amity.list_of_rooms.append(self.office)
        self.office.occupants = ["alpha", "beta", "charlie",
                                 "delta", "echo", "foxtrot"]
        self.amity.allocate_room(self.staff, "N")
        self.assertEqual(len(self.amity.unallocated_members), 1)
        self.assertEqual(len(self.office.occupants), 6)

    def test_staff_is_not_allocated_living_space(self):
        """Tests staff members can only be in offices"""

        self.amity.list_of_rooms.append(self.living_space)
        self.amity.allocate_room(self.staff, "N")
        self.assertEqual(len(self.amity.list_of_rooms[0].occupants), 0)
        self.assertEqual(len(self.amity.unallocated_members), 1)

    def test_duplicate_rooms_are_not_added(self):
        """Tests rooms with same name are not allowed"""

        self.amity.list_of_rooms.append(self.living_space)
        self.assertEqual(self.amity.create_room("Swift", "L"),
                         "Room already exists")

    def test_fellow_gets_office_by_default(self):
        """Tests fellow is created and allocated room"""

        self.amity.list_of_rooms.append(self.office)
        self.amity.add_person("Tom", "Riley", "Fellow")
        self.assertTrue(self.amity.list_of_rooms[0].occupants[0]
                        .person_name == "Tom Riley".upper())

    def test_staff_member_is_added_successfully(self):
        """Tests staff member is created and allocated room"""

        self.amity.list_of_rooms.append(self.office)
        self.amity.add_person("Rick", "James", "Staff")
        self.assertEqual(len(self.amity.allocated_members), 1)

    def test_people_are_loaded_from_file_successfully(self):
        """Tests ii accepts data from file"""

        with patch("builtins.open", mock_open(read_data="sample text")) as m:
            self.amity.load_people("file")

        m.assert_called_with("file", 'r')

    def test_for_invalid_person_role(self):
        """Tests invalid person role is not allowed"""

        res = self.amity.add_person("Guy", "Ross", "Invalid")
        self.assertEqual(res, "Invalid is not a valid person role")

    def test_members_are_added_to_waiting_list_if_no_rooms(self):
        """Tests unallocated people are added to waiting list"""

        self.amity.add_person("Roomless", "Man", "Fellow", "Y")
        self.amity.add_person("Roomless", "Woman", "Staff")
        self.amity.add_person("Random", "Person", "Fellow")
        self.assertEqual(len(self.amity.unallocated_members), 3)

    def test_members_are_added_to_waiting_list_if_rooms_full(self):
        """Tests members who miss rooms are added to waiting list"""

        self.living_space.occupants += ["one", "two", "three", "four"]
        self.office.occupants += ["one", "two", "three", "four", "five", "six"]
        self.amity.add_person("Molly", "Sue", "Fellow", "Y")
        self.amity.add_person("Ledley", "Moore", "Staff")
        self.assertEqual(len(self.amity.unallocated_members), 2)

    def test_fellow_gets_office_and_living_space_if_wants_room(self):
        """Tests fellow who wants accomodation gets a living space"""

        self.amity.list_of_rooms.append(self.living_space)
        self.amity.list_of_rooms.append(self.office)
        self.amity.add_person("Martin", "Luther", "Fellow", "Y")
        self.assertTrue(self.amity.allocated_members[0]
                        .person_name == "Martin Luther".upper())
        self.assertEqual(self.amity.list_of_rooms[0].occupants[
                         0].person_name, "MARTIN LUTHER")
        self.assertEqual(self.amity.list_of_rooms[1].occupants[
                         0].person_name, "MARTIN LUTHER")

    def test_cannot_reallocate_non_existent_person(self):
        """Tests members not allocated cannot be reallocated"""

        self.amity.list_of_rooms.append(self.living_space)
        res = self.amity.reallocate_person("No Name", "Swift")
        self.assertEqual(res, "Person not found")

    def test_cannot_reallocate_non_existent_room(self):
        """Tests reallocation only allows valid rooms"""

        self.amity.allocated_members.append(self.staff)
        res = self.amity.reallocate_person("Rick Man", "Inexistent")
        self.assertEqual(res, "Room not found")

    def test_cannot_reallocate_to_same_room(self):
        """
        Tests person cannot be reallocated to
        the same room
        """

        self.amity.list_of_rooms.append(self.office)
        self.amity.list_of_rooms[0].occupants.append(self.fellow)
        self.amity.allocated_members.append(self.fellow)
        res = self.amity.reallocate_person("Mike Jon", "Scala")
        self.assertEqual(res, "Person is already in room")

    def test_cannot_reallocate_staff_to_living_space(self):
        """Tests staff cannot be reallocated to livingspace"""

        self.amity.list_of_rooms += [self.office, self.living_space]
        self.amity.allocated_members.append(self.staff)
        self.amity.list_of_rooms[0].occupants.append(self.staff)
        res = self.amity.reallocate_person("Rick Man", "Swift")
        self.assertEqual(res, "Staff cannot be allocated living space")

    def test_cannot_reallocate_person_to_full_room(self):
        """Tests person cannot be reallocated a full room"""

        self.amity.list_of_rooms.append(self.living_space)
        self.amity.add_person("Fellow", "One", "Fellow", "Y")
        self.amity.add_person("Fellow", "Two", "Fellow", "Y")
        self.amity.add_person("Fellow", "Three", "Fellow", "Y")
        self.amity.add_person("Fellow", "Four", "Fellow", "Y")
        self.amity.list_of_rooms.append(self.office)
        self.amity.allocated_members.append(self.fellow)
        res = self.amity.reallocate_person("Mike Jon", "Swift")
        self.assertEqual(res, "Room is full")

    def test_person_is_reallocated_successfully(self):
        """Tests reallocate person works"""

        self.amity.list_of_rooms += [self.office, self.living_space]
        self.amity.allocated_members.append(self.fellow)
        self.amity.list_of_rooms[0].occupants.append(self.fellow)
        self.amity.reallocate_person("Mike Jon", "Swift")
        # Assert the person is transfered to new room
        self.assertEqual(self.amity.list_of_rooms[1].occupants[
                         0].person_name, "Mike Jon")
        # Assert the person is removed from former room
        self.assertTrue(len(self.amity.list_of_rooms[0].occupants) == 0)

    def test_cannot_print_inexistent_room(self):
        """
        Tests print_room raises alert if there
        are no occupants
        """

        res = self.amity.print_room("None")
        self.assertEqual(res, "Room does not exist")

    def test_print_room_works(self):
        """
        Tests print room returns
        the names of occupants
        """

        self.amity.list_of_rooms.append(self.office)
        self.amity.list_of_rooms[0].occupants += \
            [self.fellow, self.fellow2, self.staff]

        res = self.amity.print_room("Scala")
        self.assertEqual(res, "Print room successful")

    def test_print_allocations_raises_alert_if_no_rooms(self):
        """Tests alert is raised if no allocations available"""

        self.assertEqual(self.amity.print_allocations(None), "No rooms")

    def test_print_allocations_to_screen_works(self):
        """Tests allocations are printed to screen"""

        self.amity.list_of_rooms += [self.office, self.living_space]
        self.amity.add_person("Carla", "Bruni", "Staff")
        self.amity.add_person("Peter", "Pan", "Fellow")
        self.amity.add_person("Mike", "Ross", "Fellow", "Y")
        self.amity.add_person("Hype", "Mann", "Fellow")
        res = self.amity.print_allocations(None)
        self.assertEqual(res, "Print allocations successful")

    def test_allocations_are_written_to_file(self):
        """Tests if allocations are saved to file"""

        self.amity.list_of_rooms += [self.office, self.living_space]
        self.amity.allocated_members += [self.staff, self.fellow, self.fellow2]
        self.amity.list_of_rooms[0].occupants.append(self.staff)
        self.amity.list_of_rooms[0].occupants.append(self.fellow)
        self.amity.list_of_rooms[0].occupants.append(self.fellow2)
        self.amity.list_of_rooms[1].occupants.append(self.fellow2)

        m = mock_open()
        with patch('builtins.open', m):
            self.amity.print_allocations("file")
        m.assert_called_with("file", 'w')

    def test_print_unallocated_people_works(self):
        """Tests unallocated people are printed to screen"""

        self.amity.unallocated_members += [self.fellow,
                                           self.fellow2, self.staff]
        res = self.amity.print_unallocated(None)
        self.assertEqual(res, "Print unallocations successful")

    def test_it_prints_unallocated_people_to_file(self):
        """Tests if unallocated people are saved to file"""

        self.amity.unallocated_members += [self.staff,
                                           self.fellow, self.fellow2]

        m = mock_open()
        with patch('builtins.open', m):
            self.amity.print_unallocated("file")
        m.assert_called_with("file", 'w')

    def test_load_state_from_invalid_path_raises_error(self):
        """Tests load state does not accept invalid path"""

        res = self.amity.load_people("invalid path")
        self.assertEqual(res, "Error. File not found")

    def test_cannot_save_blank_data_to_db(self):
        """Tests blank data is not saved to db"""

        res = self.amity.save_state(None)
        self.assertEqual(res, "No data")

    def tearDown(self):
        del self.living_space
        del self.office
        del self.fellow
        del self.fellow2
        del self.staff
        del self.amity


if __name__ == '__main__':
    unittest.main()
