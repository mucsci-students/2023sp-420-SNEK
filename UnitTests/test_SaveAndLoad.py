
import sys
sys.path.append('./src')

import os
import json


from model.Puzzle import Puzzle
from controller.SaveAndLoad import SaveAndLoad
import unittest


class test_SaveAndLoad(unittest.TestCase):
    testFileName = os.path.join(os.getcwd(),"testFileName.json")
    
    def test_saveScratch(self):
        puzzleLetters = ["a", "b", "c", "d"]
        wordList = ["bacalao"]
        puzzleTest = Puzzle(puzzleLetters, wordList)
        
        SaveAndLoad.saveScratch(puzzleTest, self.testFileName)
        with open(self.testFileName, "r") as loadFile:
            testSavedData = json.load(loadFile)
        self.assertEqual(
            testSavedData['WordList'], wordList, "word list not saved")
        self.assertEqual(
            testSavedData['PuzzleLetters'], ''.join(puzzleLetters), "puzzle letters not saved")
        self.assertEqual(testSavedData['GuessedWords'], [
        ], "guessed words not empty")
        self.assertEqual(
            testSavedData['RequiredLetter'], "a", "required letter not correctly saved")
        self.assertEqual(
            testSavedData['CurrentPoints'], 0, "current points not saved")
        self.assertEqual(
            testSavedData['MaxPoints'], puzzleTest.getMaxPoints(), "max points not saved")
        os.remove(self.testFileName)

    def test_saveCurrent(self):
        puzzleLetters = list("volcanos")
        wordList = ["bacalao", "bacalao", "bacalao", "bacalao",
                    "bacalao", "bacalao", "bacalao", "bacalao", "bacalao"]
        puzzleTest = Puzzle(puzzleLetters, wordList)

        wordsToBeGuessed = ["pata", "tomate", "sandia", "volcanos"]
        expectedCurrentPoints = 28
        for guess in wordsToBeGuessed:
            puzzleTest.addGuessWord(guess)

        
        SaveAndLoad.saveCurrent(puzzleTest, self.testFileName)
        with open(self.testFileName, "r") as loadFile:
            testSavedData = json.load(loadFile)

        self.assertEqual(
            testSavedData['WordList'], wordList, "word list not saved")
        self.assertEqual(
            testSavedData['PuzzleLetters'], ''.join(puzzleLetters), "puzzle letters not saved")
        self.assertEqual(
            testSavedData['GuessedWords'], wordsToBeGuessed, "guessed words not empty")
        self.assertEqual(
            testSavedData['RequiredLetter'], "v", "required letter not correctly saved")
        self.assertEqual(
            testSavedData['CurrentPoints'], expectedCurrentPoints, "current points not saved")
        self.assertEqual(
            testSavedData['MaxPoints'], puzzleTest.getMaxPoints(), "max points not saved")
        os.remove(self.testFileName)

    def test_isSaved(self):
        puzzleLetters = ["a", "b", "c", "d"]
        wordList = ["bacalao"]
        puzzleTest = Puzzle(puzzleLetters, wordList)
        
        SaveAndLoad.saveScratch(puzzleTest, self.testFileName)
        self.assertTrue(SaveAndLoad.isSaved(self.testFileName))
        os.remove(self.testFileName)

    def test_load(self):
        puzzleLetters = ["a", "b", "c", "d"]
        wordList = ["bacalao", "bacalao", "bacalao", "bacalao",
                    "bacalao", "bacalao", "bacalao", "bacalao", "bacalao"]
        puzzleTest = Puzzle(puzzleLetters, wordList)
        
        SaveAndLoad.saveScratch(puzzleTest, self.testFileName)
        puzzleActual: Puzzle = SaveAndLoad.load(self.testFileName)

        self.assertEqual(
            puzzleActual.getWordList(), wordList, "word list not saved")
        self.assertEqual(
            puzzleActual.getPuzzleLetters(), puzzleLetters, "puzzle letters not saved")
        self.assertEqual(puzzleActual.getGuessedWords(), [
        ], "guessed words not empty")
        self.assertEqual(
            puzzleActual.getPuzzleLetters()[0], "a", "required letter not correctly saved")
        self.assertEqual(
            puzzleActual.getCurrentPoints(), 0, "current points not saved")
        self.assertEqual(
            puzzleActual.getMaxPoints(), puzzleTest.getMaxPoints(), "max points not saved")
