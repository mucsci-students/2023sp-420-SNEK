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
# To launch the GUI, create a BeeUI object and call the 'launch' function.
# Once the launch function is called, the window will launch and you will
# be able to play the game.
# EX:
#   window = BeeUI()
#   window.launch()
#
# Imports:
#    random
#    tkinter as tk
#    messagebox from tkinter
#    PhotoImage from tkinter
#

import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import random

class BeeUI:
    def __init__(self):
        # Define the window itself
        self.root = tk.Tk()
        # Determine what the window will look like and what it does on close.
        self.root.protocol("WM_DELETE_WINDOW", self.__onClosing)
        self.root.geometry("900x600")
        self.root.title("The Spelling Bee! 🐝")

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
        self.filemenu.add_command(label="Quit Current Game", command=self.__checkQuit)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close Program", command=self.__onClosing)
        self.filemenu.add_command(label="DEV Close", command=exit)

        # Word Menu for inside of action
        self.lettermenu = tk.Menu(tearoff=0)
        self.lettermenu.add_command(label='set volcanos', command=lambda:self.__setText('volcanos'))
        self.lettermenu.add_command(label='set volvanos', command=lambda:self.__setText('volvanos'))

        # Action menu options
        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="submitGuess", command=self.__submitGuess)
        self.actionmenu.add_command(label="backspace", command=self.__backspace)
        self.actionmenu.add_cascade(label="Select a word", menu=self.lettermenu)

        # Adding the submenus to the main menubar
        self.menubar.add_cascade(menu=self.filemenu, label='File')
        self.menubar.add_cascade(menu=self.actionmenu, label='Action')

        # Assigning menubar to the root window
        self.root.config(menu=self.menubar)
    
# # # # # # # # # # # # Display Main Menu # # # # # # # # # # # #

        # Define the mainFrame of the window 
        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.columnconfigure(0, weight=1)
        
        self.__mainMenuPage()

        # Display all
        self.root.mainloop()

