# Unit tests for the GameController Module

import sys
sys.path.append('./src')

import unittest


from controller.GameController import GameController
from model.Commands import Commands
from mocks.SpyUserInterface import SpyUserInterface
from model.Puzzle import Puzzle


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
            spyUserInterface.spyValues.get(spyUserInterface.showCorrectGuess, -1), 1, "The guess wasn't correctly checked.")
        
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
            spyUserInterface.spyValues.get(spyUserInterface.showWrongGuess, -1), 1, "The guess wasn't correctly checked.")
        
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
            spyUserInterface.spyValues.get(spyUserInterface.showWrongGuess, -1), 1, "The guess wasn't correctly checked.")
        
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
            spyUserInterface.spyValues.get(spyUserInterface.showCorrectGuess, -1), 1, "The correct guess wasn't correctly checked.")

        self.assertEqual(
            spyUserInterface.spyValues.get(spyUserInterface.showWrongGuess, -1), 1, "The wrong guess wasn't correctly checked.")

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
            spyUserInterface.spyValues.get(spyUserInterface.showWrongGuess, -1), 1, "The guess wasn't correctly checked.")
        

    def test_processHelpCommand(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        
        gameController.processCommand(Commands.HELP)
        
        self.assertEqual(
            spyUserInterface.spyValues.get(spyUserInterface.showHelp, -1), 1, "The help command wasn't correctly checked.")
        
    def test_processQuitCommand(self):
        spyUserInterface = SpyUserInterface()
        gameController = GameController(None)
        gameController.setUserInterface(spyUserInterface)
        
        gameController.playing = False
        gameController.processCommand(Commands.QUIT)
        
        self.assertEqual(
            spyUserInterface.spyValues.get(spyUserInterface.quitInterface, -1), 1, "The help command wasn't correctly checked.")
        
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
        gameController.processCommand(Commands.RANK)
        
        self.assertEqual(
            spyUserInterface.spyValues.get(spyUserInterface.showRanking, -1), 1, "The help command wasn't correctly checked.")
        
    def test_processUndefinedCommand(self):
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
        gameController.processCommand(Commands.UNDEFINED)
        
        self.assertEqual(
            spyUserInterface.spyValues.get(spyUserInterface.showError, -1), 1, "The help command wasn't correctly checked.")
                
    def test_processCmdLikeCommand(self):
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
        gameController.processCommand(Commands.CMD_LIKE)
        
        self.assertEqual(
            spyUserInterface.spyValues.get(spyUserInterface.showError, -1), 1, "The help command wasn't correctly checked.")
        
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
        gameController.processCommand(Commands.GUESSED_WORDS)
        
        self.assertEqual(
            spyUserInterface.spyValues.get(spyUserInterface.showGuessedWords, -1), 1, "The help command wasn't correctly checked.")
        
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
        gameController.processInput(Commands.GUESSED_WORDS)
        
        self.assertEqual(
            spyUserInterface.spyValues.get(spyUserInterface.showGuessedWords, -1), 1, "The help command wasn't correctly checked.")
        

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
            spyUserInterface.spyValues.get(spyUserInterface.showError, -1), 1, "The help command wasn't correctly checked.")



        

        
   