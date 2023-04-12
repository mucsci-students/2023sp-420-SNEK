from controller.Strategy import Strategy
from controller.Strategy import plainSave
from controller.Strategy import encryptSave
class Context:

    strategy: Strategy

    def setStrategy(self, strategy: Strategy) -> None:
        self.strategy = strategy

    def executeStrategy(self, puzzleLetters, wordList):
        return self.strategy.execute(puzzleLetters, wordList)