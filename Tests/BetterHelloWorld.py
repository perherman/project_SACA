"""A better Hello World for Tkinter"""

import tkinter as tk
from tkinter import ttk

#create subclass
class HelloView(tk.Frame):
    #A friendly module

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.name = tk.StringVar()
        self.hello_string = tk.StringVar()
        self.hello_string.set("Hello World!")

        #my_text_var="HejsanSvejsan" #Test

        name_label = ttk.Label(self, text="Name:")
        name_entry = ttk.Entry(self, textvariable=self.name)
        #my_entry = ttk.Entry(parent, textvariable=my_text_var)   # TEST
        ch_button = ttk.Button(self, text="Change", command=self.on_change)
        hello_label = ttk.Label(self, textvariable=self.hello_string,
            font=("TkDefaultFont", 36), wraplength=600)

        # Layout form
        name_label.grid(row=0, column=0, sticky=tk.W)
        name_entry.grid(row=0, column=1, sticky=(tk.W + tk.E))#book has no parethesis
        #my_entry.grid(row=0, column=1, sticky=(tk.W +tk.E))   #TEST
        ch_button.grid(row=0, column=2, sticky=tk.E)
        hello_label.grid(row=1, column=0, columnspan=3)
        self.columnconfigure(1, weight=1)

    def on_change(self):
        #handle change button clicks
        if self.name.get().strip():
            self.hello_string.set("Hej " + self.name.get())
        else:
            self.hello_string.set("Hello World")


class MyApplication(tk.Tk):
    #Hello world main application

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Set windows properties
        self.title("Mitt första Pythonprogram i Windows")
        self.geometry("800x600")
        self.resizable(width=True, height=True)

        #set UI
        HelloView(self).grid(sticky=(tk.E + tk.W + tk.N + tk.S))
        self.columnconfigure(0, weight=1)



if __name__ == '__main__':
    app = MyApplication()
    app.mainloop()





