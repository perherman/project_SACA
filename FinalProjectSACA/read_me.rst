========================================================================================================================
Final project Code in Place: SACA - Simple Address Checking Application
========================================================================================================================

Description
-----------
For my final project in Code in Place I have chosen to solve a real world problem that I have when I
manage a CRM-database. The problem is that people often give the wrong Zip code (called Postal Code in Sweden)
Ultimately I want to integrate the solution in the CRM-system itself. But Milestone 1 is to have it running
in a stand alone Windows Frame with the ability to enter an address, and check the validity of the entered combination
of street with number and alpha code, postal code and locality (city, town, village).
In this first version it only checks Swedish addresses, but Milestone 2 is to enable it to check the validity
of Danish, Norwegian and Finnish addresses as well. If you enter a Norwegian, Danish or Finnish address where the  postal
code is greater than 1000 it will however work.
The validity is checked against the official address database of Sweden which is publicized on a web site (which also
contains addresses in the other nordic countries.
To access the web site and check validity of an address one needs an API-key.

Features
--------
* Provides a validated entry form to ensure correct data
* Ability to check and validate registered address against the official Swedish zip code register
* Stores corrected data to CSV files # Milestone 1b: only correct addresses can be stored
* Auto-fills form fields whenever possible
* Ability to view saved correct addresses from the CSV-file # Milestone 1b
* The application uses keyboard inputs. So using the mouse is not necessary.

Authors
-------
Per-Olof Hermansson, perolof@gmail.com, 2020

Fair Use Disclaimer
-------------------
Since I am new to programming and only learnt basic Python I have taken the basic code for handling fields
and labels (the classes) from the book: Python GUI Programming with Tkinter, by Alan D. Moore, 2018 (Packt Publishing)
The DataRecordForm class and Application class have been re-written and adapted in order to fit the requirements of
the Simple address checking application.

Requirements
============
* Python 3
* Tkinter
* datetime
* os
* csv
* decimal
* requests
* pandas
* a valid API-key from www.geposit.se  / if the one supplied here is no longer valid you can apply for a
    trial API at https://www.postnummerservice.se/utbud/valid-adressvalidering/bestall   klick on Demo and
    enter your name, email and address. The API-key is kept in a separate file.  #Milestone 1b: keep API-key in hashed text file

Usage
=====
To start the application, run::

   py SACA/project.py


General Notes
=============
The CSV file will be saved to your current directory in the format "addresses_CURRENTDATE.csv", where CURRENTDATE is today's date in ISO format.

This program only appends to the CSV file.  You should have a spreadsheet program installed in case you need to edit the file.
Milestoned 1B: The file can be displayed on screen if you press the Display button.
