'''
#TEST
form = tk.Frame()
label = tk.Label(form, text='Name')
name_input = tk.Entry(form)
label.grid(row=0, column=0)
name_input.grid(row=1, column=0)
'''
from datetime import datetime
import os
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from decimal import Decimal, InvalidOperation
import requests
import api
import pandas as pd
import googletrans
from googletrans import Translator

api_key = ''

'''
FAIR USE DISCLAIMEr
Since I am new to programming and only learnt basic Python I have taken the basic code for handling fields
and labels (the classes) from the book: Chapter 1-4 from Python GUI Programming with Tkinter, by Alan D. Moore, 2018 (Packt Publishing)
The DataRecordForm class and Application class have been totally re-written and adapted in order to fit the requirements of
the Simple address checking application.
'''

##################
# Widget Classes #
##################

class ValidatedMixin:
    """Adds a validation functionality to an input widget"""

    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.config(
            validate='all',
            validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
            invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d')
        )

    def _toggle_error(self, on=False):
        self.config(foreground=('red' if on else 'black'))

    def _validate(self, proposed, current, char, event, index, action):
        """The validation method.

        Don't override this, override _key_validate, and _focus_validate
        """
        self._toggle_error(False)
        self.error.set('')
        valid = True
        if event == 'focusout':
            valid = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )
        return valid

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_invalid(event=event)
        elif event == 'key':
            self._key_invalid(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )

    def _focusout_invalid(self, **kwargs):
        """Handle invalid data on a focus event"""
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        """Handle invalid data on a key event.

        By default we want to do nothing
        """

        pass

    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid


class DateEntry(ValidatedMixin, ttk.Entry):

    def _key_validate(self, action, index, char, **kwargs):
        valid = True

        if action == '0':  # This is a delete action
            valid = True
        elif index in ('0', '1', '2', '3', '5', '6', '8', '9'):
            valid = char.isdigit()
        elif index in ('4', '7'):
            valid = char == '-'
        else:
            valid = False
        return valid

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            self.error.set('A value is required')
            valid = False
        try:
            datetime.strptime(self.get(), '%Y-%m-%d')
        except ValueError:
            self.error.set('Invalid date')
            valid = False
        return valid


class RequiredEntry(ValidatedMixin, ttk.Entry):

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
        return valid


class ValidatedCombobox(ValidatedMixin, ttk.Combobox):

    def _key_validate(self, proposed, action, **kwargs):
        valid = True
        # if the user tries to delete,
        # just clear the field
        if action == '0':
            self.set('')
            return True

        # get our values list
        values = self.cget('values')
        # Do a case-insensitve match against the entered text
        matching = [
            x for x in values
            if x.lower().startswith(proposed.lower())
        ]
        if len(matching) == 0:
            valid = False
        elif len(matching) == 1:
            self.set(matching[0])
            self.icursor(tk.END)
            valid = False
        return valid

    def _focusout_validate(self, **kwargs):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
        return valid


class ValidatedSpinbox(ValidatedMixin, tk.Spinbox):

    def __init__(self, *args, min_var=None, max_var=None,
                 focus_update_var=None, from_='-Infinity', to='Infinity',
                 **kwargs):
        super().__init__(*args, from_=from_, to=to, **kwargs)
        self.resolution = Decimal(str(kwargs.get('increment', '1.0')))
        self.precision = self.resolution.normalize().as_tuple().exponent
        # there should always be a variable,
        # or some of our code will fail
        self.variable = kwargs.get('textvariable') or tk.DoubleVar()

        if min_var:
            self.min_var = min_var
            self.min_var.trace('w', self._set_minimum)
        if max_var:
            self.max_var = max_var
            self.max_var.trace('w', self._set_maximum)
        self.focus_update_var = focus_update_var
        self.bind('<FocusOut>', self._set_focus_update_var)

    def _set_focus_update_var(self, event):
        value = self.get()
        if self.focus_update_var and not self.error.get():
            self.focus_update_var.set(value)

    def _set_minimum(self, *args):
        current = self.get()
        try:
            new_min = self.min_var.get()
            self.config(from_=new_min)
        except (tk.TclError, ValueError):
            pass
        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)
        self.trigger_focusout_validation()

    def _set_maximum(self, *args):
        current = self.get()
        try:
            new_max = self.max_var.get()
            self.config(to=new_max)
        except (tk.TclError, ValueError):
            pass
        if not current:
            self.delete(0, tk.END)
        else:
            self.variable.set(current)
        self.trigger_focusout_validation()

    def _key_validate(self, char, index, current, proposed, action, **kwargs):
        valid = True
        min_val = self.cget('from')
        max_val = self.cget('to')
        no_negative = min_val >= 0
        no_decimal = self.precision >= 0
        if action == '0':
            return True

        # First, filter out obviously invalid keystrokes
        if any([
                (char not in ('-1234567890.')),
                (char == '-' and (no_negative or index != '0')),
                (char == '.' and (no_decimal or '.' in current))
        ]):
            return False

        # At this point, proposed is either '-', '.', '-.',
        # or a valid Decimal string
        if proposed in '-.':
            return True

        # Proposed is a valid Decimal string
        # convert to Decimal and check more:
        proposed = Decimal(proposed)
        proposed_precision = proposed.as_tuple().exponent

        if any([
            (proposed > max_val),
            (proposed_precision < self.precision)
        ]):
            return False

        return valid

    def _focusout_validate(self, **kwargs):
        valid = True
        value = self.get()
        min_val = self.cget('from')
        max_val = self.cget('to')

        try:
            value = Decimal(value)
        except InvalidOperation:
            self.error.set('Invalid number string: {}'.format(value))
            return False

        if value < min_val:
            self.error.set('Value is too low (min {})'.format(min_val))
            valid = False
        if value > max_val:
            self.error.set('Value is too high (max {})'.format(max_val))

        return valid

