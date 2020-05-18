========================================================================================================================
SACA - Simple Address Checking Application
========================================================================================================================

Description
-----------

A simple application to enable a CRM database user to check the validity of Swedish addresses.
The validity is checked against the official address database (including zip codes) of Sweden which is publicized on a web site.

Features
--------

* Provides a validated entry form to ensure correct data
* Ability to check and validate registered address against the official Swedish zip code register
* Stores corrected data to CSV files
* Auto-fills form fields whenever possible
* Ability to view saved correct addresses from the CSV-file

Authors
-------

Per-Olof Hermansson, perolof@gmail.com, 2020

Disclaimer
----------
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
trial API at https://www.postnummerservice.se/utbud/valid-adressvalidering/bestall   klick on Demo and enter your name, email and address.

Usage
=====

To start the application, run::

   py SACA/project.py


General Notes
=============

The CSV file will be saved to your current directory in the format "addresses_CURRENTDATE.csv", where CURRENTDATE is today's date in ISO format.

This program only appends to the CSV file.  You should have a spreadsheet program installed in case you need to edit the file.
However the file can be displayed on screen if you press the Display button.
