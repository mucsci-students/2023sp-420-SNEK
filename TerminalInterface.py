from UserInterface import UserInterface
from colorama import Fore, Style
from Commands import Commands


class TerminalInterface(UserInterface):

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

   -!new rnd - Generate a new random puzzle
   -!new wrd - Generate a new puzzle with a user given
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

    def launch(self):
        while not self.quit:
            userInput = self.__getUserInput()
            self.myController.processInput(userInput)

    def __getUserInput(self, message: str = "") -> str:
        userInput = input(self.__CMD_PREFIX + message + " ").strip()
        return userInput

    def __boldPrint(self, message: str, endStr: str = "\n") -> None:
        print(Style.BRIGHT + message + Style.RESET_ALL, end=endStr)

    def __titleDescriptionPrint(self, title: str, description: str) -> None:
        print(title)
        if description != "":
            print("\t" + description)

    def getBaseWord(self) -> str:
        baseWord = self.__getUserInput(" Base word:")
        return baseWord

    def showStatus(self, rank: str, points: int) -> None:
        self.__boldPrint(rank + ": " + str(points))

    def showProgress(self, rank: str, thresholds: list[int], points: int, maxPoints: int) -> None:
        print(Style.BRIGHT + f"\n  {rank:12s} ", end=Style.RESET_ALL)
        print(" 🍯  ", end="")
        if points > thresholds[1]:
            print(self.__DONE_PROGRESS + "╶──", end="")
        else:
            print(self.__LEFT_PROGRESS + "╶──", end="")

        for rank, rankPoints in thresholds[1:-1]:
            if points >= rankPoints:
                print(self.__DONE_PROGRESS + "╶──", end="")
            else:
                print(self.__LEFT_PROGRESS + "╶──", end="")

        if points >= thresholds[1]:
            print(self.__DONE_PROGRESS + "  🐝")
        else:
            print(self.__LEFT_PROGRESS + "  🐝")

    def showPuzzle(self, letters: str) -> None:
        myLetters = letters.upper()
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

    def showRanking(self, rankingsAndPoints: dict[str, int]) -> None:
        print("The ranking points change based on the specific game you are playing:")
        self.__boldPrint("Ranking for this game:")
        for label, points in rankingsAndPoints:
            print("\t" + f"{label:10}" + ": " + str(points))

    def showEnd(self) -> None:
        print("                🐝")
        self.__boldPrint("Congratulations!", endStr=" ")
        print("You found all the words!")
        print("\tYou are the " + Fore.LIGHTYELLOW_EX +
              "bee" + Fore.RESET + "st\t\t    🍯")

    def showExit(self) -> None:
        self.__boldPrint("Exiting...")

    def showWrongGuess(self, message="") -> None:
        self.__boldPrint("Wrong guess", end="")
        if message == "":
            print("...")
        else:
            print(": " + message)

    def showCorrectGuess(self) -> None:
        self.__boldPrint("Good guess!")

    def getSaveFileName(self) -> str:
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
        self.__boldPrint(message + f" [{okStr}/{nokStr}]: ")
        choice = str(self.getUserInput()).lower()
        while choice != okStr and choice != nokStr:
            print(f"(Unrecognized choice) [{okStr}/{nokStr}]: ")
            choice = self.getUserInput().lower()

        confirmation = choice == okStr
        return confirmation

    def showMessage(self, message, endStr="\n"):
        print(message, end=endStr)
