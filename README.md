# University of Michigan Climbing Club Carpool Scheduling Software

Initially Written by Nathan Silverman (nzsilver@umich.edu) in Summer 2019.
Version 2.0 is under development currently

## Installing the program

To install the program, type the following command in the top level directory where the `setup.py` file is:

`pip install -e .`

## Running the program

To run the program, clone the git repository and run the python package `scheduler` by typing `python3 scheduler` into the terminal.

Running the program will pull results from the spreadsheet results file that is defined in the `__main__.py` file. The dues sheet which riders are cross referenced against is also defined in the `__main__.py` file.

Running the program requires a secrets.json file that is the key to a service account for the google developer console project. To get this setup, access needs to be granted by a system admin. Contact Nathan Silverman (nzsilver@umich.edu) for this.

## Contribution Guidelines

Contributions are welcome. Anyone who wants to help improve this project should contribute! To get started, look in the github issues for ideas of what to help with. Please open an issue if you are working on it, and assign yourself to it. Then fork the repo, and make changes on a branch. When the changes are good, you can make a pull request and it can be approved to merge back into the main project.

For any contribution questions, please email Nathan Silverman at nzsilver@umich.edu

To be added as a collaborator on the project, talk with Nathan Silverman.

## Discord Channel

A discord channel can be joined with the code: 7q8C9NF

This should be used for all communication about the project, along with github issues.

## Development Notes

This program is designed to facilitate carpools for the University of Michigan Climbing Club. This program gets information from a google spreadsheet that collects data about when club members want to drive to the gym, and matches riders with the best drivers in a fair manner. The algorithm for choosing a rider is based on selecting a random rider, and then finding the best driver that has seats left in their vehicle.The best driver is defined as a driver that wants to leave at a similar time and similar location.

The forms and spreadsheets used are found [here](https://drive.google.com/drive/u/0/folders/1j1w_0k5bIgqxJfmQmxbZZoGr66fJT4Y4). For any access issues, contact Nathan Silverman (nzsilver@umich.edu).

## Working/ Authenticating with Google

[This](https://pbpython.com/pandas-google-forms-part1.html) is a great resource and starting point to integrate into Google sheets with. The google sheets API also has to be enabled from the google developer console. A few of the lines of code in the article are outdated, and have been updated in the code.

To get access to this authentication, you will need to be added to the project. For this, contact Nathan Silverman (nzsilver@umich.edu)
