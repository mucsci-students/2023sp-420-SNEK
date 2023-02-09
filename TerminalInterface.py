from UserInterface import UserInterface
from colorama import Fore, Back, Style
from Commands import Commands
from math import sqrt


class TerminalInterface(UserInterface):

    def __init__(self) -> None:
        super().__init__()
        self.__CMD_PRFX = Style.BRIGHT + Fore.BLUE + ">>" + Style.RESET_ALL
        self.__DONE_PROGRESS = Fore.YELLOW + "⬢" + Style.RESET_ALL
        self.__LEFT_PROGRESS = "⬡" + Style.RESET_ALL
        self.__RANK_LABELS = ["Beginner", "Good Start", "Moving Up", "Good",
                              "Solid", "Nice", "Great", "Amazing", "Genius"]
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
   Call commands with a preceeding '!'. Commands may be
   called at anytime.

   -!new rnd - Generate a new random puzzle
   -!new wrd - Genereate a new puzzle with a user given
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

    def __getUserInput(self, message: str = "") -> str:
        userInput = input(self.__CMD_PRFX + message + " ").strip()
        return userInput

    def __boldPrint(self, message: str, endStr: str = "\n") -> None:
        print(Style.BRIGHT + message + Style.RESET_ALL, end=endStr)

    def __titleDescriptionPrint(self, title: str, description: str) -> None:
        print(title)
        if description != "":
            print("\t" + description)

    def __rankLablePoints(self, lableList: list, maxPoints: int) -> dict:
        n = len(lableList)
        if maxPoints < (n - 1):
            return None

        rankingFunction: function = lambda x: (maxPoints/((n-1)**2)) * x**2

        pointList = [round(rankingFunction(i)) for i in range(n)]
        for i in range(1, n-1):
            if pointList[i] <= pointList[i-1]:
                pointList[i] += (pointList[i-1] - pointList[i] + 1)
                pointList[i+1] -= (pointList[i-1] - pointList[i] + 1)

        rankDict = dict(zip(lableList, pointList))
        return rankDict

    def getUserInput(self):
        userInput = self.__getUserInput()

        if Commands.isCommand(userInput):
            return Commands.getCommandFromName(userInput)
        else:
            return userInput

    def getBaseWord(self) -> str:
        baseWord = self.__getUserInput(" Base word:")
        return baseWord

    def getCommand(self) -> Commands:
        command = self.__getUserInput()

        while not Commands.isCommand(command):
            command = self.__getUserInput()

        return Commands.getCommandFromName(command)

    def showStatus(self, status, points) -> None:
        rankLabels = self.__RANK_LABELS
        ranks: dict = self.__rankLablePoints(rankLabels, maxPoints)
        for i, rank in enumerate(rankLabels):
            if points == ranks[rank]:
                level = rank
                break
            elif points < ranks[rank]:
                level = rankLabels[i-1]
                break

        self.__boldPrint(level + ": " + str(points))

    def showProgress(self, points, maxPoints) -> None:
        rankLabels = self.__RANK_LABELS
        ranks: dict = self.__rankLablePoints(rankLabels, maxPoints)
        for i, rank in enumerate(rankLabels):
            if points == ranks[rank]:
                level = rank
                break
            elif points < ranks[rank]:
                level = rankLabels[i-1]
                break

        rankItems = list(ranks.items())

        print(Style.BRIGHT + f"\n  {level:12s} ", end=Style.RESET_ALL)
        print(" 🍯  ", end="")
        if points > rankItems[0][1]:
            print(self.__DONE_PROGRESS + "╶──", end="")
        else:
            print(self.__LEFT_PROGRESS + "╶──", end="")

        for rank, rankPoints in rankItems[1:-1]:
            if points >= rankPoints:
                print(self.__DONE_PROGRESS + "╶──", end="")
            else:
                print(self.__LEFT_PROGRESS + "╶──", end="")

        if points >= rankItems[-1][1]:
            print(self.__DONE_PROGRESS + "  🐝")
        else:
            print(self.__LEFT_PROGRESS + "  🐝")

    def showPuzzle(self, letters: list, progress: float) -> None:
        myLetters = list(''.join(letters).upper())
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

    def showError(self, errorMessage, errorDescription="") -> None:
        self.__titleDescriptionPrint(
            Style.BRIGHT + Fore.RED + errorMessage + Style.RESET_ALL, errorDescription)

    def showHelp(self) -> None:
        self.__boldPrint(self.__HELP_TITLE)
        print(self.__HELP_STRING)

    def showRanking(self, maxPoints: int) -> None:
        print("The ranking points change based on the specific game you are playing:")
        self.__boldPrint("Ranking for this game:")
        rankingPoints: dict = self.__rankLablePoints(
            self.__RANK_LABELS, maxPoints)
        for lable in self.__RANK_LABELS:
            points = rankingPoints[lable]

            print("\t" + f"{lable:10}" + ": " + str(points))

    def showFoundWords(self, foundWords: list) -> None:
        self.__boldPrint("Found Words:")
        for word in foundWords:
            print("\t" + word)

    def showEnd(self) -> None:
        print("                🐝")

        self.__boldPrint("Congratulations!", endStr=" ")
        print("You found all the words!")
        print("\tYou are the " + Fore.LIGHTYELLOW_EX +
              "bee" + Fore.RESET + "st\t\t    🍯")

    def showExit(self) -> None:
        self.__boldPrint("Exiting...")

    def showWrongGuess(self) -> None:
        self.__boldPrint("Wrong guess...")

    def getSaveFileName(self) -> str:  # What if the path/dir dosen't exist?
        self.__boldPrint("Desired save file: ")
        path = self.__getUserInput()
        return path

    def showGuessedWords(self, guessedWords: list) -> None:
        self.__boldPrint("Guessed Words:")
        for word in guessedWords:
            print("\t" + word)

    def getConfirmation(self, message, okStr="Y", nokStr="N"):
        okStr = okStr.lower()
        nokStr = nokStr.lower()
        self.__boldPrint(message + f"[{okStr}/{nokStr}]: ")
        choice = str(self.getUserInput()).lower()
        while choice != okStr and choice != nokStr:
            print(f"(Unrecogniced choice) [{okStr}/{nokStr}]: ")
            choice = self.getUserInput().lower()

        confirmation = choice == okStr
        return confirmation

    def showMessage(self, message, endStr="\n"):
        print(message, end=endStr)
