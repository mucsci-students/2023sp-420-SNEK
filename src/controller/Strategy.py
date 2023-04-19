from abc import ABC, abstractmethod
import base64
from cryptography.fernet import Fernet
class Strategy(ABC):

    @abstractmethod
    def execute(self):
        pass

class plainSave(Strategy):

    def execute(self, puzzleLetters, wordList):

        # transform data from variables into json format to dump into file
        puzzleLettersStr = ''.join(puzzleLetters)
        requiredLetter = puzzleLetters[0]
        return [puzzleLettersStr, "WordList", wordList, requiredLetter]

class encryptSave(Strategy):

    def execute(self, puzzleLetters, wordList):

        # transform data from variables into json format to dump into file
        puzzleLettersStr = ''.join(puzzleLetters)
        requiredLetter = puzzleLetters[0]
        tempLis = ""
        encrypLis = ""
        key = "Team SNEK"

        for i in range(0, 32-len(key)):
            key += "$"

        key = key.encode("utf-8")
        encrypText = base64.b64encode(key)
        f = Fernet(encrypText)

        for i in wordList:
            tempLis += i + ","

        encrypLis = f.encrypt(bytes(tempLis, "utf-8")).decode("utf-8")

        return [puzzleLettersStr, "SecretWordList", encrypLis, requiredLetter]