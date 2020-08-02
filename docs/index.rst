.. Michigan Climbing Club Carpool Scheduler documentation master file, created by
   sphinx-quickstart on Sat Jul 18 18:11:17 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Michigan Climbing Club Carpool Scheduler's documentation!
====================================================================

The carpool scheduling software is designed to fairly match drivers and riders going to Planet Rock (a local climbing gym in Ann Arbor) with carpools that match both the driver and riders unique date, time, and location preferences. 

The software relies on data collection from drivers and riders to happen through a google form. The responses collected in the google form are stored in a google sheet. The program is then able to read these responses, and fairly match drivers and riders. Once results are calculated, the program will publish its results to a google sheet. The program is designed to give carpool seat priority to due paying club members seeking a ride, while also ensuring that all due paying members have an equal chance at getting a ride. 
 
This software was designed to solve issues within the Michigan Climbing Club related to fairness and due paying member priority when members tried to get rides to Planet Rock in years past.  Version 1.0.0 of the software has succesfully worked for over a year. Version 2.0.0 is currently under development.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   source/modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
