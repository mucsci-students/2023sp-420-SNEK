from abc import ABC, abstractmethod
import controller.GameController


class UserInterface(ABC):

    def __init__(self) -> None:
        self.myController = None
        self.quit = False

    def setController(self, myController):
        self.myController: controller.GameController.GameController = myController

    @abstractmethod
    def launch(self):
        pass

    @abstractmethod
    def quitInterface(self):
        pass

    @abstractmethod
    def getBaseWord(self):
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
    def showEnd(self):
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
    def getLoadFileName(self):
        pass

    @abstractmethod
    def getConfirmation(self):
        pass

    @abstractmethod
    def showMessage(self):
        pass

    @abstractmethod
    def showCorrectGuess(self):
        pass

    @abstractmethod
    def showHints(self):
        pass

    @abstractmethod
    def showExit(self):
        pass
