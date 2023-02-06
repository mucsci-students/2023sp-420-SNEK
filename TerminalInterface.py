from UserInterface import UserInterface
from colorama import Fore, Back, Style
from Commands import Commands


class TerminalInterface(UserInterface):

    def __init__(self) -> None:
        super().__init__()
        self.__CMD_PRFX = Style.BRIGHT + Fore.BLUE + ">>" + Style.RESET_ALL
        self.__DONE_PROGRESS = Fore.YELLOW + "⬢" + Style.RESET_ALL
        self.__LEFT_PROGRESS = "⬡" + Style.RESET_ALL

    def __getUserInput(self, message: str = "") -> str:
        userInput = input(self.__CMD_PRFX + message + " ").strip()
        return userInput

    def __boldPrint(self, message: str, endStr: str = "\n") -> None:
        print(Style.BRIGHT + message + Style.RESET_ALL, end=endStr)

    def __titleDescriptionPrint(self, title: str, description: str) -> None:
        print(title)
        if description != "":
            print("\t" + description)

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

    def showStatus(self) -> None:
        pass

    def showProgress(self, progress) -> None:
        level = "Good Start"
        print(Style.BRIGHT + f"\n  {level:12s} ", end=Style.RESET_ALL)
        status = 0
        print(" 🍯  ", end="")

        while status < 8/9 and status < progress:
            print(self.__DONE_PROGRESS + "╶──", end="")
            status += 1/9

        while status < 8/9:
            print(self.__LEFT_PROGRESS + "╶──", end="")
            status += 1/9

        if status < progress:
            print(self.__DONE_PROGRESS + "  🐝")
        else:
            print(self.__LEFT_PROGRESS + "  🐝")

    def showPuzzle(self, letters: list, progress: float) -> None:
        self.showProgress(progress)
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
						╲___╱ '''.format(N + letters[1] + YB,
                       N + letters[2] + YB,
                       N + letters[3] + YB,
                       Y + letters[0] + YB,
                       N + letters[4] + YB,
                       N + letters[5] + YB,
                       N + letters[6] + YB)
              + Style.RESET_ALL)

    def showError(self, errorMessage, errorDescription="") -> None:
        self.__titleDescriptionPrint(
            Style.BRIGHT + Fore.RED + errorMessage + Style.RESET_ALL, errorDescription)

    def showHelp(self) -> None:
        self.__boldPrint("Found Words:")

    def showRanking(self, rankingLables: list, rankingPoints) -> None:  # Ns Hulio
        print("The ranking points change based on the specific game you are playing:")
        self.__boldPrint("Ranking for this game:")
        for lable, points in zip(rankingLables, rankingPoints):
            print("\t" + f"{lable:10}" + ": " + str(points))

    def showFoundWords(self, foundWords: list) -> None:
        self.__boldPrint("Found Words:")
        for word in foundWords:
            print("\t" + word)

    def showEnd(self) -> None:
        print("				🐝")

        self.__boldPrint("Congratulations!", endStr=" ")
        print("You found all the words!")
        print("\tYou are the " + Fore.LIGHTYELLOW_EX +
              "bee" + Fore.RESET + "st\t\t	🍯")

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

        confirmation = choice != okStr
        return confirmation

    def showMessage(self, message, endStr="\n"):
        print(message, end=endStr)
