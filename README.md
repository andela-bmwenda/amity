[![Build Status](https://travis-ci.org/andela-bmwenda/amity-cp1.svg?branch=develop)](https://travis-ci.org/andela-bmwenda/amity-cp1)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8545e9cf2e9840caae8c41a9f7ec7803)](https://www.codacy.com/app/boniface-mwenda/amity-cp1?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-bmwenda/amity-cp1&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/andela-bmwenda/amity-cp1/badge.svg)](https://coveralls.io/github/andela-bmwenda/amity-cp1)
# Amity Space Allocator
A command line application for allocating working and living space to Andelans.

## CONTENTS

 - Introduction
 - Requirements
 - Installation
 - Features
 - Testing
 - To do
 - Credits
 - License

## INTRODUCTION
Amity cli is a command line application built using python 3. It helps a user to create rooms and randomly assign them occupants. It can also save the data to a database and retrieve it for later use. Amity has been tested on `python 3.4 and '3.5`.

## REQUIREMENTS
Amity runs on [docopt](docopt.org) on the console. It is recommended that you install the app on a virtual environment, such as [virtualenv](https://virtualenv.pypa.io/en/stable/) to avoid cluttering your local environment with unnecessary packages, or worse still, creating conflicts with your system packages. That would be quite an unpleasant experience!
Amity also uses [sqlite3 database](https://sqlite.org/) which should be installed in your system.

All dependencies are listed in `requirements.txt`.

## INSTALLATION
Installing Amity is fast and easy. 
- Get the source code from github using [this link](https://github.com/andela-bmwenda/amity-cp1).
- Clone the repo using your preferred method, either `ssh` or `https`.
- Navigate to the root folder `cd amity-cp1`
- Create a virtual environment with `virtualenv`. Make sure it is already installed in your system.
- Activate your virtual environment
- Install requirements using [pip](https://pip.pypa.io/en/stable/). `pip install -r requirements.txt`
- Start the app by running the interactive option `python main.py -i`

## Features
Use the `help` command to display a list of all functions in Amity. Even better, type `'help` before any command to see it's usage. Easy does it!

### Create Room
To create a new room, use the `create_room` command followed by the name of the room and the room type. The room type can either be office(o) or livingspace(l).
> create_room earth livingspace OR create_room earth l
Also, Amity allows you to create as many rooms as you want in a single command.
> create_room winterfell -l mereen -o kingslanding -o westeros l

### Add Person
This command takes three positional arguments and one optional argument. The first three arguments are `first_name`, `last_name` and `role`. A person's role can be either `staff` or `fellow`. If the person is a fellow, they have an option of requesting for accomodation using the argument `wants_accomodation`. The default is No.
When a person is added successfully, they are automatically allocated a room or rooms as requested. If no rooms are found for the person, they are added to the waiting list. It is important to note that staff cannot be allocated living spaces.

**Examples**
> add_person John Doe fellow --wants_accomodation Y

This will allocate John Doe an office and a living space. If neither is found, John Doe will be added to the waiting list

> add_person Mary Jane staff

This will allocate Mary Jane an office

> add_person Jeff Archer fellow

This will allocate Jeff Archer an office only

### Load People
To make your life easier, Amity allows you to add people from a file. The `load_people` command does just this.
Just ensure that your data follows the format below:

OLUWAFEMI SULE FELLOW Y

DOMINIC WALTERS STAFF

SIMON PATTERSON FELLOW Y

MARI LAWRENCE FELLOW Y

LEIGH RILEY STAFF

**Example**
> load_people filename.txt

### Print Allocations
This command prints rooms and their occupants to the screen. The command has an optional argument `--output=filename` which allows the user to save the allocations to a text file.
**Example**
> print_allocations
This will print the allocations to screen only

> print_allocations --output=sample_text.txt
This will print the allocations to screen and also write to sample_text.txt

**Sample output**

WINTERFELL

---------------------------------------------------------------------------
DAVID GIBSON, HUNJA WAITHAKA, SIMON PATTERSON, MARI LAWRENCE, LEIGH RILEY


### Print Unallocated
This command prints out all people in the waiting list to the screen. An optional argument `--output=target_file` can be passed to save the data to a text file.

**Example**
> print_unallocated --output=unallocated.txt

### Print Room
This command prints all the occupants in a room specified.

**Example**
> print_room qarth

### Reallocate Person
This transfers a person from their allocated room to a new specified room

**Example**
> reallocate_person John Doe Kingslanding

### Save State
Application data in Amity, for example rooms, allocations and unallocated people can be saved to a database using the `save_state` command. The command takes an optional argument `--database=sqlitedb_path` which allows the user to pass the database path. If no argument is passed, the database is saved in a default path at the root directory.

**Example**

> save_state --database=my_database.db

### Load State
App data can be loaded from the database using the `load_state` command. The optional argument `--database=sqlitedb_path` allows the user to specify the database to load.

**Example**

> load_state --database=my_database.db

**Screencast**
Seeing is believing! Here is a screencast of Amity in action.
[screencast](https://asciinema.org/a/9nk403isnahihvbqj3zvt9v0h)

## Testing
Amity has been tested using the `nose` package. Run `nosetests` in the main directory to run the tests. The app also uses `coverage.py` to asses test coverage. Run `nosetests --with-coverage` to run the tests with coverage information.

## To Do
- Load people from unallocated list once new rooms become available

## License
Amity uses the MIT license. Feel free to fork the repo and add your awesome features. Feel free to open issues incase you spot bugs.
