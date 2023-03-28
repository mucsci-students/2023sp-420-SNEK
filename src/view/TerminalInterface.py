from view.UserInterface import UserInterface
from colorama import Fore, Style
from model.Puzzle import Puzzle
from model.Commands import *

import os



class TerminalInterface(UserInterface):

    # Initialization of styles for game title
    def __init__(self) -> None:
        super().__init__()
        self.__CMD_PREFIX = Style.BRIGHT + Fore.BLUE + ">>" + Style.RESET_ALL
        self.__DONE_PROGRESS = Fore.YELLOW + "⬢" + Style.RESET_ALL
        self.__LEFT_PROGRESS = "⬡" + Style.RESET_ALL
        self.__HELP_TITLE = "\n\tSpelling Bee Game!              🍯 🐝"
        self.__HELP_STRING = '''

How to play:
   You are given a word puzzle with a bunch of letters
   and a required letter.  The Required letter is in the
   center of the honeycomb.  Every word that you guess
   requires that the center letter be used, otherwise you
   will not receive credit for the guess.  The word that
   you guess also needs to be a valid word in the
   Scrabble dictionary.  Every puzzle has a corresponding
   pangram that it is generated from.  The pangram will
   include every letter in the honeycomb.

Commands:
   Call commands with a preceding '!'. Commands may be
   called at anytime.

   -!new random - Generate a new random puzzle
   -!new word - Generate a new puzzle with a user given
               word.  Console will prompt for the word after
               command is given.
   -!status - Display you status for the current puzzle.
   -!save - Bring up the prompts for saving your current game.
   -!load - Bring up the prompts for loading a saved game.
   -!shuffle - Shuffle the shown puzzle honeycomb randomly, changing
               the order of the letter randomly other than the 
               required center letter.  You can use this to
               help you find other words.
   -!guessed - Shows all the already correctly guessed words.
   -!help - Prints out the help menu.
   -!exit - Exits the game. Will prompt to save.'''

    # Launch terminal interface and gets user input and processes
    # input while the game is not quit
    def launch(self):
        while not self.quit:
            userInput = self.__getUserInput()
            if Commands.isCommand(userInput):
                userInput = Commands.getCommandFromName(userInput)

            self.myController.processInput(userInput)

    # Flag if the game is quit
    def quitInterface(self):
        self.quit = True

    # Gets user input from cli and checks if there is a command that
    # a user wants to use
    def __getUserInput(self, message: str = "") -> str:
        userInput = input(self.__CMD_PREFIX + message + " ").strip()
        return userInput
    
    # Path in directory that the user wants to save their games
    def __getUserInputPath(self, message: str = "") -> str:
        userInput = input(self.__CMD_PREFIX + message + " ").strip()
        return userInput

    # Reset colorama text so that it does not 
    # change other text to a bold print
    def __boldPrint(self, message: str, endStr: str = "\n") -> None:
        print(Style.BRIGHT + message + Style.RESET_ALL, end=endStr)

    # Print name of error on cli
    def __titleDescriptionPrint(self, title: str, description: str) -> None:
        print(title)
        if description != "":
            print("\t" + description)

    # Print the words base word so that the user can 
    # enter what base word they want to use for the puzzle
    def getBaseWord(self) -> str:
        self.__boldPrint("Base word: ")
        baseWord = self.__getUserInput()
        return baseWord

    # If user wants to see their points and rank status
    # when they enter the !status command, then it will print
    # users status on the screen and display rank and current points
    def showStatus(self, rank: str, currentPoints: int) -> None:
        self.__boldPrint(rank + ": " + str(currentPoints))

    # Progress bar that shows users current rank and and displays it
    # in a nice progress bar that shows how many ranks in you are and 
    # how many ranks are left to get to top rank
    def showProgress(self, rank: str, thresholds: list[int], currentPoints: int) -> None:
        print(Style.BRIGHT + f"\n  {rank:12s} ", end=Style.RESET_ALL)
        print(" 🍯  ", end="")
        if currentPoints == 0:
            print(self.__LEFT_PROGRESS + "╶──", end="")
        else:
            print(self.__DONE_PROGRESS + "╶──", end="")

        maxPoints = thresholds[-1]
        for rankPoints in thresholds[1:-1]:
            if currentPoints >= rankPoints:
                print(self.__DONE_PROGRESS + "╶──", end="")
            else:
                print(self.__LEFT_PROGRESS + "╶──", end="")

        if currentPoints >= maxPoints:
            print(self.__DONE_PROGRESS + "  🐝")
        else:
            print(self.__LEFT_PROGRESS + "  🐝")

    # Prints the puzzle into a honeycomb to display in the cli
    # required letter is in the center and always stays there when a user 
    # uses the shuffle command
    def showPuzzle(self, myPuzzle: Puzzle) -> None:
        self.showProgress(myPuzzle.getCurrentRank(), list(myPuzzle.getRankingsAndPoints().values()),myPuzzle.getCurrentPoints())
        myLetters = ''.join(myPuzzle.getPuzzleLetters()).upper()
        YB = Fore.YELLOW + Style.BRIGHT
        N = Fore.WHITE + Style.NORMAL
        Y = Fore.YELLOW
        print(YB + '''
                         ___
                     ___╱ {} ╲___
                    ╱ {} ╲___╱ {} ╲
                    ╲___╱ {} ╲___╱
                    ╱ {} ╲___╱ {} ╲ 
                    ╲___╱ {} ╲___╱
                        ╲___╱ '''.format(N + myLetters[1] + YB,
                                         N + myLetters[2] + YB,
                                         N + myLetters[3] + YB,
                                         Y + myLetters[0] + YB,
                                         N + myLetters[4] + YB,
                                         N + myLetters[5] + YB,
                                         N + myLetters[6] + YB)
              + Style.RESET_ALL)

    # Prints errors in the cli when a a user does not use the right command
    def showError(self, errorMessage, errorDescription="") -> None:
        self.__titleDescriptionPrint(
            Style.BRIGHT + Fore.RED + errorMessage + Style.RESET_ALL, errorDescription)

    # If the user types !help command, then it will print the help
    # instructions on how to play the game
    def showHelp(self) -> None:
        self.__boldPrint(self.__HELP_TITLE)
        print(self.__HELP_STRING)

    # Print rankings based on what puzzle is open and it shows how 
    # many points the user needs to achieve the next rank status
    def showRanking(self, rankingsAndPoints: dict[str, int]) -> None:
        print("The ranking points change based on the specific game you are playing:")
        self.__boldPrint("Ranking for this game:")
        for label, points in rankingsAndPoints.items():
            print("\t" + f"{label:10}" + ": " + str(points))

    # If the user completes the game, then it will print an end
    # screen that the user has found all the words
    def showEnd(self) -> None:
        print("                🐝")
        self.__boldPrint("Congratulations!", endStr=" ")
        print("You found all the words!")
        print("\tYou are the " + Fore.LIGHTYELLOW_EX +
              "bee" + Fore.RESET + "st\t\t    🍯")

    # Prints Exiting when a user wants to exit a puzzle
    def showExit(self) -> None:
        self.__boldPrint("Game exited.")
        self.__boldPrint("You are at the main program (not playing).")
        print()

    # If a user does not make a right guess, then it will 
    # print that they did not make a right guess
    def showWrongGuess(self, message="") -> None:
        self.__boldPrint("Wrong guess", endStr = "")
        if message == "":
            print("...")
        else:
            print(": \n\t" + message)

    # When a user makes the right guess, then it will
    # tell the user that they made the right guess
    def showCorrectGuess(self) -> None:
        self.__boldPrint("Good guess!")
        
        
    def __getPath(self) -> str:
        self.__boldPrint("Desired save path: ")
        name = self.__getUserInputPath()
        while name == "" or name == ".json":
            self.showError("The file has to have a name.", "Please try again:")
            name = self.__getUserInputPath()
            
        name = name if name.endswith(".json") else name + ".json "
            
        if not os.path.isabs(name):
            baseDir = os.getcwd()
            name = os.path.join(baseDir, name)
            
        fileName = os.path.normpath(name)
        
        return fileName

    # When a user wants to open their saved game, then it will 
    # ask what save file they want to open
    def getSaveFileName(self) -> str:
        fileName =  self.__getPath()
        
        if os.path.exists(fileName):
            self.showMessage("This file already exists")
            overwrite = self.getConfirmation("Do you want to overwrite it?")
            if not overwrite:
                name = os.path.join(os.getcwd(), ".json")
                fileName = os.path.normpath(name)

        return fileName

    # When a user wants to open their saved game, then it will 
    # ask what save file they want to open
    def getLoadFileName(self) -> str:
        return self.__getPath()

    # When !guessed is types, then it will print a list of all 
    # the words that the user has found in the game
    def showGuessedWords(self, guessedWords: list) -> None:
        self.__boldPrint("Guessed Words:")
        for word in guessedWords:
            print("\t" + word)

    # Confirmation for save and load for games and if it is not
    # yes or no, then it will tell the user that their input
    # is not recognized and will wait for the right input
    def getConfirmation(self, message, okStr="Y", nokStr="N"):
        okStr = okStr.lower()
        nokStr = nokStr.lower()
        self.__boldPrint(message + f" [{okStr}/{nokStr}]: ")
        choice = str(self.__getUserInput())
        while choice != okStr and choice != nokStr:
            print(f"(Unrecognized choice) [{okStr}/{nokStr}]: ")
            choice = self.__getUserInput()

        confirmation = choice == okStr
        return confirmation

    # Prints messages in cli
    def showMessage(self, message, endStr="\n"):
        print(message, end=endStr)



    def showHints(self, myPuzzle:Puzzle):
        myHints:Hint = myPuzzle.getHints()
        puzzleLetters = myPuzzle.getPuzzleLetters()
        
        self.__boldPrint("             🐝\nBᴇᴇ Gʀɪᴅ Hɪɴᴛs")
        print("\t● Puzzle Letters (Required first):  ", end="")
        self.__boldPrint(Fore.YELLOW + puzzleLetters[0].upper() + Style.RESET_ALL, endStr=" ")
        for letter in puzzleLetters[1:]:
            print(letter.upper(), end=" ")
        print()
            
        print(f"\t● Words: {myHints.numberOfWords}")
        print(f"\t● Points: {myPuzzle.getMaxPoints()}")
        print(f"\t● Pangrams: {myHints.pangrams} ", end="")
        if myHints.perfectPangrams > 0:
            print(f"({myHints.perfectPangrams} perfect)")
        else:
            print()
        
        if myHints.bingo:
            print("\t● Bingo")
            
        # Print matrix
        print("\n\t● Hint matrix:")
        print("\n", end="\t         ")
        headers = list(myHints.letterMatrix.items())[0][1].items()
        for header, _ in headers:
            self.__boldPrint(f"{header:^4}", endStr=" ")
            
        separator = "‒"
        for rowLetter, rowContent in myHints.letterMatrix.items():
            print("\n", end="\t    ")
            self.__boldPrint(f"{rowLetter:^4}", endStr=" ")
            for _, column in rowContent.items():
                if column == 0:
                    print(f"{separator:^4}", end=" ")
                else:
                    print(f"{column:^4}", end=" ")
        
        print("\n\n\n\t● Two letter list:")
        # Print 2 letter lists
        previousLetter = None
        for firstLetters, num in myHints.beginningList.items():
            if previousLetter != firstLetters[0]:
                previousLetter = firstLetters[0]
                print("\n", end="\t   ")
            print(f"  {firstLetters.upper()} → {num:<4}", end="")
        print()