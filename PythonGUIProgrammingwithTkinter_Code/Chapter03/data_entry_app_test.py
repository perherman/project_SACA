from datetime import datetime
import os
import csv
import tkinter as tk
from tkinter import ttk


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
        recordinfo = tk.LabelFrame(self, text="Record Information")

        # line 1
        self.inputs['Co Code'] = LabelInput(
            recordinfo, "Co Code",
            input_var=tk.StringVar()
        )
        self.inputs['Co Code'].grid(row=0, column=0)

        self.inputs['Post Address'] = LabelInput(
            recordinfo, "Post Address",
            input_var=tk.StringVar()
        )
        self.inputs['Post Address'].grid(row=0, column=1, columnspan=3)

        # line 2
        self.inputs['Zip Code'] = LabelInput(
            recordinfo, "Zip Code",
            input_var=tk.StringVar()
        )
        self.inputs['Zip Code'].grid(row=1, column=0)
        self.inputs['Locality'] = LabelInput(
            recordinfo, "Locality",
            input_var=tk.StringVar()
        )
        self.inputs['Locality'].grid(row=1, column=1)

        recordinfo.grid(row=0, column=0, sticky=(tk.W + tk.E))

        self.reset()

        # default the form
        #self.reset()

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

        # clear all values
        for widget in self.inputs.values():
            widget.set('')


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("SACA - Simple Address Checking Application")
        self.resizable(width=False, height=False)

        ttk.Label(self, text="SACA - Simple Address Checking Application", font=("TkDefaultFont", 16)).grid(row=0)

        self.recordform = DataRecordForm(self)
        self.recordform.grid(row=1, padx=10)

        self.savebutton = ttk.Button(self, text="Save", command=self.on_save)
        self.savebutton.grid(sticky=tk.E, row=2, padx=10)

        # status bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky=(tk.W + tk.E), row=3, padx=10)

        self.records_saved = 0

    def on_save(self):
        """Handles save button clicks"""

        # For now, we save to a hardcoded filename with a datestring.
        # If it doesnt' exist, create it,
        # otherwise just append to the existing file
        datestring = datetime.today().strftime("%Y-%m-%d")
        filename = "adresses_{}.csv".format(datestring)
        newfile = not os.path.exists(filename)

        data = self.recordform.get()

        with open(filename, 'a') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

        self.records_saved += 1
        self.status.set(
            "{} records saved this session".format(self.records_saved))
        self.recordform.reset()


if __name__ == "__main__":

    app = Application()
    app.mainloop()
