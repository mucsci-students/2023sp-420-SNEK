# Unit Test cases for Puzzle.py
# Nicholas Hoopes
#
# Will test the creation of a puzzle, assuring that
# all fields are correctly populated, and assures that
# getter and setter methods correctly return the right
# data.  Also assures that the correct exceptions
# are thrown for their respective cases.

import sys

from model.DataSource import DataSource
sys.path.append('src/model')

import random
import sqlite3
import os
from model.Puzzle import Puzzle
import unittest


class test_Puzzle(unittest.TestCase):
    word = "volcanos"
    puzzleLetters = list(set(word))
    wordsList = ["cava", "volcano", "volcanos"]
    
    def setUp(self):
        if not os.path.exists("test1.db"):
            con = sqlite3.connect("test1.db")
            cur = con.cursor()
            cur.execute("CREATE TABLE word_list ( numLetter INT,letter VARCHAR(10) NOT NULL,differentLetters VARCHAR(45) NOT NULL, word VARCHAR(45) NOT NULL, PRIMARY KEY (word));")
            con.commit()
            cur.execute(
                "INSERT INTO word_list (letter,differentLetters , word,numLetter) VALUES ('w','waxrok', 'waxwork', '7');")
            con.commit()
            cur.execute(
                "INSERT INTO word_list (letter, word,differentLetters,numLetter) VALUES ('w','waxworks', 'waxorks', '8');")
            con.commit()
            con.close()

    
      
    def test_puzzleHIint(self):
        dataSource = DataSource("test1.db")
        myList = dataSource.grabWordsFor("waxworks", "x")
        tst_puzzle = Puzzle(list(set("waxworks")), myList)
        hint = dataSource.getHints(myList)
        tst_puzzle.setHint(hint)
        self.assertEquals(hint,tst_puzzle.getHint(),f"actual: {tst_puzzle.getHint()}, original: {hint}")

    def test_createPuzzle(self):
        tst_puzzle = Puzzle(self.puzzleLetters, self.wordsList)

        expected = self.puzzleLetters
        actual = tst_puzzle.getPuzzleLetters()
        self.assertEqual(actual, expected,
                         f"actual: {actual}\nexpected: {expected}")

        expected = self.wordsList
        actual = tst_puzzle.getWordList()
        self.assertEqual(actual, expected,
                         f"actual: {actual}\nexpected: {expected}")

        expected = 0
        actual = tst_puzzle.getCurrentPoints()
        self.assertEqual(actual, expected,
                         f"actual: {actual}\nexpected: {expected}")

        expected = []
        actual = tst_puzzle.getGuessedWords()
        self.assertEqual(actual, expected,
                         f"actual: {actual}\nexpected: {expected}")

        expected = "Beginner"
        actual = tst_puzzle.getCurrentRank()
        self.assertEqual(actual, expected,
                         f"actual: {actual}\nexpected: {expected}")

        expected = 23
        actual = tst_puzzle.getMaxPoints()
        self.assertEqual(actual, expected,
                         f"actual: {actual}\nexpected: {expected}")

    def test_shuffle(self):
        tst_puzzle = Puzzle(self.puzzleLetters, self.wordsList)

        random.seed(121420)     # Just a randomly chosen random seed
        tst_puzzle.shuffle()
        original = tst_puzzle.getPuzzleLetters()
        actual = tst_puzzle.getCurrentRank()
        self.assertFalse(actual == original,
                         f"actual: {actual}\noriginal: {original}")

    def test_addGuessWord(self):
        wordsList = ["onee", "twoo", "three", "four",
                     "five", "sixx", "seven", "eight", "nine", "volcanos"]
        tst_puzzle = Puzzle(self.puzzleLetters, wordsList)
        guessWord = "four"
        expectedPoints = 1
        expectedGuessedWords = [guessWord]

        tst_puzzle.addGuessWord(guessWord)

        actualPoints = tst_puzzle.getCurrentPoints()
        actualGuessedWords = tst_puzzle.getGuessedWords()

        self.assertEqual(actualPoints, expectedPoints,
                         f"actual: {actualPoints}\noriginal: {expectedPoints}")
        self.assertEqual(actualPoints, expectedPoints,
                         f"actual: {actualGuessedWords}\noriginal: {expectedGuessedWords}")

        _wordsList = wordsList.copy()
        _wordsList.remove(guessWord)
        for guess in _wordsList:
            tst_puzzle.addGuessWord(guess)

        actualPoints = tst_puzzle.getCurrentPoints()
        expectedPoints = tst_puzzle.getMaxPoints()
        self.assertEqual(actualPoints, expectedPoints,
                         f"actual: {actualGuessedWords}\noriginal: {expectedGuessedWords}")

        actualGuessedWords = tst_puzzle.getGuessedWords()
        expectedGuessedWords = tst_puzzle.getWordList()
        self.assertEqual(actualPoints, expectedPoints,
                         f"actual: {actualGuessedWords}\noriginal: {expectedGuessedWords}")
    


if __name__ == '__main__':
    unittest.main()
