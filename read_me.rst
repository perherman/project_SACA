========================================================================================================================
Final project Code in Place: SACA - Simple Address Checking Application
========================================================================================================================

Description
-----------
For my final project in Code in Place I have chosen to solve a real world problem that I have when I
manage a CRM-database. The problem is that people often give the wrong Zip code (called Postal Code in Sweden)
Ultimately I want to integrate the solution in the CRM-system itself (Milestone 3). But Milestone 1 is to have it running
in a stand alone Windows Frame with the ability to enter an address, and check the validity of the entered combination
of street with number and alpha code, postal code and locality (city, town, village).

The validity is checked against the official address database of Sweden which is publicized on a web site (which also
contains addresses in the other nordic countries).
To access the web site and check validity of an address one needs an API-key.

In this first version it only checks Swedish addresses, but Milestone 2 is to enable it to fully check the validity
of Danish, Norwegian and Finnish addresses as well. However, if you enter a Norwegian, Danish or Finnish address
where the  postal code is greater than 1000 it will work. I supply a CSV-file with a number of Swedish addresses that
you can use while trying the application. Some of them are correct, and some of the are incorrect.
After entering a correct address, you can save it to a CSV-file. The Save button is otherwise disabled.
If you enter an incorrect address you will get an error message with the cause of the error, originally in Swedish.
The translation of the error messages are done with Googletrans, and it does not always make a perfect translation.

Features
--------
*   Ability to check and validate registered address against the official Swedish zip code register
*   If address entered is incorrect it gives an error message with info of what is wrong, and also a messagewindow suggesting
        the correct address
*   Translates error codes from Swedish to English using Googletrans
*   Provides a validated entry form to ensure correct data
*   Stores corrected data to CSV files
*   Ability to view a sample of Swedish addresses, both correct and incorrect, for foreign users so that they can test the application
*   Auto-fills form fields whenever possible, in this version the Country code.
*   Ability to view saved correct addresses from the CSV-file
*   The application uses keyboard inputs. So using the mouse is not necessary


Authors
-------
Per-Olof Hermansson, perolof@gmail.com, 2020

Fair Use Disclaimer
-------------------
Since I am new to programming and only learnt basic Python I have taken the basic code for handling fields
and labels (the classes) from the book: Chapter 1-4 from Python GUI Programming with Tkinter, by Alan D. Moore, 2018 (Packt Publishing)
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
* googletrans (Translator)
* api (file with API-key to access www.geposit.se database)
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

