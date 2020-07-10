# University of Michigan Climbing Club Carpool Scheduling Software
> Carpool Scheduling software used for fairly coordinating carpools to the local climbing gym.


The carpool scheduling software is designed to fairly match drivers and riders going to Planet Rock (a local climbing gym in Ann Arbor) with carpools that match both the driver and riders unique date, time, and location preferences. 

 The software relies on data collection from drivers and riders to happen through a google form. The responses collected in the google form are stored in a google sheet. The program is then able to read these responses, and fairly match drivers and riders. Once results are calculated, the program will publish its results to a google sheet. The program is designed to give carpool seat priority to due paying club members seeking a ride, while also ensuring that all due paying members have an equal chance at getting a ride. 
 
 This software was designed to solve issues within the Michigan Climbing Club related to fairness and due paying member priority when members tried to get rides to Planet Rock in years past. This software has succesfully worked for over a year.

 ## Installation
 
To install the program, type the following command in the top level directory where the `setup.py` file is. Make sure you are using python >= 3.5, and `pip` installs for python 3. It may be necessary to use `pip3` instead of `pip` depending on your system.

```
pip install -e . 
```
Notice the period after the e (i.e. installing in your current path)

## Usage
To run:
```
scheduler
```
This will list the available options that can be used to run the program. 

UPDATE THESE TO INCLUDE FINAL PROGRAM OPTIONS AND DESCRIPTIONS

Running the program requires a secrets.json file that is the key to a service account for the google developer console project. This is needed to allow the program to communicate with google drive. To get this setup, access needs to be granted by a system admin. Contact Nathan Silverman or Roberts Kalnins for this. 

## Development Setup
All developers should be using python >=3.5, have a `secret.json` file, and should have run the installation step above. See note above about obtaining a `secret.json` file.

## Contribution Guidelines

Contributions are welcome. Anyone who wants to help improve this project should contribute! Please follow the following steps to contribute.

1. Check Github issues. If needed, create a new issue with what problem/ feature you are solving or adding
1. Fork the repo
1. Create your branch (`git checkout -b feature/fooBar`)
1. Do the work. Add tests if needed to verify your work is correct.
1. Format code
1. Run tests
1. Commit your changes
1. Push to the new branch
1. Create a new pull request

### Formatting
This project is formatted using the [black](https://github.com/psf/black) formatter. Please use this before attempting to submit a pull requests. Non formatted code will fail the pull request.

### Testing
Tests for this codebase have been developed using the [nose2](https://docs.nose2.io/en/latest/) testing framework. Please add tests for new features you contribute, and ensure that any code you add does not break the codebase. 

To run tests, run the following command from the top level directory.
```
nose2
```

### Python Guide
The [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md) is used in this project. Please keep code consistent with the style guide.

### Documentation
Code should be documented well according to the Google Python Style Guide. Documentation should be written in the form of docstrings primarily. Code should also be clearly commented. See [this](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings) section of Googles documentation for docstring guidelines. For more information about documenting python code, see [this] (https://realpython.com/documenting-python-code/) article.

## Discord Channel

A discord channel has been set up for communication between developers. It can be joined with the code: 7q8C9NF

## Revision History
* 1.0.0
  * Initial version. This version worked succesfully for the 2019 - 2020 school year. This version was developed by Nathan Silverman. Thank you to Jonah Rosenblum (jonaher@umich.edu) and Chris Wentland (chriswen@umich.edu) for editing help.

* 2.0.0
  * This version is currently under development. It has been developed by Roberts Kalnins and Nathan Silverman. This version represents a major rewrite of the software from the ground up. It solves many of the issues found from running v1.0.0 for an entire year.

  ## Meta
  Primary contributions by:

  * Nathan Silverman - nzsilverman@gmail.com

  * Roberts Kalnins - rkalnins@umich.edu

  Thank you to all others who have contributed to the development of this project.

  Distributed under the GNU GPL v3 license. See [LICENSE](LICENSE) for more information.