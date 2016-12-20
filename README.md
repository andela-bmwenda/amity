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
Amity runs on [docopt](docopt.org) on the console. It should also be installed in a [virtual environment](https://virtualenv.pypa.io/en/stable/) to avoid cluttering your system with unneeded packages. Other dependancies can be found in `requirements.txt`.

## INSTALLATION
- Access the repo from github using [this link](https://github.com/andela-bmwenda/amity-cp1).
- Clone using your preferred method, either `ssh` or `https`.
- Navigate to the root folder `cd amity-cp1`
- Create a virtual environment with `virtual env` or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/), depending on your preference.
- Activate your virtual environment
- Install requirements using [pip](https://pip.pypa.io/en/stable/). `pip install -r requirements.txt`
- Start the app by running the interactive option `python main.py -i`
## Features
## Testing
Amity has been tested using the `nose` package. Run `nosetests` in the main directory to run the tests. The app also uses `coverage.py` to asses test coverage. Run `nosetests --with-coverage` to run the tests with coverage information.

## To Do
- Load people from unallocated list once new rooms become availabe

## License
Amity uses the MIT license. Feel free to fork the repo and add your awesome features. Feel free to open issues incase you spot bugs.