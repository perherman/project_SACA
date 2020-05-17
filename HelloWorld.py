#import tkinter as tk
from tkinter import *  #imports Tkinter lib, ok for small scripts!
from tkinter.ttk import * #ttk widgets are better looking!


root = Tk() #root or master application, top level window, one per application

label = Label(root, text = "Hello World!") # creates a new label object, a widget for displaying text or image
#with root as parent or master widget, each widget is contained in an other, hierarchy

button = Button(root, text = "Ok")
button2 = Button(root, text = "Avbryt")

label2 = Label(root, text = "Checking Swedish Addresses")

enter = Entry(root, text = "Ange en extra adress!")

label.pack()# places the label widget onto parent widget,  screen
label2.pack()
enter.pack()
button.pack()
button2.pack()

root.mainloop()# main event loop,processes all events, keystrokes, mouse clicks, etc runs until quit.
#usually last line of Tkinter program.




