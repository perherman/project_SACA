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

Authors
=======

Per-Olof Hermansson, 2020

Requirements
============

* Python 3
* Tkinter

Usage
=====

To start the application, run::

   py SACA/project.py


General Notes
=============

The CSV file will be saved to your current directory in the format "addresses_CURRENTDATE.csv", where CURRENTDATE is today's date in ISO format.

This program only appends to the CSV file.  You should have a spreadsheet program installed in case you need to edit or check the file.


SPECIFICATION
=============

Functionality required
______________________

The ability to check if a Swedish address has the following valid items:
•	Valid postal code
•	Valid locality (town, city, village etc)
*   Valid street address including number & alpha code/stairwell/apartment

Also a combination of several items in an address should be validated
•	Valid street address including number, in combination with zip code and locality
•	Valid Box number, in combination with zip code and locality

The program must:
.................

• have inputs that:
  - ignore meaningless keystrokes
  - require a value for all fields
  - get marked with an error if the value is invalid on focusout
• prevent checking the address or saving record when errors are present

Functionality not required in version 1
_______________________________________
In this first version the following functions are not required, but will be released in coming versions:
•   Auto update of locality after entering the zip code, and after checking that the
    street & number /Box & number are valid for the entered zipcode
•	Auto update of Zip Code from the entered street name and locality
•	Auto suggestion & completion of street name at time of entry in the SACA Windows Application in a scroll list
    with the ability to choose which address, and get the correct zip code and locality updated in respective field.
•	Ability to test Norwegian, Danish or Finnish addresses.
•  The functionality above working directly with the Oracle Database, while accessing one address at a time
    for example:
    -	Auto update of correct zip code from a current street name & number + locality (or Box address) in the Oracle database
    -
Limitations
___________
This first version runs in a stand alone Windows window, and cannot update the valid values directly in to the CRM database.
The first version will not have separate fields for the address, number or alpha code/no of stairs/apartment.
The application should be able to run without the use of mouse, i.e. just using keyboard inputs.

Data Dictionary
_______________
The following items of data are required in the application:
Country Code (string, 2, UU): ttk.Listbox
    default is ‘SE’ in the first version, in future also: ‘NO’, ‘FI’, ‘DK’)
Zip Code (string, 5 digits, 10000-99999: ttk.Listbox
    (in future it should also check the length of NO, FI and Dk which is 4 digits)
Postal Address (string, 35, U+34lower case: ttk.Entry
    either a street or village address with number or a box with number, including alpha code)
Locality (string, 35, U+34lower case, City, town, village): ttk.Entry
In future version also Regional Code (LKF, string 6, and A-region, string 2): ttk.Entry

Labels for the fields: ttk.LabelFrame
Labels above fields (in order to make alignment of fields easier)

Layout: se attachment SACA.jpg

