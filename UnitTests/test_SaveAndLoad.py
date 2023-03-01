import sys
import os
import json


from Puzzle import Puzzle
from SaveAndLoad import SaveAndLoad
import unittest


class test_SaveAndLoad(unittest.TestCase):
    def test_saveScratch(self):
        puzzleLetters = ["a", "b", "c", "d"]
        wordList = ["bacalao"]
        puzzleTest = Puzzle(puzzleLetters, wordList)
        os.makedirs("saveFiles", exist_ok=True)
        SaveAndLoad.saveScratch(puzzleTest, "testFileName")
        with open("saveFiles/testFileName.json", "r") as loadFile:
            testSavedData = json.load(loadFile)

        self.assertEquals(
            testSavedData['WordList'], wordList, "word list not saved")
        self.assertEquals(
            testSavedData['PuzzleLetters'], ''.join(puzzleLetters), "puzzle letters not saved")
        self.assertEqual(testSavedData['GuessedWords'], [
        ], "guessed words not empty")
        self.assertEqual(
            testSavedData['RequiredLetter'], "a", "required letter not correctly saved")
        self.assertEqual(
            testSavedData['CurrentPoints'], 0, "current points not saved")
        self.assertEqual(
            testSavedData['MaxPoints'], puzzleTest.getMaxPoints(), "max points not saved")
        os.remove("saveFiles/testFileName.json")

    def test_saveCurrent(self):
        puzzleLetters = list("volcanos")
        wordList = ["bacalao", "bacalao", "bacalao", "bacalao",
                    "bacalao", "bacalao", "bacalao", "bacalao", "bacalao"]
        puzzleTest = Puzzle(puzzleLetters, wordList)

        wordsToBeGuessed = ["pata", "tomate", "sandia", "volcanos"]
        expectedCurrentPoints = 28
        for guess in wordsToBeGuessed:
            puzzleTest.addGuessWord(guess)

        os.makedirs("saveFiles", exist_ok=True)
        SaveAndLoad.saveCurrent(puzzleTest, "testFileName")
        with open("saveFiles/testFileName.json", "r") as loadFile:
            testSavedData = json.load(loadFile)

        self.assertEquals(
            testSavedData['WordList'], wordList, "word list not saved")
        self.assertEquals(
            testSavedData['PuzzleLetters'], ''.join(puzzleLetters), "puzzle letters not saved")
        self.assertEqual(
            testSavedData['GuessedWords'], wordsToBeGuessed, "guessed words not empty")
        self.assertEqual(
            testSavedData['RequiredLetter'], "v", "required letter not correctly saved")
        self.assertEqual(
            testSavedData['CurrentPoints'], expectedCurrentPoints, "current points not saved")
        self.assertEqual(
            testSavedData['MaxPoints'], puzzleTest.getMaxPoints(), "max points not saved")
        os.remove("saveFiles/testFileName.json")

    def test_isSaved(self):
        puzzleLetters = ["a", "b", "c", "d"]
        wordList = ["bacalao"]
        puzzleTest = Puzzle(puzzleLetters, wordList)
        os.makedirs("saveFiles", exist_ok=True)
        SaveAndLoad.saveScratch(puzzleTest, "testFileName")
        self.assertTrue(SaveAndLoad.isSaved("testFileName"))
        os.remove("saveFiles/testFileName.json")

    def test_load(self):
        puzzleLetters = ["a", "b", "c", "d"]
        wordList = ["bacalao", "bacalao", "bacalao", "bacalao",
                    "bacalao", "bacalao", "bacalao", "bacalao", "bacalao"]
        puzzleTest = Puzzle(puzzleLetters, wordList)
        os.makedirs("saveFiles", exist_ok=True)
        SaveAndLoad.saveScratch(puzzleTest, "testFileName")
        puzzleActual: Puzzle = SaveAndLoad.load("testFileName")

        self.assertEquals(
            puzzleActual.getWordList(), wordList, "word list not saved")
        self.assertEquals(
            puzzleActual.getPuzzleLetters(), puzzleLetters, "puzzle letters not saved")
        self.assertEqual(puzzleActual.getGuessedWords(), [
        ], "guessed words not empty")
        self.assertEqual(
            puzzleActual.getPuzzleLetters()[0], "a", "required letter not correctly saved")
        self.assertEqual(
            puzzleActual.getCurrentPoints(), 0, "current points not saved")
        self.assertEqual(
            puzzleActual.getMaxPoints(), puzzleTest.getMaxPoints(), "max points not saved")
