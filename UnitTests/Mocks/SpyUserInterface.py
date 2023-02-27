import UserInterface


class SpyUserInterface(UserInterface.UserInterface):
    def __init__(self) -> None:
        super().__init__()

        self.spyValues: dict = dict()

    def launch(self, *args):
        count = self.spyValues.get(self.launch, 0)
        self.spyValues[self.launch] = count + 1

    def quitInterface(self, *args):
        count = self.spyValues.get(self.quitInterface, 0)
        self.spyValues[self.quitInterface] = count + 1

    def getUserInput(self, *args):
        count = self.spyValues.get(self.getUserInput, 0)
        self.spyValues[self.getUserInput] = count + 1

    def getBaseWord(self, *args):
        count = self.spyValues.get(self.getBaseWord, 0)
        self.spyValues[self.getBaseWord] = count + 1

    def getCommand(self, *args):
        count = self.spyValues.get(self.getCommand, 0)
        self.spyValues[self.getCommand] = count + 1

    def showStatus(self, *args):
        count = self.spyValues.get(self.showStatus, 0)
        self.spyValues[self.showStatus] = count + 1

    def showRanking(self, *args):
        count = self.spyValues.get(self.showRanking, 0)
        self.spyValues[self.showRanking] = count + 1

    def showPuzzle(self, *args):
        count = self.spyValues.get(self.showPuzzle, 0)
        self.spyValues[self.showPuzzle] = count + 1

    def showError(self, *args):
        count = self.spyValues.get(self.showError, 0)
        self.spyValues[self.showError] = count + 1

    def showHelp(self, *args):
        count = self.spyValues.get(self.showHelp, 0)
        self.spyValues[self.showHelp] = count + 1

    def showFoundWords(self, *args):
        count = self.spyValues.get(self.showFoundWords, 0)
        self.spyValues[self.showFoundWords] = count + 1

    def showEnd(self, *args):
        count = self.spyValues.get(self.showEnd, 0)
        self.spyValues[self.showEnd] = count + 1

    def showExit(self, *args):
        count = self.spyValues.get(self.showExit, 0)
        self.spyValues[self.showExit] = count + 1

    def showWrongGuess(self, *args):
        count = self.spyValues.get(self.showWrongGuess, 0)
        self.spyValues[self.showWrongGuess] = count + 1

    def showGuessedWords(self, *args):
        count = self.spyValues.get(self.showGuessedWords, 0)
        self.spyValues[self.showGuessedWords] = count + 1

    def showProgress(self, *args):
        count = self.spyValues.get(self.showProgress, 0)
        self.spyValues[self.showProgress] = count + 1

    def getSaveFileName(self, *args):
        count = self.spyValues.get(self.getSaveFileName, 0)
        self.spyValues[self.getSaveFileName] = count + 1

    def getConfirmation(self, *args):
        count = self.spyValues.get(self.getConfirmation, 0)
        self.spyValues[self.getConfirmation] = count + 1

    def showMessage(self, *args):
        count = self.spyValues.get(self.showMessage, 0)
        self.spyValues[self.showMessage] = count + 1

    def showCorrectGuess(self, *args):
        count = self.spyValues.get(self.showCorrectGuess, 0)
        self.spyValues[self.showCorrectGuess] = count + 1
