from view.UserInterface import UserInterface
from colorama import Fore, Style
from view.Inputer import Inputer
from model.Puzzle import Puzzle
from model.Commands import *
from model.Hint import Hint
from contextlib import redirect_stdout


import os
import sys


class TerminalInterface(UserInterface):

    # Initialization of styles for game title
    def __init__(self) -> None:
        super().__init__()
        self.defaultYes = 'y'
        self.defaultNo = 'n'
        self.defaultCancel = 'c'
        self.myInputer: Inputer = Inputer()
        self.__CMD_PREFIX: str = Style.BRIGHT + Fore.BLUE + ">>" + Style.RESET_ALL
        self.__DONE_PROGRESS: str = Fore.YELLOW + "⬢" + Style.RESET_ALL
        self.__LEFT_PROGRESS: str = "⬡" + Style.RESET_ALL
        self.__HELP_TITLE: str = "\n\tSpelling Bee Game!              🍯 🐝"
        self.__HELP_STRING: str = '''

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
   -!scores - Displays both the high scores for the puzzle and 
              the current score for the player.
   -!save - Bring up the prompts for saving your current game.
   -!save secret - Bring up the prompts for saving your current 
                   game with encryption.
   -!save score - Bring up prompts for saving your score into
                  High Scores if applicable.
   -!save image - Saves image of the CLI honeycomb.
   -!load - Bring up the prompts for loading a saved game.
   -!scores - Display the scoreboard for the current game and current points.
   -!rank - Display available ranks and point thresholds per rank.
   -!shuffle - Shuffle the shown puzzle honeycomb randomly, changing
               the order of the letter randomly other than the
               required center letter.  You can use this to
               help you find other words.
   -!guessed - Shows all the already correctly guessed words.
   -!hints - prints out all the hints for the given puzzle
   -!help - Prints out the help menu.
   -!exit - Exits the game. Will prompt to save.
   -!quit - Exits the entire program. Will prompt to save.'''

    # Launch terminal interface and gets user input and processes
    # input while the game is not quit

    def launch(self):
        try:
            commandStrings = Commands.getCommandNameList()
            while not self.quit:
                userInput = self.__getUserInput(options=commandStrings)
                if Commands.isCommand(userInput):
                    userInput = Commands.getCommandFromName(userInput)

                self.myController.processInput(userInput)
        except:
            sys.stdout.flush()
            print()
            exit()

    # Flag if the game is quit
    def quitInterface(self):
        self.quit = True

    # Gets user input from cli and checks if there is a command that
    # a user wants to use
    def __getUserInput(self, message: str = "", options=[]) -> str:
        userInput = self.myInputer.input(
            self.__CMD_PREFIX + message + " ", options).strip().lower()
        return userInput

    # Path in directory that the user wants to save their games
    def __getUserInputPath(self, message: str = "") -> str:
        userInput = self.myInputer.inputPath(
            self.__CMD_PREFIX + message + " ").strip()
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
        baseWord = input().lower().strip()
        return baseWord


    # Progress bar that shows users current rank and and displays it
    # in a nice progress bar that shows how many ranks in you are and
    # how many ranks are left to get to top rank
    def showProgress(self, rank: str, thresholds: list[int], currentPoints: int) -> None:
        rankAndPoints = f"{rank} ({currentPoints})"
        print(Style.BRIGHT + f"\n  {rankAndPoints:16s} ", end=Style.RESET_ALL)
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
        # os.system('cls' or 'clear')
        self.showProgress(myPuzzle.getCurrentRank(), list(
            myPuzzle.getRankingsAndPoints().values()), myPuzzle.getCurrentPoints())
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
        self.__boldPrint("Wrong guess", endStr="")
        if message == "":
            print("...")
        else:
            print(": \n\t" + message)

    # When a user makes the right guess, then it will
    # tell the user that they made the right guess
    def showCorrectGuess(self) -> None:
        self.__boldPrint("Good guess!")

    def __getPath(self) -> str:
        baseDir = os.getcwd()
        self.__boldPrint("Desired save path:")
        print(f"\tDefault directory: {baseDir}")
        name = self.__getUserInputPath()
        while name == "" or name == ".json":
            self.showError("The file has to have a name.", "Please try again:")
            name = self.__getUserInputPath()

        name = name if name.endswith(".json") else name + ".json"

        if not os.path.isabs(name):
            name = os.path.join(baseDir, name)

        fileName = os.path.normpath(name)

        return fileName

    # When a user wants to open their saved game, then it will
    # ask what save file they want to open
    def getSaveFileName(self) -> str:
        fileName = self.__getPath()

        if os.path.exists(fileName):
            self.showMessage("This file already exists")
            overwrite = self.getConfirmation("Do you want to overwrite it?")

            if overwrite == self.defaultYes:
                pass
            elif overwrite == self.defaultNo:
                fileName = ""
            else:
                fileName = None

        return fileName
 
    def saveScreenshot(self, myPuzzle: Puzzle):
            myLetters = ''.join(myPuzzle.getPuzzleLetters()).upper()
            rank = myPuzzle.getCurrentRank()
            score = myPuzzle.getCurrentPoints()
            prog = "Rank: " + rank + "   " + "Score: " + str(score)
            fileName = self.getSaveFileName()
            fileName = os.path.splitext(fileName)[0]
            fileName = fileName + ".png"

            
            return     ['''  {}
<---------------------------->
|             ___            |
|         ___/ {} \___        |
|        / {} \___/ {} \\       |
|        \___/ {} \___/       |
|        / {} \___/ {} \\       |
|        \___/ {} \___/       |
|            \___/           |
<---------------------------->'''.format(prog,
                            myLetters[1],
                            myLetters[2],
                            myLetters[3],
                            myLetters[0],
                            myLetters[4],
                            myLetters[5],
                            myLetters[6]), fileName]
        

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

    def __getQuickInput(self, okStr, nokStr, canStr):
        return self.myInputer.quickInput(self.__CMD_PREFIX + " ", [okStr, nokStr, canStr])

    # Confirmation for save and load for games and if it is not
    # yes or no, then it will tell the user that their input
    # is not recognized and will wait for the right input
    def getConfirmation(self, message, okStr="", nokStr="", canStr=""):
        self.choice = ""

        if okStr == "":
            okStr = self.defaultYes

        if nokStr == "":
            nokStr = self.defaultNo

        if canStr == "":
            canStr = self.defaultCancel

        okStr = okStr.lower()
        nokStr = nokStr.lower()
        canStr = canStr.lower()

        self.__boldPrint(message + f" [{okStr}/{nokStr}/{canStr}]: ")
        if len(okStr) == 1 and len(nokStr) == 1 and len(canStr) == 1:
            choice = self.__getQuickInput(okStr, nokStr, canStr)
        else:
            choice = str(self.__getUserInput(
                options=[okStr, nokStr, canStr])).lower().strip()

        while choice != okStr and choice != nokStr and choice != canStr:
            print(f"Unrecognized choice [{okStr}/{nokStr}/{canStr}]: ")
            choice = self.__getUserInput(
                options=[okStr, nokStr, canStr]).lower().strip()

        return choice

    # Prints messages in cli
    def showMessage(self, message, endStr="\n"):
        print(message, end=endStr)

    def showHints(self, myPuzzle: Puzzle):
        myHints: Hint = myPuzzle.getHint()
        puzzleLetters = myPuzzle.getPuzzleLetters()

        self.__boldPrint("             🐝\nBᴇᴇ Gʀɪᴅ Hɪɴᴛs")
        print("\t● Puzzle Letters (Required first):  ", end="")
        self.__boldPrint(
            Fore.YELLOW + puzzleLetters[0].upper() + Style.RESET_ALL, endStr=" ")
        for letter in puzzleLetters[1:]:
            print(letter.upper(), end=" ")
        print()

        print(f"\t● Words: {myHints.numberOfWords}")
        print(f"\t● Points: {myPuzzle.getMaxPoints()}")
        print(f"\t● Pangrams: {myHints.pangram} ", end="")
        if myHints.perfectPangram > 0:
            print(f"({myHints.perfectPangram} perfect)")
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

    def showHighScores(self, myPuzzle: Puzzle):
        B = Style.BRIGHT
        Y = Fore.YELLOW
        R = Style.RESET_ALL
        G = Fore.GREEN
        W = Fore.WHITE
        D = Style.DIM
        highScoreText = [f"{D+B+G}",
 "#     #                          #####                                         " ,
 "#     #  #   ####   #    #      #     #   ####    ####   #####   ######   #### " ,
 "#     #  #  #    #  #    #      #        #    #  #    #  #    #  #       #     " ,
 "#######  #  #       ######       #####   #       #    #  #    #  #####    #### " ,
 "#     #  #  #  ###  #    #            #  #       #    #  #####   #            #" ,
 "#     #  #  #    #  #    #      #     #  #    #  #    #  #   #   #       #    #" ,
 "#     #  #   ####   #    #       #####    ####    ####   #    #  ######   #### " ,
 f"{R}"]
        middle: int = (os.get_terminal_size().columns / 2)
        myHighScores:list[list[str,int]] = myPuzzle.getHighScores()

        if len(myHighScores) > 0:
            k = len(highScoreText[1])/2
            leadingBlank = ''.join([" "] * (int)(middle - k))
            for text in highScoreText:
                print(leadingBlank+text)

            k:int = 20
            n:int = 20
            l: int = (int)(middle - (((k + n)/2) + 7))  # 7 is the breathing room and frames
            i: int = 2

            leadingBlank = ''.join([" "] * l)

            first = myHighScores[0]
            print(f"{leadingBlank}{B+Y}╔══════╤═{''.join(['═']*k)}═╤═{''.join(['═']*n)}═╗{R}")
            print(f"{leadingBlank}{B+Y}║ {R+Y}{'RANK':^4}{B+Y} │ {R+Y}{'NAME':^20}{B+Y} │ {R+Y}{'POINTS':^20}{B+Y} ║{R}")
            print(f"{leadingBlank}{B+Y}╠══════╪═{''.join(['═']*k)}═╪═{''.join(['═']*n)}═╣{R}")
            print(f"{leadingBlank}{B+Y}║ {G}{'1':^4}{B+Y} │ {G}{first[0].upper():^20}{B+Y} │ {G}{first[1]:^20}{B+Y} ║{R}")

            if len(myHighScores) > 1:
                print(f"{leadingBlank}{B+Y}╟──────┼─{''.join(['─']*k)}─┼─{''.join(['─']*n)}─╢{R}")
                for name, score in myHighScores[1:-1]:
                    print(f"{leadingBlank}{B+Y}║ {W}{i:^4}{B+Y} │ {W}{name.upper():^20}{B+Y} │ {W}{score:^20}{B+Y} {B+Y}║{R}")
                    print(f"{leadingBlank}{B+Y}╟──────┼─{''.join(['─']*k)}─┼─{''.join(['─']*n)}─╢{R}")
                    i += 1

                last = myHighScores[-1]
                print(f"{leadingBlank}{B+Y}║ {R+W+D}{len(myHighScores):^4}{B+Y} │ {R+W+D}{last[0].upper():^20}{B+Y} │ {R+W+D}{last[1]:^20}{B+Y} ║{R}")

            print(f"{leadingBlank}{B+Y}╚══════╧═{''.join(['═']*k)}═╧═{''.join(['═']*n)}═╝{R}")

            currentPoints = myPuzzle.getCurrentPoints()
            difference = myPuzzle.getMinimumHighScore() - currentPoints
            self.__boldPrint(f"You have {currentPoints} points:")
            if difference > 0:
                print(f"\tYou are {difference} points away form entering the leader board.")
            else:
                print(f"\tCongratulations! you can already enter the leader board!")

        else:
            msg = "No high scores!"
            middle = (int) (middle - len(msg))
            leadingBlank = ''.join([" "] * middle)
            self.__boldPrint(f"{leadingBlank}{B+Y}No high scores!{R}")

    def getScoreName(self):
        name = ""

        while name == "":
            print("Please provide a name: ")
            name = input(self.__CMD_PREFIX + ' ')
        name = name[:20]
        
        return name