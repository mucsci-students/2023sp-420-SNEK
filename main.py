from DataSource import *
from UserInterface import *
from GameController import *
from Commands import Commands
from TerminalInterface import TerminalInterface
from State import State


class Main():
    __EXIT_MSG = "Do you want to exit the game? (You'll be able to save it)"
    __SAVE_MSG = "Do you want to save the game?"
    __OVERRIDE_MSG = "Do you want to overwrite the game?"
    __STILL_LLOAD_MSG = "Do you want to load another game?"
    __NO_GAME_TITLE = "Not Currently in game:"

    def __NO_GAME_DESC(self, description):
        return f"You can't {description} a game if you are not playing one."

    def __init__(self, myGameController: GameController, myUserInterface: UserInterface) -> None:
        self.myGameController = myGameController
        self.myUserInterface = myUserInterface
        self.exitProgram = False
        self.playing = False
        self.newLoad = False

    def __saveGame(self, normalMode, overMode):
        saveFileName = self.myUserInterface.getSaveFileName()
        puzzle: Puzzle = self.myGameController.getPuzzle()
        state: State = puzzle.getState()
        try:
            saveNum = state.isSaved(saveFileName)
        except MasterFileNotFound:
            saveNum = -1
        if saveNum != -1:
            saveGame = True
            while saveGame and saveNum != -1:
                self.myUserInterface.showError(
                    "That file name is already in use.")
                saveGame = self.myUserInterface.getConfirmation(
                    self.__OVERRIDE_MSG)
                if saveGame:
                    try:
                        puzzle = self.myGameController.getPuzzle()
                        state = puzzle.getState()
                        state.save(saveFileName, overMode)
                        self.playing = True
                    except:
                        self.myUserInterface.showError(
                            "Something went wrong with the saveing.", "Sorry, try again.")
                    return
        else:
            try:
                puzzle = self.myGameController.getPuzzle()
                state = puzzle.getState()
                state.save(saveFileName, normalMode)
                self.playing = True
            except:
                self.myUserInterface.showError(
                    "Something went wrong with the saveing.", "Sorry, try again.")

    def __askForSaveing(self) -> None:
        saveGame = self.myUserInterface.getConfirmation(self.__SAVE_MSG)
        if saveGame:
            scratchMode = self.myUserInterface.getConfirmation(
                "How do you want to save?", okStr="scratch", nokStr="current")
            if scratchMode:
                self.__saveGame("scratch", "overS")
            else:
                self.__saveGame("current", "overC")

    def __askExitAndSave(self) -> None:
        exitGame = self.myUserInterface.getConfirmation(self.__EXIT_MSG)
        if exitGame:
            self.playing = False
            self.__askForSaveing()
        else:
            return -1

    def __askForLoading(self) -> None:
        saveFileName = self.myUserInterface.getSaveFileName()
        puzzle = self.myGameController.getPuzzle()
        state: State = puzzle.getState()
        try:
            saveNum = state.isSaved(saveFileName)
        except MasterFileNotFound:
            self.myUserInterface.showError("That file does not exist.")
        loadGame = True
        while loadGame and saveNum == -1:
            self.myUserInterface.showError("That file does not exist.")
            loadGame = self.myUserInterface.getConfirmation(
                self.__STILL_LLOAD_MSG)
            if loadGame:
                saveFileName = self.myUserInterface.getSaveFileName()
                puzzle = self.myGameController.getPuzzle()
                state = puzzle.getState()
                saveNum = state.isSaved(saveFileName)

        if loadGame:
            self.newLoad = True
            retVal = state.load(saveFileName)
            if(retVal == -1):
                print("No save file folder created.")
                return
            elif(retVal == -2):
                print("No save file of that name found.")
                return
            self.playing = True
            self.__playGame()

    def __playGame(self) -> None:
        self.newLoad = False
        while self.playing and not self.myGameController.gameOver and not self.newLoad:
            myPuzzle = self.myGameController.getPuzzle()
            print(myPuzzle.wordsList)
            statVal = self.myUserInterface.showProgress(
                myPuzzle.points, myPuzzle.numberOfLetters)
            self.myGameController.setStatus(statVal)
            self.myUserInterface.showPuzzle(
                myPuzzle.wordPuzzle, myPuzzle.points/myPuzzle.numberOfLetters)
            userInput = self.myUserInterface.getUserInput()
            if Commands.isCommand(userInput):
                self.processCommand(userInput)
            elif not self.myGameController.guess(userInput):
                self.myUserInterface.showWrongGuess()

        if self.myGameController.gameOver:
            self.myUserInterface.showEnd()
            self.playing = False
            self.myGameController.setGameOver()
            return

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
                scratchMode = self.myUserInterface.getConfirmation(
                    "How do you want to save?", okStr="scratch", nokStr="current")
                if scratchMode:
                    self.__saveGame("scratch", "overS")
                else:
                    self.__saveGame("current", "overC")
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("save"))

        elif command == Commands.RANK:
            if self.playing:
                puzzle = self.myGameController.getPuzzle()
                maxPoints = puzzle.numberOfLetters
                self.myUserInterface.showRanking(maxPoints)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("the rank of"))

        elif command == Commands.GUESSED_WORDS:
            if self.playing:
                puzzle: Puzzle = self.myGameController.getPuzzle()
                self.myUserInterface.showGuessedWords(puzzle.foundWords)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("show guessed words"))

        elif command == Commands.SHUFFLE:
            if self.playing:
                self.myGameController.shuffle()
                myPuzzle = self.myGameController.getPuzzle()
                self.myUserInterface.showPuzzle(
                    myPuzzle.wordPuzzle, myPuzzle.points/myPuzzle.numberOfLetters)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("shuffle letters of"))

        elif command == Commands.NEW_GAME_RND:
            if self.playing:
                retVal = self.__askExitAndSave()
                if(retVal == -1):
                    return
                self.myGameController = GameController()
                Puzzle.createPuzzle()
                self.playing = True
                self.__playGame()
            else:
                self.myGameController = GameController()
                Puzzle.createPuzzle()
                self.playing = True
                self.__playGame()

        elif command == Commands.NEW_GAME_WRD:
            if self.playing:
                retVal = self.__askExitAndSave()
                if(retVal == -1):
                    return
                baseWord = self.myUserInterface.getBaseWord()
                self.myGameController = GameController()
                Puzzle.createPuzzle(baseWord)
                self.playing = True
                self.__playGame()
            else:
                baseWord = self.myUserInterface.getBaseWord()
                self.myGameController = GameController()
                Puzzle.createPuzzle(baseWord)
                self.playing = True
                self.__playGame()

        elif command == Commands.SHOW_STATUS:
            if self.playing:
                myPuzzle = self.myGameController.getPuzzle()
                points = myPuzzle.getPoints()
                maxPoints = myPuzzle.numberOfLetters
                self.myUserInterface.showStatus(points, maxPoints)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("show status of"))
        else:
            self.myUserInterface.showError(
                "Not a valid command:", 'Type "Help" to show all posibilities')


def main():
    myGameController = GameController()
    myUserInterface = TerminalInterface()

    myMain = Main(myGameController, myUserInterface)

    myUserInterface.showHelp()
    while not myMain.exitProgram:
        command = myUserInterface.getCommand()
        myMain.processCommand(command)


if __name__ == "__main__":
    main()
