# BeeUI
# Team SNEK
# CSCI 420 - Software Engineering
# Millersville University
#
# BeeUI will create a BeeUI object upon a constructor call,
# and functionality of the game will begin when the .launch()
# function is called on that object.
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
#    Image, ImageTk from pillow (PIL)
#    GameController
#    UserInterface (superclass)
#

import sys
sys.path.append('../controller')


import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import *
import os
from UserInterface import UserInterface
from PIL import Image,ImageTk
import random
#from GameController import GameController
from colorama import Fore, Style

class BeeUI(UserInterface):

    __EXIT_MSG = "Do you want to exit the game? (You'll be able to save it)"
    __DONE_PROGRESS = "⬢"
    __LEFT_PROGRESS = "⬡"

    def __init__(self):
        super().__init__()
        # Define the window itself
        self.root = tk.Tk()
        # Determine what the window will look like and what it does on close.
        self.root.geometry("900x600")
        self.root.title("The Spelling Bee! 🐝")

# # # # # # # # # # # # # Menus # # # # # # # # # # # # # 
        # Create Menu bar
        self.menubar = tk.Menu(self.root)

        # File menu options
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.__preGamePage)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save", command=self.__onSave)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Load Game", command=self.__onLoad)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit Current Game", command=self.__checkQuit)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close Program", command=self.__onClosing)
        # For developer usage - assure removed for release
        # self.filemenu.add_command(label="DEV Close", command=exit)

        self.viewmenu = tk.Menu(self.menubar, tearoff=0)
        self.viewmenu.add_command(label="Show Rankings", command=lambda:self.myController.processInput("!rank"))
        self.viewmenu.add_command(label="Show Guessed Words", command=lambda:self.myController.processInput("!guessed"))
        self.viewmenu.add_command(label="Show Help", command=self.showHelp)

# # # # # # # # # # # # # Developer Menus # # # # # # # # # # # # #
# # # # # Assure that these are removed for release 
# # # # # Or perhaps edited to be used by user

        # Word Menu for inside of action
        self.lettermenu = tk.Menu(tearoff=0)
        self.lettermenu.add_command(label='set volcanos', command=lambda:self.__setText('volcanos'))
        self.lettermenu.add_command(label='set volvanos', command=lambda:self.__setText('volvanos'))

        # Action menu options
        self.actionmenu = tk.Menu(self.menubar, tearoff=0)
        self.actionmenu.add_command(label="submitGuess", command=self.__submitGuess)
        self.actionmenu.add_command(label="backspace", command=self.__backspace)
        self.actionmenu.add_cascade(label="Select a word", menu=self.lettermenu)

# # # # # # # # # # # # # END Developer Menus # # # # # # # # # # # # #

        # Adding the submenus to the main menubar
        self.menubar.add_cascade(menu=self.filemenu, label='File')
        self.menubar.add_cascade(menu=self.viewmenu, label='Views')
        # self.menubar.add_cascade(menu=self.actionmenu, label='Action')

        # Assigning menubar to the root window
        self.root.config(menu=self.menubar)
    
# # # # # # # # # # # # Display Main Menu # # # # # # # # # # # #

        # Define the mainFrame of the window
        self.mainFrame = tk.Frame(self.root)
        # MainFrame will be the frame for any and all widgets to be
        # added and displayed.
        
        # Display the mainMenuPage
        self.__mainMenuPage()
        

