# University of Michigan Climbing Club Carpool Scheduling Software
Initially Written by Nathan Silverman (nzsilver@umich.edu) in Summer 2019.
# Installing the program
To install the program, type the following command in the top level directory where the `setup.py` file is:

`pip install -e .`

# Running the program
To run the program, clone the git repository and run the python package `scheduler` by typing `python3 scheduler` into the terminal.

Running the program will pull results from the spreadsheet results file that is defined in the `__main__.py` file. The dues sheet which riders are cross referenced against is also defined in the `__main__.py` file.

Running the program requires a secrets.json file that is the key to a service account for the google developer console project. To get this setup, access needs to be granted by a system admin. Contact Nathan Silverman (nzsilver@umich.edu) for this.

# Contribution Guidelines
Contributions are welcome. Anyone who wants to help improve this project should contribute! To get started, look in the github issues for ideas of what to help with. Please comment on an issue if you are working on it, and assign yourself to it. When it is ready for production, make a pull request.

For any contribution questions, please email Nathan Silverman at nzsilver@umich.edu

# Development Notes
This program is designed to facilitate carpools for the University of Michigan Climbing Club. This program gets information from a google spreadsheet that collects data about when club members want to drive to the gym, and matches riders with the best drivers in a fair manner. The algorithm for choosing a rider is based on selecting a random rider, and then finding the best driver that has seats left in their vehicle.The best driver is defined as a driver that wants to leave at a similar time and similar location.

The forms and spreadsheets used are found [here](https://drive.google.com/drive/u/0/folders/1j1w_0k5bIgqxJfmQmxbZZoGr66fJT4Y4). For any access issues, contact Nathan Silverman (nzsilver@umich.edu).

## Code structure
### `__main__.py`
* Calls from `read_responses.py` to generate lists for tues_riders, tues_drivers, thurs_riders, thurs_drivers, sun_riders, and sun_drivers based on input from the google form
* Capool responses spreadsheet and dues spreadsheet defined in this file


### `read_responses.py`
* Uses Google API to pull data from carpool responses spreadsheet and dues spreadsheet (names assigned in `__main__.py`)
* Performs validation checks to make sure data from forms have necessary fields and all riders have paid dues

### `generate_rides.py`
* Matches riders with drivers, based on an algorithm that randomly selects riders and pairs them with their best matched available driver

### `print_responses.py`
* Prints results of pairing drivers with riders
* Eventually, this should post results to a google sheet. For now it prints to stdout

### classes/`Dept_Time.py`
* Enum defining different possible departure times

### classes/`Driver.py`
* Class defining different aspects of a driver

### classes/`Loc.py`
* Enum defining different possible departure locations

### classes/`Rider.py`
* Class defining different aspects of a rider

## Working/ Authenticating with Google
[This](https://pbpython.com/pandas-google-forms-part1.html) is a great resource and starting point to integrate into Google sheets with. The google sheets API also has to be enabled from the google developer console. A few of the lines of code in the article are outdated, and have been updated in the code.

To get access to this authentication, you will need to be added to the project. For this, contact Nathan Silverman (nzsilver@umich.edu)
