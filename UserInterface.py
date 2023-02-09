from abc import ABC, abstractmethod


class UserInterface(ABC):

    @abstractmethod
    def getUserInput(self):
        pass

    @abstractmethod
    def getBaseWord(self):
        pass

    @abstractmethod
    def getCommand(self):
        pass

    @abstractmethod
    def showStatus(self):
        pass

    @abstractmethod
    def showRanking(self):
        pass

    @abstractmethod
    def showPuzzle(self):
        pass

    @abstractmethod
    def showError(self):
        pass

    @abstractmethod
    def showHelp(self):
        pass

    @abstractmethod
    def showFoundWords(self):
        pass

    @abstractmethod
    def showEnd(self):
        pass

    @abstractmethod
    def showExit(self):
        pass

    @abstractmethod
    def showWrongGuess(self):
        pass

    @abstractmethod
    def showGuessedWords(self):
        pass

    @abstractmethod
    def showProgress(self):
        pass

    @abstractmethod
    def getSaveFileName(self):
        pass

    @abstractmethod
    def getConfirmation(self):
        pass

    @abstractmethod
    def showMessage(self):
        pass
