# BeeUI
# Team SNEK
# CSCI 420 - Software Engineering
# Millersville University
#
# BeeUI will immediately display a window upon a constructor call,
# and functionality of the game with begin from there.
#
# IMPORTANT: BeeUI() is called at the bottom of this file for
#            testing purposes, assure that it is removed before
#            utilization in other modules.
#
# Imports:
#    tkinter as tk
#    messagebox from tkinter
#

import tkinter as tk
from tkinter import messagebox

class BeeUI:
    def __init__(self):
        # Placeholder wordPuzzle
        wordPuzzle = ['v', 'o', 'l', 'c', 'a', 'n', 's']

        # Define the window itself
        self.root = tk.Tk()
        # Determine what the window will look like and what it does on close.
        self.root.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.root.geometry("800x500")
        self.root.title("The Spelling Bee! 🐝")

        # Label at the top of the screen
        self.label = tk.Label(self.root, text="Welcome to the Spelling Bee Game!", font=('Arial', 18))
        self.label.pack(padx=20, pady=20)

        # Frame for entry box and backspace button
        self.entryframe = tk.Frame(self.root)
        self.entryframe.columnconfigure(0, weight=1)
        self.entryframe.columnconfigure(1, weight=1)

        # Defining entry box and backspace button.
        self.entry = tk.Entry(self.entryframe, font=('Arial', 12))
        self.entry.bind('<KeyPress>', self.__shortcut)
        self.entry.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.entry.focus()
        self.bckspce = tk.Button(self.entryframe, text="backspace", font=('Arial', 18), command=self.__backspace)
        self.bckspce.grid(row=0, column=1, sticky=tk.W+tk.E)

        # Displaying entryframe on screen.
        self.entryframe.pack(fill='x', padx=250)

        # Submit guess button creation and display
        self.sub = tk.Button(self.root, text="Submit Guess", font=('Arial', 18), command=lambda:self.__submit_guess())
        self.sub.pack(padx=10, pady=10)

        # Creation of frame for the honeycomb
        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)

        # Defining each of the 7 buttons.  btn4 is the required letter.
        self.btn1 = tk.Button(self.buttonframe, text=wordPuzzle[1], font=('Arial', 18), command=lambda:self.__set_text(wordPuzzle[1]))
        self.btn1.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E)

        self.btn2 = tk.Button(self.buttonframe, text=wordPuzzle[2], font=('Arial', 18), command=lambda:self.__set_text(wordPuzzle[2]))
        self.btn2.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.btn3 = tk.Button(self.buttonframe, text=wordPuzzle[3], font=('Arial', 18), command=lambda:self.__set_text(wordPuzzle[3]))
        self.btn3.grid(row=1, column=1, sticky=tk.W+tk.E)

        self.btn4 = tk.Button(self.buttonframe, text=wordPuzzle[0], font=('Arial', 18), command=lambda:self.__set_text(wordPuzzle[0]))
        self.btn4.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E)

        self.btn5 = tk.Button(self.buttonframe, text=wordPuzzle[4], font=('Arial', 18), command=lambda:self.__set_text(wordPuzzle[4]))
        self.btn5.grid(row=3, column=0, sticky=tk.W+tk.E)

        self.btn6 = tk.Button(self.buttonframe, text=wordPuzzle[5], font=('Arial', 18), command=lambda:self.__set_text(wordPuzzle[5]))
        self.btn6.grid(row=3, column=1, sticky=tk.W+tk.E)

        self.btn7 = tk.Button(self.buttonframe, text=wordPuzzle[6], font=('Arial', 18), command=lambda:self.__set_text(wordPuzzle[6]))
        self.btn7.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E)

        # Display the honeycomb frame to window
        self.buttonframe.pack(fill='x', padx=250)
 
        # # # # # # # # # # # # # Menus # # # # # # # # # # # # # 
        # Create Menu bar
        self.menubar = tk.Menu(self.root)

        # File menu options
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Save Current Game")
        self.filemenu.add_command(label="Save Scratch Game")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Load Game")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close", command=self.__on_closing)
        self.filemenu.add_command(label="DEV Close", command=exit)

        # Word Menu for inside of action
        self.lettermenu = tk.Menu(tearoff=0)
        self.lettermenu.add_command(label='set volcanos', command=lambda:self.__set_text('volcanos'))
        self.lettermenu.add_command(label='set volvanos', command=lambda:self.__set_text('volvanos'))

        # Action menu options
        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="submit_guess", command=self.__submit_guess)
        self.actionmenu.add_command(label="backspace", command=self.__backspace)
        self.actionmenu.add_cascade(label="Select a word", menu=self.lettermenu)

        # Adding the submenus to the main menubar
        self.menubar.add_cascade(menu=self.filemenu, label='File')
        self.menubar.add_cascade(menu=self.actionmenu, label='Action')

        # Assigning menubar to the root window
        self.root.config(menu=self.menubar)

        # Display all
        self.root.mainloop()

    # Private method __on_closing
    # Displays a message box when the user closes the window
    # Can be used to ask user if they want to save before quitting.
    def __on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

    # Private method __set_text
    # Handles placing the letters from the buttons into the entry field
    # on screen.
    # Args:
    #   text - a string or char that gets appended to the end of the entry field
    def __set_text(self, text):
        self.entry.insert(len(self.entry.get()), text)
        return
    
    # Private method __submit_guess
    # Handles submitting what is in the entry field
    def __submit_guess(self):
        text = self.entry.get()
        if text.lower() == "volcanos":
            print("Correct!")
        else:
            print("Incorrect!")
        self.entry.delete(0, tk.END)

    # Private method __shortcut
    # shortcut functionality for pressing enter to submit guess
    def __shortcut(self, event):
        if event.keysym == "Return":
            self.__submit_guess()

    # Private method __backspace
    # allow backspace button to have functionality.
    def __backspace(self):
        self.entry.delete(len(self.entry.get()) - 1, tk.END)

    

BeeUI()