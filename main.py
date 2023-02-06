from DataSource import *
from UserInterface import *
from GameController import *
from Commands import Commands


class Main():
    __EXIT_MSG = "Do you want to exit the game? (You'll be able to save it)"
    __SAVE_MSG = "Do you want to save the game?"
    __OVERRIDE_MSG = "Do you want to overwrite the game?"
    __STILL_LLOAD_MSG = "Do you want to load another game?"
    __NO_GAME_TITLE = "Not Currently in game:"

    @property
    def __NO_GAME_DESC(description):
        return f"You can't {description} a game if you are not playing one."

    def __init__(self, myGameController: GameController, myUserInterface: UserInterface) -> None:
        self.myGameController = myGameController
        self.myUserInterface = myUserInterface
        self.exitProgram = False
        self.playing = False

    def __saveGame(self, normalMode, overMode):
        saveFileName = self.myUserInterface.getSaveFileName()
        saveNum = self.myGameController.isSaved(saveFileName)
        if saveNum != -1:
            while saveGame and saveNum != -1:
                self.myUserInterface.showError(
                    "That file name is already in use.")
                saveGame = self.myUserInterface.getConfirmation(
                    self.__OVERRIDE_MSG)
                if saveGame:
                    try:
                        saveFileName = self.myUserInterface.getSaveFileName()
                        self.myGameController.save(
                            saveFileName, overMode)
                        self.playing = False
                    except:
                        self.myUserInterface.showError(
                            "Something went wrong with the saveing.", "Sorry, try again.")
                        return
        else:
            try:
                self.myGameController.save(saveFileName, normalMode)
            except:
                self.myUserInterface.showError(
                    "Something went wrong with the saveing.", "Sorry, try again.")

            self.playing = False

    def __askForSaveing(self) -> None:
        saveGame = self.myUserInterface.getConfirmation(self.__SAVE_MSG)
        if saveGame:
            scrachMode = self.myUserInterface.getConfirmation(
                "How do you want to save?", okStr="scrach", nokStr="current")
            if scrachMode:
                self.__saveGame("scrach", "overS")
            else:
                self.__saveGame("current", "overC")

    def __askExitAndSave(self) -> None:
        exitGame = self.myUserInterface.getConfirmation(self.__EXIT_MSG)
        if exitGame:
            self.playing = False
            self.__askForSaveing()

    def __askForLoading(self) -> None:
        saveFileName = self.myUserInterface.getSaveFileName()
        saveNum = self.myGameController.isSaved(saveFileName)
        loadGame = True
        while loadGame and saveNum == -1:
            self.myUserInterface.showError("That file does not exist.")
            loadGame = self.myUserInterface.getConfirmation(
                self.__STILL_LLOAD_MSG)
            if loadGame:
                saveFileName = self.myUserInterface.getSaveFileName()
                saveNum = self.myGameController.isSaved(saveFileName)

        if loadGame:
            try:
                self.myGameController.loadGame(
                    saveFileName)
                self.playing = True
                self.__playGame()
            except:
                self.myUserInterface.showError(
                    "Something went wrong with the loading.", "Sorry, try again.")

    def __playGame(self) -> None:
        while self.playing and not self.myGameController.gameEnded():
            myPuzzle = self.myGameController.getPuzzle()
            self.myUserInterface.showPuzzle(myPuzzle)
            userInput = self.myUserInterface.getUserInput()
            if Commands.isCommand(userInput):
                self.processCommand(userInput)
            elif not self.myGameController.makeGuess(userInput):
                self.myUserInterface.showWrongGuess(userInput)

        if self.myGameController.gameEnded():
            self.myUserInterface.showEnd()

    def processCommand(self, command) -> None:
        if command == Commands.EXIT:
            if self.playing:
                self.__askExitAndSave()
            else:
                self.exitProgram = True

        elif command == Commands.HELP:
            self.myUserInterface.showHelp()

        elif command == Commands.LOAD:
            if self.playing:
                exitGame = self.myUserInterface.getConfirmation(
                    self.__EXIT_MSG)
                if exitGame:
                    self.playing = False
                    self.__askForSaveing()
                    self.__askForLoading()
            else:
                self.__askForLoading()

        elif command == Commands.SAVE:
            if self.playing:
                scrachMode = self.myUserInterface.getConfirmation(
                    "How do you want to save?", okStr="scrach", nokStr="current")
                if scrachMode:
                    self.__saveGame("scrach", "overS")
                else:
                    self.__saveGame("current", "overC")
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("save"))

        elif command == Commands.RANK:
            if self.playing:
                rank = self.myGameController.getRank()
                self.myUserInterface.showRank(rank)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("the rank of"))

        elif command == Commands.GUESSED_WORDS:
            if self.playing:
                guessedWords = self.myGameController.getGuessedWords()
                self.myUserInterface.showGuessedWords(guessedWords)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("show guessed words"))

        elif command == Commands.SHUFFLE:
            if self.playing:
                self.myGameController.shuffle()
                myPuzzle = self.myGameController.getPuzzle()
                self.myUserInterface.showPuzzle(myPuzzle)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("shuffle letters of"))

        elif command == Commands.NEW_GAME_RND:
            if self.playing:
                self.__askExitAndSave()
            else:
                self.myGameController.newPuzzle()
                self.playing = True
                self.__playGame()

        elif command == Commands.NEW_GAME_WRD:
            if self.playing:
                self.__askExitAndSave()
            else:
                baseWord = self.myUserInterface.getBaseWord()
                self.myGameController.newPuzzle(baseWord)
                self.playing = True
                self.__playGame()
        else:
            self.myUserInterface.showError(
                "Not a valid command:", 'Type "Help" to show all posibilities')


def main():
    myDataSource = DataSource()
    myGameController = GameController(myDataSource)
    myUserInterface = UserInterface()

    myMain = Main(myGameController, myUserInterface)

    while not myMain.exitProgram:
        command = myUserInterface.getCommand()
        myMain.processCommand(command)


if __name__ == "__main__":
    main()
