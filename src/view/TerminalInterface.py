from view.UserInterface import UserInterface
from colorama import Fore, Style, Back
from view.Inputer import Inputer
from model.Puzzle import Puzzle
from model.Commands import *
from model.Hint import Hint


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
        self.__CMD_PREFIX: str = Style.BRIGHT + Fore.BLUE + Back.BLACK + "\n>>" + Style.RESET_ALL + Back.BLACK
        self.__DONE_PROGRESS: str = Fore.YELLOW + "⬢" + Style.RESET_ALL + Back.BLACK
        self.__LEFT_PROGRESS: str = "⬡" + Style.RESET_ALL + Back.BLACK
        self.__TITLE:str = f'''{Back.BLACK}
    ┌───────────────────────┬─────────────────────────────────┐
    │ Team {Fore.LIGHTGREEN_EX}SNEK{Fore.RESET + Back.BLACK} presents:   │  Type {Fore.LIGHTBLUE_EX}!help{Fore.RESET + Back.BLACK} to show how to play │
    │     {Fore.LIGHTYELLOW_EX}SPELLING BEE{Fore.RESET + Back.BLACK}      │    And don't forget to enjoy!   │
    └───────────────────────┴─────────────────────────────────┘\n''' + Back.BLACK

        self.__HELP_TITLE: str = f"{Back.BLACK}\n\tSpelling Bee Game!              🍯 🐝"
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
'''
        self.__HELP_COMMANDS: str = f'''
