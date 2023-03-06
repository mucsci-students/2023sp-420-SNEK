# Unit tests for the GameController Module
import sys
sys.path.append('src/controller')
sys.path.append('src/model')
sys.path.append('src/view')



from GameController import GameController
import unittest
from Mocks.SpyUserInterface import SpyUserInterface
from Puzzle import Puzzle


class test_GameController(unittest.TestCase):


    def test_correctGuess(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        gameController.myPuzzle = testPuzzle

        gameController.processGuess("volcanos")

        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showCorrectGuess], 1, "The guess wasn't correctly checked.")
        
    def test_wrongGuessNotInWordList(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        gameController.myPuzzle = testPuzzle

        gameController.processGuess("volovlov")

        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showWrongGuess], 1, "The guess wasn't correctly checked.")
        
    def test_wrongGuessWithoutMandatoryLetter(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        gameController.myPuzzle = testPuzzle

        gameController.processGuess("three")

        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showWrongGuess], 1, "The guess wasn't correctly checked.")
        
    def test_wrongGuessAlreadyGuessedWord(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        gameController.myPuzzle = testPuzzle

        gameController.processGuess("volcanos")
        gameController.processGuess("volcanos")

        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showCorrectGuess], 1, "The guess wasn't correctly checked.")

        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showWrongGuess], 1, "The guess wasn't correctly checked.")

    def test_wrongGuessLessThanFourLettersWord(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        gameController.myPuzzle = testPuzzle

        gameController.processGuess("vov")

        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showWrongGuess], 1, "The guess wasn't correctly checked.")
        

    def test_processHelpCommand(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        
        gameController.processCommand("!help")
        
        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showHelp], 1, "The help command wasn't correctly checked.")
        
    def test_processExitCommand(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        
        gameController.playing = False
        gameController.processCommand("!exit")
        
        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.quitInterface], 1, "The help command wasn't correctly checked.")
        
    def test_processRankCommand(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        testPuzzle.currentRank = "Beginner"
        gameController.playing = True
        gameController.myPuzzle = testPuzzle
        gameController.processCommand("!rank")
        
        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showRanking], 1, "The help command wasn't correctly checked.")
        
    def test_processWrongCommand(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        testPuzzle.currentRank = "Beginner"
        gameController.playing = True
        gameController.myPuzzle = testPuzzle
        gameController.processCommand("!españita")
        
        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showError], 1, "The help command wasn't correctly checked.")
        
    def test_processGuessCommand(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        testPuzzle.currentRank = "Beginner"
        gameController.playing = True
        gameController.myPuzzle = testPuzzle
        gameController.processCommand("!guessed")
        
        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showGuessedWords], 1, "The help command wasn't correctly checked.")
        
    def test_processGuessCommandAtInput(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        testPuzzle.currentRank = "Beginner"
        gameController.playing = True
        gameController.myPuzzle = testPuzzle
        gameController.processInput("!guessed")
        
        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showGuessedWords], 1, "The help command wasn't correctly checked.")
        

    def test_errorGuessIfNotPlayingAtInput(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        word = "volcanos"
        puzzleLetters = list(set(word))
        wordList = ["onee", "twoo", "three", "four", "five",
                    "sixx", "seven", "eight", "nine", "volcanos"]
        testPuzzle = Puzzle(puzzleLetters, wordList)
        testPuzzle.currentRank = "Beginner"
        gameController.playing = False
        gameController.myPuzzle = testPuzzle
        gameController.processInput("cucaracha")
        
        self.assertEqual(
            spyUserInterface.spyValues[spyUserInterface.showError], 1, "The help command wasn't correctly checked.")



        

        
   