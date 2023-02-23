# Unit tests for the GameController Modual
# Written by Stephen Clugston and Aitor Cantero Crespo with test_shuffle
# Bug fixed by Stephen Clugston and Aitor Cantero Crespo

import sys
import os
#sys.path.insert(0, os.path.abspath(".."))

from GameController import *
import unittest
import pytest

class test_GameController(unittest.TestCase):

    # Tests the creation of a GameController... tests of the Puzzle handled by the Puzzle unittests
    def test_GameControllerCreation(self):
        gameController = GameController()
        lableList = ["Beginner", "Good Start", "Moving Up", "Good",
                     "Solid", "Nice", "Great", "Amazing", "Genius"]

        self.assertEqual(gameController.lableList, lableList)

    # Tests the functionality of guess. Only case untested is a correct guess that is the last guess
    # WARNING:     Not working fully as intended. Functionality of puzzle is causing unexpected behavior after MANUALLY
    #              setting the puzzle fields, more specifically wordPuzzle. setWordPuzzle doesn't explixitly randomise the
    #              list, so expexcted behavior for puzzle.setWordPuzzle(list(set("volcanos"))) would be ['v', 'o', 'l', 'c', 'a', 'n', 'o']
    #              yet the list returned is randomized, not preserving the expected required letter as "V". Unknown at this time if this
    #              unexpected behavior is due to MANUALLY setting the puzzle fields, or if it is another underlying issue
    # PLEASE_NOTE: The guess function was manually tested to extent with all possible edge cases in mind and is currently working as
    #              intended in the current release build.
    def test_guess(self):
        # Creates the GameController
        gameController = GameController()

        # Puzzle Fields
        word = "volcanos"
        wordPuzzle = list('volcans')
        print(wordPuzzle)
        foundWords = ['volcanos']
        status = "Beginner"
        points = 5
        wordsList = ['volcano', 'This', 'is', 'a', 'Test']
        wordListSize = len(wordsList)
        numofLetters = 16

        # Set the puzzle obj
        puzzle = Puzzle()
        puzzle.setWord(word)
        puzzle.setWordPuzzle(wordPuzzle)
        puzzle.setFoundWords(foundWords)
        puzzle.setStatus(status)
        puzzle.setPoints(points)
        puzzle.setSize(wordListSize)
        puzzle.wordsList = wordsList
        puzzle.numberOfLetters = numofLetters

        # Sets gameController puzzle to the puzzle obj
        gameController.puzzle = puzzle

        # Correct Guess
        correctGuess = "volcano"

        # Too short of a guess
        short = "vol"

        # Missing required character
        noReq = "Hello"

        # Inccorect guess
        incor = "volvanos"

        # Tests the case of a correct guess
        self.assertTrue(gameController.guess(correctGuess))

        # Tests the case of a word being less than 4 characters
        self.assertFalse(gameController.guess(short))

        # Test the case in which the word does not contain the required letter
        self.assertFalse(gameController.guess(noReq))

        # Test the case in which the guessed word is not correct
        self.assertFalse(gameController.guess(incor))

        # Tests if the already correct guess will now be incorrect
        self.assertFalse(gameController.guess(correctGuess))

    # Tests whether shuffle works as intended. No more that 5 shuffles to the same base word is allowed
    def test_shuffle(self):
        # Creates the GameController
        gameController = GameController()

        # Sets the word puzzle
        gameController.puzzle.setWordPuzzle(list(set("volcanos")))

        # The invalid, unshuffled list
        unshuffle = list(set("volcanos"))

        # Count of invalid shuffles
        invalidCount = 0

        # Performs 100 shuffles, and counts the number of invalid shuffles
        for i in range(100):
            gameController.shuffle()
            if gameController.puzzle.getWordPuzzle == unshuffle:
                invalidCount += 1

        self.assertTrue(invalidCount < 5)


class TestGettersSetters(unittest.TestCase):

    # Tests whether the function setStatus correctly sets the status of the puzzle obj
    def test_setStatus(self):
        status = "Beginner"
        gameController = GameController()
        gameController.setStatus(status)

        self.assertTrue(gameController.puzzle.status == status)

    # Tests whether the function setGameOver correctly sets the gameOver field to true

    def test_setGameOver(self):
        gameController = GameController()
        gameController.setGameOver()

        self.assertFalse(gameController.setGameOver())

    # Tests whether the function getPuzzle returns the correct puzzle

    def test_getPuzzle(self):
        # Puzzle Fields
        word = "volcanos"
        wordPuzzle = set(word)
        foundWords = ['volcanos']
        status = "Beginner"
        points = 5
        wordsList = ['Hello', 'This', 'is', 'a', 'Test']
        wordListSize = len(wordsList)

        # Set the puzzle obj
        puzzle = Puzzle()
        puzzle.setWord(word)
        puzzle.setWordPuzzle(wordPuzzle)
        puzzle.setFoundWords(foundWords)
        puzzle.setStatus(status)
        puzzle.setPoints(points)
        puzzle.setSize(wordListSize)

        # Set the puzzle obj in gameController
        gameController = GameController()
        gameController.puzzle = puzzle

        self.assertEqual(gameController.getPuzzle(), puzzle)