# # # # # # # # # # # # Class Methods # # # # # # # # # # # #

    # Private method __onSave
    # Notifies myController that the user intends to save
    def __onSave(self):
        self.myController.processInput("!save")

    # Private method __onLoad
    # Notifies myController that the user intends to load
    def __onLoad(self, help=""):
        # Trying to load from the main menu
        if(help == ""):
            self.myController.processInput("!load")
        # Trying to load from inside of another game
        elif(help =="help"):
            self.myController.processInput("!load")
            # showStatus() needed to update status of new game
            self.showStatus()

    # Public method getConfirmation
    # Returns a True or False confirmation between two options
    # given to the user.  This information is used by GameController
    # to know what to run and when.
    def getConfirmation(self, inputString, okStr="yes", nokStr="no"):
        # Checking how the user wants to save (Scratch / Current)
        if(inputString == "How do you want to save?"):
            self.textStringForCon = ""
            self.__messageWindow("Save", "How do you want to save?")
            if self.textStringForCon == "":
                return 3
            print(self.textStringForCon)
            if self.textStringForCon.lower() == okStr: # Scratch
                return True
            elif self.textStringForCon.lower() == nokStr: # Current
                return False
        
        # Asking user about overwritting already saved game name
        elif(inputString == "Do you want to overwrite it?"):
            return True
        
        # Asking user if they wish to exit the current game
        elif(inputString == self.__EXIT_MSG):
            if messagebox.askyesno("", self.__EXIT_MSG):
                return True
            else:
                return False
        
        # Asking the user if they wish to save the game upon exit
        elif(inputString == "Do you want to save the game?"):
            if messagebox.askyesno("Save", "Do you want to save the game?"):
                return True
            else:
                return False

        # Asking the user if they wish to save upon New game
        elif(inputString == "Do you want to save?"):
            if messagebox.askyesno("Save", "Do you want to save the game?"):
                self.__preGamePage()
                return True
            else:
                self.__preGamePage()
                return False
    
    # Private method __messageWindow
    # Accepts a title for the window, and a message for the window.
    def __messageWindow(self, title="title", message="Message! Close the window!"):
        self.win = Toplevel() # Popout screen
        self.win.title(title)
        tk.Label(self.win, text=message).pack()
        self.windowFrameBtns = tk.Frame(self.win)
        self.windowFrameBtns.columnconfigure(0, weight=1)
        self.windowFrameBtns.columnconfigure(1, weight=1)

        # Displays two buttons to the popout window, one for a Scratch save and one for 
        # a Current save.
        self.scratchBtn = tk.Button(self.windowFrameBtns, text='Scratch', command=lambda:[self.__textHelper("scratch")])
        self.currentBtn = tk.Button(self.windowFrameBtns, text='Current', command=lambda:[self.__textHelper("current")])

        self.scratchBtn.grid(row=0, column=0)
        self.currentBtn.grid(row=0, column=1)

        self.windowFrameBtns.pack()
        self.win.wait_window() # Program will wait for the selection of the user.

    # Private method textHelper
    # Accepts a string text that will be one of two option ("scratch"/"current")
    # and then assigns it to be used in getConfirmation
    def __textHelper(self, text):
        self.textStringForCon = text
        self.win.destroy() # Destroys the popout window
        
    # Public method getSaveFileName
    # Accepts a saveType that will be a string of ("save"/"load")
    # Proceeds to open a filedialog that will allow user to save or load
    # a game as needed.
    def getSaveFileName(self, saveType = ""):
        if(saveType == "save"):
            return filedialog.asksaveasfilename(filetypes=[("Json File","*.json")], defaultextension=[("Json File", "*.json")], initialdir=os.getcwd())
        elif(saveType == "load"):
            return filedialog.askopenfilename(title="Select the file", filetype=(("Json File", "json"), ("all files", "*")), initialdir=os.getcwd())    

    # Public method showMessage
    # Accepts a message msgString
    # Displays a messagebox with msgString
    def showMessage(self, msgString):
        if(msgString == "This file already exists"):
            return
        messagebox.showinfo("", msgString)

    # Public method showError
    # Params:
    #   errorString - description of the error
    #   errorTitle - title of the error messagebox
    # Displays a messagebox with the given error
    def showError(self, errorString="Error!", errorTitle="Error!"):
        messagebox.showinfo(errorTitle, errorString)

    # Public method getBaseWord
    # Pulls the typed word from the newWord entry box on the
    # pre-game page to be sent to controller.
    def getBaseWord(self):
        return self.newWord.get()

    # Public method launch
    # Launches the BeeUI.  Call on a BeeUI object.
    def launch(self):
        self.root.mainloop()

    # Public method quitInterface
    def quitInterface(self):
        pass

    # Public method showCorrectGuess
    # If the controller signals that the given guess was correct,
    # then the label at the top of the game page will be changed.
    def showCorrectGuess(self):
        self.correctLabel.configure(text=f"Your guess was correct!", font=('Arial', 25))

    # Public method showEnd
    # If the controller signals that the game is over, then a victory
    # title will be displayed at the top of the screen and usable buttons will
    # be grayed out.
    def showEnd(self):
        self.__winPage()
        
    # Public method showGuessedWords
    # Params:
    #   guessList - a list of words already guessed by the user.
    # Shows list of guessed words to the player
    def showGuessedWords(self, guessList):
        str = '\n'.join(guessList)
        self.showMessage(str)

    # Public method showHelp
    # Creates a small popup window to display the helpscreen image to
    # the user.
    def showHelp(self):
        self.win = Toplevel() # popout window
        self.win.title("Help!")

        self.helpscreenImg = Image.open('img/helpscreen.PNG')
        self.helpscreenImg = self.helpscreenImg.resize((750, 500))
        self.helpscreenImgSized = ImageTk.PhotoImage(self.helpscreenImg)

        self.helpscreenImg = tk.Button(self.win, image=self.helpscreenImgSized) # Unusable button
        self.helpscreenImg.pack()

    # Public method showProgress
    # Params:
    #   rank - current rank of the user
    #   thresholds - list of point thresholds for ranks
    #   currentPoints - current points the user has earned
    # Displays a progress bar at the top of the screen that is updated as
    # the game is played.
    def showProgress(self, rank: str, thresholds: list[int], currentPoints: int) -> None:
        str = ""
        str +=" 🍯  "
        if currentPoints == 0:
            str += self.__LEFT_PROGRESS + "───"
        else:
            str += self.__DONE_PROGRESS + "───"

        maxPoints = thresholds[-1]
        for rankPoints in thresholds[1:-1]:
            if currentPoints >= rankPoints:
                str += self.__DONE_PROGRESS + "───"
            else:
                str += self.__LEFT_PROGRESS + "───"

        if currentPoints >= maxPoints:
            str += self.__DONE_PROGRESS + "  🐝"
        else:
            str += self.__LEFT_PROGRESS + "  🐝"
        
        self.progBar.configure(text=str)
    
    # Public method showPuzzle
    # Params:
    #   puzzle - the puzzle key the user is playing with
    # Updates the gamePage to have all current and up-to-date info
    # about their currently played game.
    def showPuzzle(self, puzzle):
        self.wordPuzzle = puzzle.getPuzzleLetters()
        self.__gamePage()
        self.showProgress(puzzle.getCurrentRank(), list(puzzle.getRankingsAndPoints().values()), puzzle.getCurrentPoints())
        self.myController.processInput("!status")

    # Public method showRanking
    # Params:
    #   rankDict - Dictionary of rank to points required
    def showRanking(self, rankDict):
        stri = "The ranking points change based on the specific game you are playing:\n"
        stri += "Ranking for this game:\n"
        for label, points in rankDict.items():
            stri += "\t" + f"{label:10}" + ": " + str(points) + "\n"
        
        self.showMessage(stri)
        
    # Public method showStatus
    # Params:
    #   rank - current rank of the user
    #   points - current points the user has earned
    # Updates the gamePage to show current points and rank
    def showStatus(self, rank, points):
        self.rank.configure(text = rank)
        self.pointVal.configure(text = points)

    # Public method showWrongGuess
    # Params:
    #   str - the description of the wrong guess made.
    # Shows the user why their guess is incorrect
    def showWrongGuess(self, str):
        self.correctLabel.configure(text=str, font=('Arial', 25))

    # Private method __onClosing
    # Displays a message box when the user closes the window
    # Can be used to ask user if they want to save before quitting.
    def __onClosing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.myController.processInput("!exit")
            self.root.destroy()

    # Private method __setText
    # Handles placing the letters from the buttons into the entry field
    # on screen.
    # Args:
    #   text - a string or char that gets appended to the end of the entry field
    def __setText(self, text):
        self.entry.configure(state='normal')
        self.entry.insert(len(self.entry.get()), text)
        self.entry.configure(state='disabled')
        return
    
    # Private method __submitGuess
    # Handles submitting what is in the entry field
    # and passes it to the controller to be evaluted.
    # Clears the wordfield upon completion.
    def __submitGuess(self):
        text = self.entry.get()
        self.entry.configure(state='normal')
        self.entry.delete(0, tk.END)
        self.entry.configure(state='disabled')
        self.myController.processInput(text)

    # Private method __shortcut
    # Params:
    #   event - a <KeyPress> event
    def __shortcut(self, event):
        if event.keysym == "Return":
            self.__submitGuess()
        elif event.keysym == "BackSpace":
            self.__backspace()
        elif event.keysym == "space":
            self.__shuffleText()
        elif event.keysym == self.wordPuzzle[0]:
            self.__setText(self.wordPuzzle[0])
        elif event.keysym == self.wordPuzzle[1]:
            self.__setText(self.wordPuzzle[1])
        elif event.keysym == self.wordPuzzle[2]:
            self.__setText(self.wordPuzzle[2])
        elif event.keysym == self.wordPuzzle[3]:
            self.__setText(self.wordPuzzle[3])
        elif event.keysym == self.wordPuzzle[4]:
            self.__setText(self.wordPuzzle[4])
        elif event.keysym == self.wordPuzzle[5]:
            self.__setText(self.wordPuzzle[5])
        elif event.keysym == self.wordPuzzle[6]:
            self.__setText(self.wordPuzzle[6])

    # Private method __backspace
    # allow backspace button to have functionality.
    def __backspace(self):
        self.entry.configure(state='normal')
        self.entry.delete(len(self.entry.get()) - 1, tk.END)
        self.entry.configure(state='disabled')

    # Private method __clearFrame
    # Destroys all widgets in the mainFrame
    # For usage when swapping screens.
    def __clearFrame(self):
        for widgets in self.mainFrame.winfo_children():
            widgets.destroy()

    # Private method __checkQuit
    # Tells the controller we are ready to exit the game.
    def __checkQuit(self):
        self.myController.processInput("!exit")
        if not self.myController.playing:
            self.__mainMenuPage()

    # Private method __checkTerminate
    # Tells the controller we wish to quit and
    # terminates the program.
    def __checkTerminate(self):
        self.myController.processInput("!exit")
        if not self.myController.playing:
            self.root.destroy()

    # Private method __shuffleText
    # Shuffles the honeycomb on screen during gameplay.
    # Modifies the word puzzle.
    def __shuffleText(self):
        self.myController.processInput("!shuffle")

    # Private method __startGame
    # Notifies the controller that the user wants a new
    # random game.
    def __startGame(self):
        self.myController.processCommand("!new rnd")

    # # # # # # # # # # # # # Pages # # # # # # # # # # # # # 

    # Private method __mainMenuPage
    # Upon calling will clear the frame of anything currently
    # on screen (in the mainFrame).  After that it will
    # add all usefull information for the main menu
    # to the mainFrame to be seen on screen, and will then display.
    def __mainMenuPage(self):
        self.__clearFrame()

        # Assigns exit protocol for the window.
        self.root.protocol("WM_DELETE_WINDOW", self.__onClosing)
        
        self.filemenu.entryconfig("Save", state="disabled")
        self.filemenu.entryconfig("Quit Current Game", state="disabled")
        self.viewmenu.entryconfig("Show Rankings", state="disabled")
        self.viewmenu.entryconfig("Show Guessed Words", state="disabled")
        self.filemenu.entryconfig("Close Program", command=self.__onClosing)

        # Label at the top of the screen
        self.welcome = tk.Label(self.mainFrame, text="Welcome to the Spelling Bee Game! 🐝", font=('Arial', 30))
        self.welcome.pack()

        # Load images necessary for buttons
        self.newImg = PhotoImage(file='img/new.png')
        self.loadImg = PhotoImage(file='img/load.png')
        self.helpImg = PhotoImage(file='img/how.png')
        self.exitImg = PhotoImage(file='img/exit.png')

        # Create buttons for navigating menus
        self.newGameBtn = tk.Button(self.mainFrame, border='0', image=self.newImg, command=self.__preGamePage)
        self.loadGameBtn = tk.Button(self.mainFrame, border='0', image=self.loadImg, command=lambda:[self.__onLoad("help"), self.__gamePage()])
        self.helpBtn = tk.Button(self.mainFrame, border='0', image=self.helpImg, command=self.__howToPlayPage)
        self.exitGameBtn = tk.Button(self.mainFrame, border='0', image=self.exitImg, command=self.__onClosing)

        

        # Display buttons on main menu
        self.newGameBtn.pack(pady=7)
        self.loadGameBtn.pack(pady=7)
        self.helpBtn.pack(pady=7)
        self.exitGameBtn.pack(pady=7)

        # Display mainFrame
        self.mainFrame.pack(fill='x')

    # Private method __howToPlayPage
    # Upon calling will clear the frame of anything currenlty
    # on screen (in the mainFrame).  After that it will
    # add all usefull information for the how to play
    # instructions to the mainFrame to be seen on screen,
    # and will then display.
    def __howToPlayPage(self):
        self.__clearFrame()

        # Instructions #

        #Label at the top of the screen
        self.welcome = tk.Label(self.mainFrame, text="Welcome to the Spelling Bee Game! 🐝", font=('Arial', 30))
        self.welcome.pack()

        self.howToLabel = tk.Label(self.mainFrame, text="How To Play:\t\t\t ", font=('Arial bold', 24))
        self.howToLabel.pack()

        self.helpscreenImg = Image.open('img/helpscreen.PNG')
        self.helpscreenImg = self.helpscreenImg.resize((750, 425))
        self.helpscreenImgSized = ImageTk.PhotoImage(self.helpscreenImg)

        self.helpscreenImg = tk.Button(self.mainFrame, image=self.helpscreenImgSized)
        self.helpscreenImg.pack()

        # Designs #
        # Go Back Button #
        self.goBackImg = Image.open('img/goBack.png')
        self.goBackImg = self.goBackImg.resize((140, 51))
        self.goBackSized = ImageTk.PhotoImage(self.goBackImg)

        self.goBack = tk.Button(self.mainFrame, border='0', image=self.goBackSized, command=self.__mainMenuPage)
        self.goBack.pack()

    # Private method __preGamePage
    # Upon calling will clear the frame of anything currently
    # on screen (in the mainFrame).  After that it will
    # add all usefull information for the pre-game page,
    # adding buttons and an entry field for starting new games.
    def __preGamePage(self):
        self.__clearFrame()

        #Label at the top of the screen
        self.welcome = tk.Label(self.mainFrame, text="Welcome to the Spelling Bee Game! 🐝", font=('Arial', 30))
        self.welcome.pack()

        # New Game Random
        self.randBtnImg = PhotoImage(file='img/newRand.png')
        self.randBtn = tk.Button(self.mainFrame, border='0', image=self.randBtnImg, command=lambda: self.myController.processInput("!new rnd"))
        self.randBtn.pack(pady=25)

        # New Game Custom
        self.newWordGrid = tk.Frame(self.mainFrame)
        self.newWordGrid.columnconfigure(0, weight=1)
        self.newWordGrid.columnconfigure(0, weight=1)

        self.newWordLabel = tk.Label(self.newWordGrid, font=('Arial', 14), text='Type custom word here: ')
        self.newWordLabel.grid(row=0, column=0)
        self.newWord = tk.Entry(self.newWordGrid, font=('Arial', 18))
        self.newWord.grid(row=0, column=1, ipadx=20)

        self.customBtnImg = PhotoImage(file='img/newCustom.png')
        self.customBtn = tk.Button(self.newWordGrid, border='0', image=self.customBtnImg, command=lambda:self.myController.processInput("!new wrd"))
        self.customBtn.grid(row=1, columnspan=2)
        self.newWordGrid.pack(pady=25)

        self.goBackImg = PhotoImage(file='img/goBack.png')
        self.goBackBtn = tk.Button(self.mainFrame, border='0', image=self.goBackImg, command=self.__mainMenuPage)
        self.goBackBtn.pack(pady=25)

    # Private method __gamePage
    # Upon calling will clear the frame of anything currently
    # on screen (in the mainFrame).  After that it will
    # add all usefull information for the current game
    # to the mainFrame to be seen on screen, and will then display.
    def __gamePage(self):
        self.__clearFrame()

        self.root.protocol("WM_DELETE_WINDOW", self.__checkTerminate)

        # Allows usage of some filemenu options
        self.filemenu.entryconfig("New", command=lambda:[self.myController.processInput("!exit")])
        self.filemenu.entryconfig("Save", state="normal")
        self.filemenu.entryconfig("Quit Current Game", state="normal")
        self.filemenu.entryconfig("Close Program", command=self.__checkTerminate)

        self.viewmenu.entryconfig("Show Rankings", state="normal")
        self.viewmenu.entryconfig("Show Guessed Words", state="normal")

        self.correctLabel = tk.Label(self.mainFrame, text="", font=('Arial', 25))

        # Label at the top of the screen
        self.rankFrame = tk.Frame(self.mainFrame)
        self.rankFrame.columnconfigure(0, weight=1)
        self.rankFrame.columnconfigure(1, weight=1)

        # Point value header
        self.pointFrame = tk.Frame(self.mainFrame)
        self.pointFrame.columnconfigure(0, weight=1)
        self.pointFrame.columnconfigure(1, weight=1)

        # Defining header text labels
        self.rnklbl = tk.Label(self.rankFrame, text="Rank: ", font=('Arial', 18))
        self.rank = tk.Label(self.rankFrame, text="Beginner", font=('Arial', 18))
        self.progBar = tk.Label(self.mainFrame, font=('Arial', 18), text="🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯-🍯")
        self.pnts = tk.Label(self.pointFrame, text="Points: ", font=('Arial', 18))
        self.pointVal = tk.Label(self.pointFrame, text="0", font=('Arial', 18))
        
        # Placing labels into rank and point frames
        self.rnklbl.grid(row=0, column=0)
        self.rank.grid(row=0, column=1)
        self.pnts.grid(row=1, column=0)
        self.pointVal.grid(row=1, column=1)

        # Displaying game information to the screen
        self.correctLabel.pack()
        self.progBar.pack()
        self.rankFrame.pack()
        self.pointFrame.pack()


        # Frame for entry box and backspace button
        self.entryframe = tk.Frame(self.mainFrame)
        self.entryframe.columnconfigure(0, weight=1)
        self.entryframe.columnconfigure(1, weight=1)

        # Defining entry box and backspace button.
        self.entry = tk.Entry(self.entryframe, font=('Arial', 18), state="disabled", disabledbackground="white", disabledforeground="black")
        self.root.bind('<KeyPress>', self.__shortcut)
        self.entry.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.bck = PhotoImage(file='img/backspace.png')
        self.bckspce = tk.Button(self.entryframe, border='0', image=self.bck, command=self.__backspace)
        self.bckspce.grid(row=0, column=1, sticky=tk.W+tk.E)

        # Displaying entryframe on screen.
        self.entryframe.pack()

        self.submitButtonImg = Image.open('img/submit.png')
        self.submitButtonImg = self.submitButtonImg.resize((140, 51))
        self.submitButtonSized = ImageTk.PhotoImage(self.submitButtonImg)

        # Submit guess button creation and display
        self.sub = tk.Button(self.mainFrame, border='0', image=self.submitButtonSized, command=lambda:[self.__submitGuess(), self.myController.processInput("!status")])
        self.sub.pack()

        # Creation of frame for the honeycomb
        self.buttonframe = tk.Frame(self.mainFrame)

        # Opening base image for the honeycombs
        self.combImg = Image.open('img/comb.png')
        self.combImg = self.combImg.resize((100, 100))
        self.comb = ImageTk.PhotoImage(self.combImg)

        # Defining each of the 7 buttons.  btn4 is the required letter.
        self.btn1 = tk.Button(self.buttonframe, border='0', compound=tk.CENTER, text=self.wordPuzzle[1].upper(), font=('Arial', 18), image=self.comb, command=lambda:self.__setText(self.wordPuzzle[1]))
        self.btn1.place(y=8, x=150)
        #self.btn1Letter = tk.Button(self.buttonframe, activebackground= '#c7b12b', border='0', bg='#c7b12b', text=self.wordPuzzle[1].upper(), font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[1]))
        #self.btn1Letter.place(y=37, x=184)

        self.btn2 = tk.Button(self.buttonframe, border='0', compound=tk.CENTER, text=self.wordPuzzle[2].upper(), font=('Arial', 18), image=self.comb, command=lambda:self.__setText(self.wordPuzzle[2]))
        self.btn2.place(x=50, y=60)
        #self.btn2Letter = tk.Button(self.buttonframe, activebackground= '#c7b12b', border='0', bg='#c7b12b', text=self.wordPuzzle[2].upper(), font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[2]))
        #self.btn2Letter.place(x=86, y=90)

        self.btn3 = tk.Button(self.buttonframe, border='0', compound=tk.CENTER, text=self.wordPuzzle[3].upper(), font=('Arial', 18), image=self.comb, command=lambda:self.__setText(self.wordPuzzle[3]))
        self.btn3.place(x=250, y=60)
        #self.btn3Letter = tk.Button(self.buttonframe, activebackground= '#c7b12b', border='0', bg='#c7b12b', text=self.wordPuzzle[3].upper(), font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[3]))
        #self.btn3Letter.place(x=286, y=90)

        self.btn4 = tk.Button(self.buttonframe, border='0', compound=tk.CENTER, text=self.wordPuzzle[0].upper(), font=('Arial', 18), image=self.comb, command=lambda:self.__setText(self.wordPuzzle[0]))
        self.btn4.place(x=150, y=110)
        #self.btn4Letter = tk.Button(self.buttonframe, activebackground= '#c7b12b', border='0', bg='#c7b12b', text=self.wordPuzzle[0].upper(), font=('Arial bold', 18), command=lambda:self.__setText(self.wordPuzzle[0]))
        #self.btn4Letter.place(x=184, y=136)

        self.btn5 = tk.Button(self.buttonframe, border='0', compound=tk.CENTER, text=self.wordPuzzle[4].upper(), font=('Arial', 18), image=self.comb, command=lambda:self.__setText(self.wordPuzzle[4]))
        self.btn5.place(x=50, y=160)
        #self.btn5Letter = tk.Button(self.buttonframe, activebackground= '#c7b12b', border='0', bg='#c7b12b', text=self.wordPuzzle[4].upper(), font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[4]))
        #self.btn5Letter.place(x=86, y=190)

        self.btn6 = tk.Button(self.buttonframe, border='0', compound=tk.CENTER, text=self.wordPuzzle[5].upper(), font=('Arial', 18), image=self.comb, command=lambda:self.__setText(self.wordPuzzle[5]))
        self.btn6.place(x=250, y=160)
        #self.btn6Letter = tk.Button(self.buttonframe, activebackground= '#c7b12b', border='0', bg='#c7b12b', text=self.wordPuzzle[5].upper(), font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[5]))
        #self.btn6Letter.place(x=286, y=190)

        self.btn7 = tk.Button(self.buttonframe, border='0', compound=tk.CENTER, text=self.wordPuzzle[6].upper(), font=('Arial', 18), image=self.comb, command=lambda:self.__setText(self.wordPuzzle[6]))
        self.btn7.place(x=150, y=210)
        #self.btn7Letter = tk.Button(self.buttonframe, activebackground= '#c7b12b', border='0', bg='#c7b12b', text=self.wordPuzzle[6].upper(), font=('Arial', 18), command=lambda:self.__setText(self.wordPuzzle[6]))
        #self.btn7Letter.place(x=186, y=240)

        # Display the honeycomb frame to window
        self.buttonframe.pack(ipadx=200, ipady=155)

        self.shuffleButtonImg = Image.open('img/shuffle.png')
        self.shuffleButtonImg = self.shuffleButtonImg.resize((140, 51))
        self.shuffleButtonSized = ImageTk.PhotoImage(self.shuffleButtonImg)

        self.buttonShuffle = tk.Button(self.mainFrame, border='0', image=self.shuffleButtonSized, command=lambda:self.__shuffleText())
        self.buttonShuffle.pack()

        self.mainFrame.pack(fill='x')

    # Private method __winPage
    # Displays a win condition page and a go back arrow
    # that brings you to the main menu.
    def __winPage(self):
        self.__clearFrame()

        self.beestImg = Image.open('img/beest.PNG')
        self.beestImg = self.beestImg.resize((650, 400))
        self.beestImgSized = ImageTk.PhotoImage(self.beestImg)

        self.beestBtn = tk.Button(self.mainFrame, border='0', image=self.beestImgSized)
        self.beestBtn.pack()

        self.goBackImg = PhotoImage(file='img/goBack.png')
        self.goBackBtn = tk.Button(self.mainFrame, border='0', image=self.goBackImg, command=self.__mainMenuPage)
        self.goBackBtn.pack(pady=25)

# End class
# ASSURE YOU REMOVE THIS OR COMMENT IT OUT AFTER IMPLEMENTATION INTO MAIN:
# BeeUI()