Commands:
   Call commands with a preceding '{Fore.LIGHTBLUE_EX}!{Fore.RESET + Back.BLACK}'. Commands may be called at anytime.

   -{Fore.LIGHTBLUE_EX}!new random{Fore.RESET + Back.BLACK} - Generate a new random puzzle.
   -{Fore.LIGHTBLUE_EX}!new word{Fore.RESET + Back.BLACK} - Generate a new puzzle with a user given word. Console will
                prompt for the word after command is given.
   -{Fore.LIGHTBLUE_EX}!scores{Fore.RESET + Back.BLACK} - Displays both the high scores for the puzzle and the current 
              score for the player.
   -{Fore.LIGHTBLUE_EX}!save{Fore.RESET + Back.BLACK} - Bring up the prompts for saving your current game.
   -{Fore.LIGHTBLUE_EX}!save secret{Fore.RESET + Back.BLACK} - Bring up the prompts for saving your game with encryption.
   -{Fore.LIGHTBLUE_EX}!save image{Fore.RESET + Back.BLACK} - Saves image of the CLI honeycomb.
   -{Fore.LIGHTBLUE_EX}!load{Fore.RESET + Back.BLACK} - Bring up the prompts for loading a saved game.
   -{Fore.LIGHTBLUE_EX}!scores{Fore.RESET + Back.BLACK} - Display the scoreboard for the current game and current points.
   -{Fore.LIGHTBLUE_EX}!rank{Fore.RESET + Back.BLACK} - Display available ranks and point thresholds per rank.
   -{Fore.LIGHTBLUE_EX}!shuffle{Fore.RESET + Back.BLACK} - Shuffle the shown puzzle honeycomb randomly, other than the 
               required center letter.
   -{Fore.LIGHTBLUE_EX}!guessed{Fore.RESET + Back.BLACK} - Shows all the already correctly guessed words.
   -{Fore.LIGHTBLUE_EX}!hints{Fore.RESET + Back.BLACK} - Prints out all the hints for the given puzzle.
   -{Fore.LIGHTBLUE_EX}!help{Fore.RESET + Back.BLACK} - Prints out the help menu.
   -{Fore.LIGHTBLUE_EX}!exit{Fore.RESET + Back.BLACK} - Exits the game. Will prompt to save.
   -{Fore.LIGHTBLUE_EX}!quit{Fore.RESET + Back.BLACK} - Exits the entire program. Will prompt to save.'''

    def __makeBackgroundBlack(self):
        if os.name == "posix":
            # Unix/Linux/MacOS/BSD/etc
            os.system('setterm -background black -foreground white -store')
        elif os.name in ("nt", "dos", "ce"):
            # DOS/Windows
            os.system('color 07')
            # os.system('color 7f')


    def __cls(self, numLines=100):

        if os.name == "posix":
            # Unix/Linux/MacOS/BSD/etc
            os.system('clear')
            
        elif os.name in ("nt", "dos", "ce"):
            # DOS/Windows
            os.system('CLS')
        else:
            # Fallback for other operating systems.
            print('\n' * numLines)

    def __clear(self):
        self.__cls()
        self.__makeBackgroundBlack()
        print(self.__TITLE)

    # Launch terminal interface and gets user input and processes
    # input while the game is not quit
    def launch(self):
        self.__clear()
        self.showHelp()
        self.__clear()

        try:
            commandStrings = Commands.getCommandNameList()
            while not self.quit:
                userInput = self.__getUserInput(options=commandStrings)
                if Commands.isCommand(userInput):
                    userInput = Commands.getCommandFromName(userInput)

                self.__clear()
                self.myController.processInput(userInput)
        except:
            sys.stdout.flush()
            self.showError("Exiting...", "Unexpected error.")
            exit()

    # Flag if the game is quit
    def quitInterface(self):
        self.__cls()
        self.quit = True

    # Gets user input from cli and checks if there is a command that
    # a user wants to use
    def __getUserInput(self, message: str = "", options=[]) -> str:
        userInput = self.myInputer.input(self.__CMD_PREFIX + message + " ", options).strip().lower()

        return userInput

    # Path in directory that the user wants to save their games
    def __getUserInputPath(self, message: str = "") -> str:
        userInput = self.myInputer.inputPath(self.__CMD_PREFIX + message + " ").strip()

        return userInput

    # Reset colorama text so that it does not
    # change other text to a bold print
    def __boldPrint(self, message: str, endStr: str = "\n") -> None:
        print(Style.BRIGHT + message + Style.RESET_ALL + Back.BLACK, end=endStr)

    # Print name of error on cli
    def __titleDescriptionPrint(self, title: str, description: str) -> None:
        print(title)
        if description != "":
            print("\t" + description)

    # Print the words base word so that the user can
    # enter what base word they want to use for the puzzle
    def getBaseWord(self) -> str:
        self.__boldPrint("\nBase word: ")
        baseWord = input(self.__CMD_PREFIX + " ").lower().strip()

        self.__clear()

        return baseWord
        


    # Progress bar that shows users current rank and and displays it
    # in a nice progress bar that shows how many ranks in you are and
    # how many ranks are left to get to top rank
    def showProgress(self, rank: str, thresholds: list[int], currentPoints: int) -> None:
        rankAndPoints = f"{rank} ({currentPoints})"
        print(Style.BRIGHT + f"\n  {rankAndPoints:16s} ", end=Style.RESET_ALL + Back.BLACK)
        print(" 🍯  ", end="")
        if currentPoints == 0:
            print(self.__LEFT_PROGRESS + "╶──", end="")
        else:
            print(self.__DONE_PROGRESS + "╶──", end="")

        maxPoints = thresholds[-1]
        for rankPoints in thresholds[1:-1]:
            if currentPoints >= rankPoints and currentPoints != 0:
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
        self.showProgress(myPuzzle.getCurrentRank(), list(
            myPuzzle.getRankingsAndPoints().values()), myPuzzle.getCurrentPoints())
        myLetters = ''.join(myPuzzle.getPuzzleLetters()).upper()
        YB = Fore.YELLOW + Style.BRIGHT
        N = Fore.WHITE + Style.NORMAL
        Y = Fore.YELLOW
        B = Fore.LIGHTBLUE_EX
        NB = Fore.WHITE + Style.BRIGHT
        W = Style.RESET_ALL + Fore.WHITE  + Back.BLACK
        guessed = myPuzzle.getGuessedWords().copy()
        n: int = len(guessed)
        if n < 12:
            guessed.reverse()
            guessed = guessed + ['--'] * (12 - n)
        else:
            guessed = guessed[-12:]
            guessed.reverse()

        print('''                      {}┌──────────────────────────────────────┐{}
          ___         {}│         {}Recently found words:{}        │{}
      ___╱ {} ╲___     {}│ {}  {} │{}
     ╱ {} ╲___╱ {} ╲    {}│ {}  {} │{}
     ╲___╱ {} ╲___╱    {}│ {}  {} │{}
     ╱ {} ╲___╱ {} ╲    {}│ {}  {} │{}
     ╲___╱ {} ╲___╱    {}│ {}  {} │{}
         ╲___╱        {}│ {}  {} │{}
                      {}└──────────────────────────────────────┘{}'''
        .format(B, YB,
                B, NB, B, YB,
                N + myLetters[1] + YB, B, W + guessed[0].center(17), guessed[1].center(17) + B, YB,
                N + myLetters[2] + YB, N + myLetters[3] + YB, B, W + guessed[2].center(17), guessed[3].center(17) + B, YB,
                Y + myLetters[0] + YB, B, W + guessed[4].center(17), guessed[5].center(17) + B, YB,
                N + myLetters[4] + YB, N + myLetters[5] + YB, B, W + guessed[6].center(17), guessed[7].center(17) + B, YB,
                N + myLetters[6] + YB, B, W + guessed[8].center(17), guessed[9].center(17) + B, YB,
                B, W + guessed[10].center(17), guessed[11].center(17) + B, YB,
                B, Style.RESET_ALL  + Back.BLACK)
      )

    # Prints errors in the cli when a a user does not use the right command
    def showError(self, errorMessage, errorDescription="") -> None:
        self.__titleDescriptionPrint(
            Style.BRIGHT + Fore.RED + errorMessage + Style.RESET_ALL + Back.BLACK, errorDescription)

    # If the user types !help command, then it will print the help
    # instructions on how to play the game
    def showHelp(self) -> None:
        self.__boldPrint(self.__HELP_TITLE)
        print(self.__HELP_STRING)
        print("\nShow commands as well? [y/n]")
        choice = self.__getQuickInput('y', 'n', 'c')
        if choice == 'y':
            print(self.__HELP_COMMANDS)
            self.__hold()
        else:
            self.__clear()

    # Print rankings based on what puzzle is open and it shows how
    # many points the user needs to achieve the next rank status
    def showRanking(self, rankingsAndPoints: dict[str, int]) -> None:
        print("\nThe ranking points change based on the specific game you are playing.")
        self.__boldPrint("\nRanking for this game:\n")
        ranks = list(rankingsAndPoints.items())
        ranks.reverse()
        for label, points in ranks:
            print("\t" + f"{label:10}" + ": " + str(points))
            
        self.__hold()

    # If the user completes the game, then it will print an end
    # screen that the user has found all the words
    def showEnd(self) -> None:
        print("\n\n                🐝")
        self.__boldPrint("Congratulations!", endStr=" ")
        print("You found all the words!")
        print("\tYou are the " + Fore.LIGHTYELLOW_EX +
              "bee" + Fore.RESET + Back.BLACK + "st\t\t    🍯\n\n")

    # Prints Exiting when a user wants to exit a puzzle
    def showExit(self) -> None:
        self.__boldPrint(Fore.BLUE + "Game exited." + Fore.RESET + Back.BLACK)
        self.__boldPrint("You are at the main program", endStr=Fore.LIGHTWHITE_EX + " (not playing).\n\n" + Fore.RESET + Back.BLACK)

    # If a user does not make a right guess, then it will
    # print that they did not make a right guess
    def showWrongGuess(self, message="") -> None:
        self.__boldPrint(Fore.RED + "Wrong guess" + Fore.RESET + Back.BLACK, endStr="")
        if message == "":
            print(Fore.RED +"..." + Fore.RESET + Back.BLACK)
        else:
            print(Fore.RED +": \n\t" + Fore.RESET + Back.BLACK + message)

    # When a user makes the right guess, then it will
    # tell the user that they made the right guess
    def showCorrectGuess(self, word:str) -> None:
        self.__boldPrint(Fore.GREEN + "Good guess!" + Fore.RESET + Back.BLACK)
        print(f"\t{word}")

    def __getPath(self, extension, SaveOrLoad) -> str:
        baseDir = os.getcwd()
        self.__boldPrint(f"Desired path to {SaveOrLoad}:")
        print(f"\tDefault directory: {baseDir}")
        name = self.__getUserInputPath()
        while name == "" or name == extension:
            self.showError("The file has to have a name.", "Please try again:")
            name = self.__getUserInputPath()

        name = name if name.endswith(extension) else name + extension

        if not os.path.isabs(name):
            name = os.path.join(baseDir, name)

        fileName = os.path.normpath(name)

        self.__clear()

        return fileName

    # When a user wants to open their saved game, then it will
    # ask what save file they want to open
    def getSaveFileName(self, extension) -> str:
        fileName = self.__getPath(extension, "save")

        if os.path.exists(fileName):
            baseName = os.path.basename(fileName)

            overwrite = self.getConfirmation(f"WARNING:\n\tThe file {baseName} already exists\n\tDo you want to overwrite it?")


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
            fileName = self.getSaveFileName(".png")
            # fileName = os.path.splitext(fileName)[0]
            # fileName = fileName + ".png"

            
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
    def getLoadFileName(self, extension) -> str:
        path = self.__getPath(extension, "load")
        return path

    # When !guessed is types, then it will print a list of all
    # the words that the user has found in the game
    def showGuessedWords(self, guessedWords: list) -> None:
        self.__boldPrint(f"Guessed Words ({len(guessedWords)}):")
        cols = os.get_terminal_size().columns
        accumulator = 4
        print("\t")
        for word in guessedWords:
            word:str = word.capitalize()
            if accumulator + 22 < cols:
                print(f" {word:^20s} ", end="")
                accumulator += 22
            else:
                print(f"\n {word:^20s} ", end="")
                accumulator = 26
        
        self.__hold()


    def __getQuickInput(self, okStr, nokStr, canStr):
        choice = self.myInputer.quickInput(self.__CMD_PREFIX + " ", [okStr, nokStr, canStr])
        self.__clear()
        return choice

    # Confirmation for save and load for games and if it is not
    # yes or no, then it will tell the user that their input
    # is not recognized and will wait for the right input
    def getConfirmation(self, message:str, okStr="", nokStr="", canStr=""):
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

        if "WARNING:" in message:
            pieces = message.split("WARNING:", 1)
            message = pieces[0] + f"{Fore.MAGENTA}WARNING:{Fore.RESET + Back.BLACK}" + pieces[1]

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

        self.__clear()
        return choice

    # Prints messages in cli
    def showMessage(self, message, endStr="\n"):
        print(message, end=endStr)

    def showHints(self, myPuzzle: Puzzle):
        myHints: Hint = myPuzzle.getHint()
        puzzleLetters = myPuzzle.getPuzzleLetters()

        self.__boldPrint("             🐝\nBᴇᴇ Gʀɪᴅ Hɪɴᴛs")
        self.__boldPrint("\t● Puzzle Letters ", endStr="")
        print("(Required first):  ", end="")
        self.__boldPrint(
            Fore.YELLOW + puzzleLetters[0].upper() + Style.RESET_ALL + Back.BLACK, endStr=" ")
        for letter in puzzleLetters[1:]:
            print(letter.upper(), end=" ")
        print()
        self.__boldPrint("\t● Words: ", endStr="")
        print(f"{myHints.numberOfWords}  ({myPuzzle.getMaxPoints()} points total)")
        self.__boldPrint("\t● Pangrams: ", endStr="")
        print(f"{myHints.pangram}  ", end="")
        if myHints.perfectPangram > 0:
            print(f"({myHints.perfectPangram} perfect)")
        else:
            print()


        # Print matrix
        bingo = "\tBingo" if myHints.bingo else "\n"
        self.__boldPrint("\n\t● Hint matrix:", endStr=bingo)
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

        self.__boldPrint("\n\n\t● Two letter list:", endStr="")
        # Print 2 letter lists
        previousLetter = None
        for firstLetters, num in myHints.beginningList.items():
            if previousLetter != firstLetters[0]:
                previousLetter = firstLetters[0]
                print("\n", end="\t   ")
            print(f"  {firstLetters.upper()} → {num:<4}", end="")

        self.__hold()


    def __hold(self):
        self.__boldPrint("\n\n\t" + Style.BRIGHT + Fore.BLUE + "Press ENTER to exit the page and continue..." + Style.RESET_ALL + Back.BLACK)
        input()
        self.__clear()

    def showHighScores(self, myPuzzle: Puzzle, isEnd = False):
        B = Style.BRIGHT
        Y = Fore.YELLOW
        R = Style.RESET_ALL + Back.BLACK
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
            if isEnd:
                if difference < 0:
                    self.__boldPrint("Congrats! :)")
                    print("\tYour score is now entered into the top 10 leaderboard for this puzzle!\n")
                else:
                    self.__boldPrint("Sorry! :(")
                    print("\tYour score is NOT high enough to enter into the top 10 leaderboard for this puzzle.\n")
            else:
                self.__boldPrint(f"You have {currentPoints} points:")
                if difference == 0:
                    print(f"\tJust one more guess and you'll be able to enter the leaderboard.")
                elif difference > 0:
                    print(f"\tYou are {difference} points away form entering the leaderboard.")
                else:
                    print(f"\tCongratulations! You can already enter the leader board!")

            self.__hold()

        else:
            print(f"{B+Y}There are no high scores! {R} :(")
            self.__boldPrint("\tTry to exit the game to save your's and be part of the leaderboard!\n")

        
        

    def getScoreName(self):
        name = ""

        while name == "":
            print("Please provide a name: ")
            name = input(self.__CMD_PREFIX + ' ')
        name = name[:20]
        
        return name