##################
# Module Classes #
##################


class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    def __init__(self, parent, label='', input_class=ttk.Entry,
                 input_var=None, input_args=None, label_args=None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = input_var

        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)
        self.error = getattr(self.input, 'error', tk.StringVar())
        self.error_label = ttk.Label(self, textvariable=self.error)
        self.error_label.grid(row=2, column=0, sticky=(tk.W + tk.E))

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        if self.variable:
            return self.variable.get()
        elif type(self.input) == tk.Text:
            return self.input.get('1.0', tk.END)
        else:
            return self.input.get()

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
                self.variable.set(bool(value))
        elif self.variable:
                self.variable.set(value, *args, **kwargs)
        elif type(self.input).__name__.endswith('button'):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)


class DataRecordForm(tk.Frame):
    """The input form for our widgets"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # A dict to keep track of input widgets
        self.inputs = {}

        # Build the form
        # recordinfo section
        recordinfo = tk.LabelFrame(self, text="Address Information")

        # line 1
        self.inputs['countrycode'] = LabelInput(
            recordinfo, "Country Code",
            input_class=ValidatedCombobox,
            input_var=tk.StringVar(),
            input_args = {"values": ["SE", "NO", "DK", "FI"]}
       )
        self.inputs['countrycode'].grid(row=0, column=0)

        self.inputs['street'] = LabelInput(
            recordinfo, "Postal Address",
            input_class=RequiredEntry,
            input_var=tk.StringVar()
        )
        self.inputs['street'].grid(row=0, column=1,sticky="we")

        # line 2
        self.inputs['postalcode'] = LabelInput(
            recordinfo, "Postal Code",
            input_class=ValidatedCombobox,  ##dropdown list of zip codes, but it is slow!
            input_var=tk.StringVar(),
            input_args={"values": [str(x) for x in range(10000, 99999, 1)]}
            #input_class = ValidatedSpinbox,
            #input_var = tk.IntVar(),
            #input_args = {"from_": '10000', "to": '99999', "increment": '1'}
        )
        self.inputs['postalcode'].grid(row=1, column=0)


        self.inputs['locality'] = LabelInput(
            recordinfo, "Locality",
            input_class=RequiredEntry,
            input_var=tk.StringVar()
        )
        self.inputs['locality'].grid(row=1, column=1)

        recordinfo.grid(row=1, column=0, sticky="we")

        # default the form
        self.reset()

    def get(self):
        """Retrieve data from form as a dict"""

        # We need to retrieve the data from Tkinter variables
        # and place it in regular Python objects

        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        """Resets the form entries"""

        # gather the default entered value
        c_code = self.inputs['countrycode'].get()

        # clear all values
        for widget in self.inputs.values():
            widget.set('')

        self.inputs['countrycode'].input.focus()

        if c_code not in ('',):
            self.inputs['countrycode'].set(c_code)
            self.inputs['street'].input.focus()

    def get_errors(self):
        """Get a list of field errors in the form"""

        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()

        return errors

class Application(tk.Tk):
    """Application root window"""
    #modified and adapted to work with checking postal addresses at geposit.se

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("SACA - Simple Address Checking Application")
        self.resizable(width=True, height=True)

        ttk.Label(self, text="SACA - Simple Address Checking Application", font=("TkDefaultFont", 16)).grid(row=0)

        self.records_saved = 0
        self.records_checked = 0
        self.record_correct = tk.StringVar()
        self.record_correct.set('disabled') # parameter in order to check if record is correct before saving.

        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=20)

        self.checkbutton = ttk.Button(self, text="Check", command=self.on_check)
        self.checkbutton.grid(sticky="e",row=2, column=0, padx=10, pady=5)

        button_state = self.record_correct.get()
        # print(button_state + 'after') #testing if the button_state has changed after check button

        self.savebutton = ttk.Button(self, text="Save", state = button_state, command=self.on_save)
        self.savebutton.grid(sticky="e", row=2, column=1, padx=10, pady=5)

        self.samplesbutton =ttk.Button(self, text="Show Samples", command=self.on_show_samples)
        self.samplesbutton.grid(sticky="e",row=2, column=2, padx=10, pady=15)

        self.savedbutton =ttk.Button(self, text="Show Saved", command=self.on_show_saved)
        self.savedbutton.grid(sticky="e",row=2, column=3, padx=10, pady=15)


        # status bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky="w", row=3, padx=10)


    def on_check(self):
        '''Checks if errors in fields, takes data and appends definition of format string=json, and appends
        string with API-key'''

        errors = self.recordform.get_errors()
        if errors:
            self.status.set(
                "Cannot check, error in fields: {}"
                    .format(', '.join(errors.keys()))
            )
            return False

        data = self.recordform.get()
        #print(data) # print to test function during development
        #fetch api_key from file # Milestone 1b: hash the key
        api_key = api.key
        # append format (json) and API-key to data in order to get the call to succeed.
        data.update({'response_format': 'json' , 'api_key': api_key})

        #add country code from form in order to put it at the end of the URL in request.post()
        c_code = data['countrycode']
        c_code = c_code.lower()
        #print(c_code) test lower

        #delete counctrycode element from data
        del data['countrycode']

        #print(data) #test to see if it appends correctly

        self.records_checked += 1

        #add country code to URL
        #use data from record to check address with geposit.se
        response = requests.post('https://valid.geposit.se/1.7/validate/address/'+c_code, data=data)
        response.raise_for_status()
        #receive data back from geposit.se and assign it to data
        data = response.json()

        if ((int)(data['response']['is_valid']) == 1):
            #print("Address is correct") # testing
            self.status.set("Address is correct.     {} records checked this session".format(self.records_checked))
            # print(data) testing
            self.savebutton['state'] = tk.NORMAL
        else:
            #print("Address is incorrect") # print to test function during development
            self.savebutton['state'] = tk.DISABLED
            # print(data) #testing
            error=str(data['response']['errors'])
            translator = Translator()
            translated = translator.translate(text=error, src='sv')
            self.status.set("Address is incorrect, Error: " + translated.text + "\n" + "{} records checked this session".format(self.records_checked))

            #print("Errors in address") # print to test function during development
            #print(data['response']['errors'])# print to test function during development

            suggestions = data['response']['suggestions']
            suggest = suggestions[0] # take out dictionary from list
            # print(suggestions) # testing
            #print(suggest) #testing
            street = suggest.get('street') + ' ' + suggest.get('street_number') + '' + suggest.get(
                'extra_number') + '' + suggest.get('letter')
            postalcode = suggest.get('postalcode')
            locality = suggest.get('locality')
            suggested_address = street + ' ' + postalcode + ' ' + locality
            #print(street) #testing
            #print(postalcode) # testing
            #print(locality) # testing

            messagebox.showinfo("Try the following address:", suggested_address)

            #print("Suggestion(s) to use instead:")
            #print(data['response']['suggestions']) # this I want to Display on separate window if possible


    def on_save(self):
        """Handles save button clicks"""

        # Check for errors first

        errors = self.recordform.get_errors()
        if errors:
            self.status.set(
                "Cannot save, error in fields: {}"
                    .format(', '.join(errors.keys()))
            )
            return False

        # save to a hardcoded filename with a datestring.
        # If it doesnt' exist, create it,
        # otherwise just append to the existing file
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "addresses_{}.csv".format(datestring)
        newfile = not os.path.exists(filename)

        data = self.recordform.get()
        #print(data) # print to test function during development

        with open(filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

        self.records_saved += 1
        self.status.set(
            "{} records saved this session".format(self.records_saved))
        self.recordform.reset()
        self.savebutton['state'] = tk.DISABLED


    def on_show_saved(self):
        '''opens text widget to show saved correct address'''

        window = tk.Tk()
        window.title("Saved correct addresses")
        window.geometry('500x400+805+50')
        txt = scrolledtext.ScrolledText(window, width=100, height=100)
        txt.grid(column=1, row=0)
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "addresses_{}.csv".format(datestring)
        saved_txt = pd.read_csv(filename, delimiter=",", encoding="ISO-8859-1")

        txt.insert('insert', saved_txt)


    def on_show_samples(self):
        '''opens text widget to show samples of address to use for testing'''

        window = tk.Tk()
        window.title("A sample of Swedish addresses (correct and incorrect)")
        window.geometry('500x400+300+350')
        txt = scrolledtext.ScrolledText(window, width=100, height=100)
        txt.grid(column=1, row=0)
        sample_txt = pd.read_csv("sample_addresses.csv", delimiter=",", encoding="ISO-8859-1")

        txt.insert('insert', sample_txt)



if __name__ == "__main__":

    app = Application()
    app.mainloop()