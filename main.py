#!/usr/bin/env python
"""
Usage:
    amity create_room (<room_name> <room_type>)...
    amity add_person <first_name> <last_name> (Fellow | Staff) [--wants_accomodation=(Y | N)]
    amity print_allocations [-output=<filename>]
    amity reallocate_person <first_name> <last_name> <room_name>
    amity print_room <room_name>
    amity print_unallocated [-output=<filename>]
    amity load_people <filename>
    amity save_state [--database=<sqlite_database>]
    amity load_state
    amity (-i | --interactive)
    amity (-h | --help | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
    -a, --wants_accomodation=<opt>  Person wants accomodation [default: N]
    -d, --database=<sqlite_database>  Save state to specified database [default: amity_db]
"""

import sys
import os
import cmd
from docopt import docopt, DocoptExit
from pyfiglet import figlet_format
from termcolor import cprint
from app.amity import Amity

amity = Amity()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def intro():
    cprint(figlet_format('Amity Space Allocator', font='slant'),
           'blue', attrs=['bold'])
    print("Welcome to Amity! Here is a list of commands to get you started." +
          " Type 'help' anytime to access documented commands")
    cprint(__doc__, 'magenta')


class AmitySystem(cmd.Cmd):
    prompt = '(Amity) '
    file = None

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room (<room_name> <room_type>)..."""

        rooms = args["<room_name>"]
        types = args["<room_type>"]
        for room in rooms:
            r_type = types[rooms.index(room)]
            amity.create_room(room, r_type)

    @docopt_cmd
    def do_add_person(self, args):
        """
        Usage:
            add_person <first_name> <last_name> (fellow | staff) [--wants_accomodation=<opt>]

        Options:
            -a, --wants_accomodation=<opt>  Wants accomodation [default: N]
        """
        first_name = args["<first_name>"]
        last_name = args["<last_name>"]
        if args["fellow"]:
            role = "FELLOW"
        else:
            role = "STAFF"
        accomodate = args["--wants_accomodation"].upper()
        if accomodate == 'Y' or accomodate == 'N':
            amity.add_person(first_name, last_name, role, accomodate)
        else:
            cprint("Invalid accomodation option. Please enter Y/N", 'red')

    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <first_name> <last_name> <room_name>"""

        first_name = args["<first_name>"]
        last_name = args["<last_name>"]
        room_name = args["<room_name>"]
        person_name = first_name + " " + last_name

        amity.reallocate_person(person_name, room_name)

    @docopt_cmd
    def do_print_allocations(self, args):
        """
        Usage: print_allocations [--output=<filename>]

        Options:
        -o, --output=<filename>  Save allocations to file
        """

        filename = args["--output"]
        amity.print_allocations(filename)

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people <filename>"""

        file = args["<filename>"]

        amity.load_people(file)

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [-output=<filename>]

        Options:
        -o, --output=<filename>  Save unallocated people to file
        """

        file = args["--output"]

        amity.print_unallocated(file)

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""

        room_name = args["<room_name>"]
        amity.print_room(room_name)

    @docopt_cmd
    def do_save_state(self, args):
        """
        Usage: save_state [--database=<sqlite_database>]

        Options:
        -d, --database=<sqlite_database>  Save state to specified database [default: amity_db]    
        """

        db_name = args["--database"]
        amity.save_state(db_name)

    @docopt_cmd
    def do_load_state(self, args):
        """
        Usage: load_state [--load=<database>]

        Options:
        -l, --load=<database>  Load data from specified database [default: amity_db]
        """
        amity.load_state(args["--load"])

    def do_clear(self, arg):
        """Clears screen"""

        os.system('clear')

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Thank you for using Amity. Adios!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    os.system('clear')
    intro()
    AmitySystem().cmdloop()

print(opt)
