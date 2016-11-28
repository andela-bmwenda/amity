#!/usr/bin/env python
"""
Usage:
    amity create_room <room_name>...
    amity add_person <first_name> <last_name> <role> [--accomodate=<N>]
    amity print_room <room_name>
    amity (-i | --interactive)
    amity (-h | --help | --version)

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import os
import cmd
from app.amity import Amity
from docopt import docopt, DocoptExit


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


class AmitySystem(cmd.Cmd):
    intro = 'Welcome to Amity' \
        + ' (type help for a list of commands.)'
    prompt = '(Amity) '
    file = None

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_name>..."""
        # print("Here are the rooms\n\t{}".format(args))
        rooms = args["<room_name>"]
        # Amity.create_room(self, " ".join(rooms))
        for room in rooms:
            Amity.create_room(self, room)

    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <first_name> <last_name> <role> [--accomodate=<N>]"""
        first_name = args["<first_name>"]
        last_name = args["<last_name>"]
        role = args["<role>"]
        # accomodate = args["[--accomodate]"]
        # Amity.add_person(first_name, last_name, role)
        Amity.add_person(self, first_name, last_name, role)

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""

        room_name = args["<room_name>"]
        Amity.print_room(self, room_name)

    def do_clear(self, arg):
        """Clears screen>"""

        os.system('clear')

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    AmitySystem().cmdloop()

print(opt)