# # # # # # # # # # # # Class Methods # # # # # # # # # # # #

    # Public method launch
    # Launches the GUI.  FOR USAGE IN MAIN.PY
    def launch(self):
        BeeUI()

    # Private method __onClosing
    # Displays a message box when the user closes the window
    # Can be used to ask user if they want to save before quitting.
    def __onClosing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

    # Private method __setText
    # Handles placing the letters from the buttons into the entry field
    # on screen.
    # Args:
    #   text - a string or char that gets appended to the end of the entry field
    def __setText(self, text):
        self.entry.insert(len(self.entry.get()), text)
        return
    
    # Private method __submitGuess
    # Handles submitting what is in the entry field
    def __submitGuess(self):
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
            self.__submitGuess()

    # Private method __backspace
    # allow backspace button to have functionality.
    def __backspace(self):
        self.entry.delete(len(self.entry.get()) - 1, tk.END)

    # Private method __clearFrame
    # Destroys all widgets in the mainFrame
    # For usage when swapping screens.
    def __clearFrame(self):
        for widgets in self.mainFrame.winfo_children():
            widgets.destroy()

    # Private method __checkQuit
    # Pops a message box up to ask the user if they really want to return to the menu.
    # In future will work for asking if the user wants to save before leaving a game.
    def __checkQuit(self):
        if messagebox.askyesno(title="Quit Current Game?", message="Do you really want to return to the menu?"):
            self.__mainMenuPage()

    # Private method __shuffleText
    # Shuffles the honeycomb on screen during gameplay.
    # Modifies the word puzzle.
    def __shuffleText(self):
        restOfLetters = list(self.wordPuzzle[1:])
        random.shuffle(restOfLetters)
        self.wordPuzzle = self.wordPuzzle[0] + ''.join(restOfLetters)
        self.btn1.configure(text=self.wordPuzzle[3], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[3]))
        self.btn2.configure(text=self.wordPuzzle[1], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[1]))
        self.btn3.configure(text=self.wordPuzzle[2], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[2]))
        self.btn4.configure(text=self.wordPuzzle[0], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[0]))
        self.btn5.configure(text=self.wordPuzzle[4], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[4]))
        self.btn6.configure(text=self.wordPuzzle[5], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[5]))
        self.btn7.configure(text=self.wordPuzzle[6], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[6]))


    # # # # # # # # # # # # # Pages # # # # # # # # # # # # # 

    # Private method __mainMenuPage
    # Upon calling will clear the frame of anything currently
    # on screen (in the mainFrame).  After that it will
    # add all usefull information for the main menu
    # to the mainFrame to be seen on screen, and will then display.
    def __mainMenuPage(self):
        self.__clearFrame()
        
        self.filemenu.entryconfig("Save Current Game", state="disabled")
        self.filemenu.entryconfig("Save Scratch Game", state="disabled")
        self.filemenu.entryconfig("Quit Current Game", state="disabled")
        # Label at the top of the screen
        self.welcome = tk.Label(self.mainFrame, text="Welcome to the Spelling Bee Game! 🐝", font=('Arial', 30))
        self.welcome.grid(row=0, column=0)

        self.newGameBtn = tk.Button(self.mainFrame, text="New Game", font=('Arial', 25), command=self.__gamePage)
        self.loadGameBtn = tk.Button(self.mainFrame, text="Load Game", font=('Arial', 25), command=self.__gamePage)
        self.exitGameBtn = tk.Button(self.mainFrame, text="Exit Game", font=('Arial', 25), command=self.__onClosing)

        self.newGameBtn.grid(row=1, pady=25)
        self.loadGameBtn.grid(row=2, pady=25)
        self.exitGameBtn.grid(row=3, pady=25)

        self.mainFrame.pack(fill='x')

    # Private method __gamePage
    # Upon calling will clear the frame of anything currently
    # on screen (in the mainFrame).  After that it will
    # add all usefull information for the current game
    # to the mainFrame to be seen on screen, and will then display.
    def __gamePage(self):
        self.__clearFrame()

        self.filemenu.entryconfig("Save Current Game", state="normal")
        self.filemenu.entryconfig("Save Scratch Game", state="normal")
        self.filemenu.entryconfig("Quit Current Game", state="normal")

        # Variables that will be required:
        # Placeholder self.wordPuzzle
        self.wordPuzzle = "volcans"

        # Label at the top of the screen
        self.rankFrame = tk.Frame(self.mainFrame)
        self.rankFrame.columnconfigure(0, weight=1)
        self.rankFrame.columnconfigure(1, weight=1)

        self.pointFrame = tk.Frame(self.mainFrame)
        self.pointFrame.columnconfigure(0, weight=1)
        self.pointFrame.columnconfigure(1, weight=1)

        self.rnklbl = tk.Label(self.rankFrame, text="You're a: ", font=('Arial', 18))
        self.rank = tk.Label(self.rankFrame, text="Beginner", font=('Arial', 18))
        self.progBar = tk.Label(self.mainFrame, font=('Arial', 18), text="🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯")
        self.pnts = tk.Label(self.pointFrame, text="Points: ", font=('Arial', 18))
        self.pointVal = tk.Label(self.pointFrame, text="0", font=('Arial', 18))
        
        self.rnklbl.grid(row=0, column=0)
        self.rank.grid(row=0, column=1)
        self.progBar.grid(row=1, column=0)
        self.pnts.grid(row=1, column=0)
        self.pointVal.grid(row=1, column=1)

        self.rankFrame.grid(row=0, column=0, pady=5)
        self.pointFrame.grid(row=2, column=0, pady=5)


        # Frame for entry box and backspace button
        self.entryframe = tk.Frame(self.mainFrame)
        self.entryframe.columnconfigure(0, weight=1)
        self.entryframe.columnconfigure(1, weight=1)

        # Defining entry box and backspace button.
        self.entry = tk.Entry(self.entryframe, font=('Arial', 12))
        self.entry.bind('<KeyPress>', self.__shortcut)
        self.entry.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.entry.focus()
        self.bck = PhotoImage(file='backspace.png')
        self.bckspce = tk.Button(self.entryframe, image=self.bck, command=self.__backspace)
        self.bckspce.grid(row=0, column=1, sticky=tk.W+tk.E)

        # Displaying entryframe on screen.
        self.entryframe.grid(row=3, column=0, pady=5)

        # Submit guess button creation and display
        self.sub = tk.Button(self.mainFrame, text="Submit Guess", font=('Arial', 18), command=lambda:self.__submitGuess())
        self.sub.grid(row=4, column=0, pady=5)

        # Creation of frame for the honeycomb
        self.buttonframe = tk.Frame(self.mainFrame)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)

        # Defining each of the 7 buttons.  btn4 is the required letter.
        self.btn1 = tk.Button(self.buttonframe, text=self.wordPuzzle[1], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[1]))
        self.btn1.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E)

        self.btn2 = tk.Button(self.buttonframe, text=self.wordPuzzle[2], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[2]))
        self.btn2.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.btn3 = tk.Button(self.buttonframe, text=self.wordPuzzle[3], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[3]))
        self.btn3.grid(row=1, column=1, sticky=tk.W+tk.E)

        self.btn4 = tk.Button(self.buttonframe, text=self.wordPuzzle[0], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[0]))
        self.btn4.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E)

        self.btn5 = tk.Button(self.buttonframe, text=self.wordPuzzle[4], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[4]))
        self.btn5.grid(row=3, column=0, sticky=tk.W+tk.E)

        self.btn6 = tk.Button(self.buttonframe, text=self.wordPuzzle[5], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[5]))
        self.btn6.grid(row=3, column=1, sticky=tk.W+tk.E)

        self.btn7 = tk.Button(self.buttonframe, text=self.wordPuzzle[6], font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[6]))
        self.btn7.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E)

        # Display the honeycomb frame to window
        self.buttonframe.grid(row=5, column=0, ipadx=150, pady=5)

        self.buttonShuffle = tk.Button(self.mainFrame, text="Shuffle", font=('Arial', 18), bg=('#FAF884'), command=lambda:self.__shuffleText())
        self.buttonShuffle.grid(row=6, pady=5)

        self.mainFrame.pack(fill='x')

# End class
# ASSURE YOU REMOVE THIS OR COMMENT IT OUT AFTER IMPLEMENTATION INTO MAIN:
#BeeUI()