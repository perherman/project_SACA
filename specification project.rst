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
*   Valid street address including number & alpha code/stairwell/apartment, in combination with zip code and locality
*   Valid Box number, in combination with zip code and locality
*   A combination of all items in an address should be validated in order to be able to save the address.
*   When clicking Check address the message "The address is correct", or the address in incorrect will be displayed, and if
    incorrect it will give the error code and errormessage indicating which element of the address is incorrect.
*   If address entered is incorrect a message window suggest the correct address
*   A correct address can saved to a local CSV-file. If the address is incorrect it should not be possible to save the adress
*   The CSV-file with saved addresses should be able to be viewed by the user by clicking a View Saved Addresses button.
*   For demonstration purposes a file with sample Swedish addresses can be viewed by clicking a View Sample Adresses button.

The program must:
.................
*   have inputs that:

    -   ignore meaningless keystrokes
    -   require a value for all fields
    -   get marked with an error if the value is invalid on focusout
*   prevent saving record when errors are present
*   prevent checking the record if any field is blank or has invalid characters, and give a warning
*   It should be possible to use the application without the use of mouse, i.e. just using keyboard inputs.

Functionality not required in version 1
_______________________________________
In this first version the following functions are not required, but will be released in coming versions:

*   Auto update of locality after entering the zip code, and after checking that the
    street & number /Box & number are valid for the entered zipcode
*   Auto update of Zip Code from the entered street name and locality
*   Auto suggestion & completion of street name at time of entry in the SACA Windows Application in a scroll list
    with the ability to choose which address, and get the correct zip code and locality updated in respective field.
*   Ability to fully test Norwegian, Danish or Finnish addresses with postal codes starting with 0.
*   The functionality above working directly with the Oracle Database, while accessing one address at a time
    for example:
    -	Auto update of correct zip code from a current street name & number + locality (or Box address) in the Oracle database

Limitations
___________
This first version runs in a stand alone Windows window, and cannot update the valid values directly in to the CRM database.
The first version will not have separate fields for the address, number or alpha code/no of stairs/apartment, rather
they will be in a field for the full combination.

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
*   A check button activates the command to check the address against www.geposit.se authenticating with an API-key
*   A save button activates the command to save the data of the address to a local address file
*   A display button displays saved data to a separate window on screen
*   A display button displays Samples of Swedish addresses to a separate window on screen
*   The API-key which is necessary for authentification is contained in a local text-file and read before calling the API at geposit.se
    in coming version the API-key will be stored in a hashed file.

Layout
------
*   The layout should resemble the layout of the current Windows CRM-system
    (written in the low code tool Magic XPA). In Milestone 1 the layout is acceptable, but not good

    Layout of current Windows CRM-system: se attachment Layout SACA.jpg




