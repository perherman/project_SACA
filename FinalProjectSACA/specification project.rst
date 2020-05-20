========================================================================================================================
SACA - Simple Address Checking Application
========================================================================================================================

Description
-----------
A simple application to enable a CRM database user to check the validity of Swedish addresses.
The validity is checked against the official address database (including zip codes) of Sweden which
is publicized on a web site via an API which requires an API-key.

Functionality required
______________________
The ability to check if a Swedish address has the following valid items:

*   Valid postal code
*   Valid locality (town, city, village etc)
*   Valid street address including number & alpha code/stairwell/apartment

Also a combination of several items in an address should be validated

*   Valid street address including number, in combination with zip code and locality
*   Valid Box number, in combination with zip code and locality
*   In the first version it will only respond with either "The address is correct", or the address in incorrect, and if
    incorrect it will give the error code and errormessage indicating which element of the address is incorrect.

*   A correct address should be possible to save in a local CSV-file.
*   The CSV-file should be able to be viewed by the user.

The program must:
.................
*   have inputs that:

    -   ignore meaningless keystrokes
    -   require a value for all fields
    -   get marked with an error if the value is invalid on focusout

*   prevent checking the address or saving record when errors are present

Functionality not required in version 1
_______________________________________
In this first version the following functions are not required, but will be released in coming versions:

*   Auto update of locality after entering the zip code, and after checking that the
    street & number /Box & number are valid for the entered zipcode
*   Auto update of Zip Code from the entered street name and locality
*   Auto suggestion & completion of street name at time of entry in the SACA Windows Application in a scroll list
    with the ability to choose which address, and get the correct zip code and locality updated in respective field.
*   Ability to test Norwegian, Danish or Finnish addresses.
*   The functionality above working directly with the Oracle Database, while accessing one address at a time
    for example:
    -	Auto update of correct zip code from a current street name & number + locality (or Box address) in the Oracle database


Limitations
___________
This first version runs in a stand alone Windows window, and cannot update the valid values directly in to the CRM database.
The first version will not have separate fields for the address, number or alpha code/no of stairs/apartment, rather they will be in a field for the full combination.
The application should be able to run without the use of mouse, i.e. just using keyboard inputs.

Data Dictionary
_______________
The following items of data are required in the application:

*   Country Code (string, 2, UU): ttk.Listbox
    default is "SE" in the first version, in future also: "NO", "FI", "DK"
*   Zip Code (string, 5 digits, 10000-99999: ttk.Listbox
    (in future it should also check the length of NO, FI and Dk which is 4 digits)
*   Postal Address (string, 35, U+34lower case: ttk.Entry
    either a street or village address with number or a box with number, including alpha code)
*   Locality (string, 35, U+34lower case, City, town, village): ttk.Entry, check if Alpha
*   In future version also Regional Code (LKF, string 6, and A-region, string 2): ttk.Entry

Labels for the fields: ttk.LabelFrame
Labels above fields (in order to make alignment of fields easier)

Buttons
-------
*   A check button activates the command to check the address against www.geposit.se
*   A save button activates the command to save the data of the address to a local address file
*   A display button activates the command to display the data on screen (using Panda)
*   The API-key which is necessary for authentification will be saved in a local text-file and read before calling the API at geposit.se
    in coming version the API-key will be stored in a hashed file.

Layout
------
*   The layout should resemble the layout of the current Windows CRM-system
    (written in the low code tool Magic XPA). In Milestone 1 the layout is acceptable, but not good

    Layout of current Windows CRM-system: se attachment Layout SACA.jpg




