import sys
sys.path.append('../model')

import json
import os
from customExcept import SaveNotFound
from customExcept import MasterFileNotFound
from Puzzle import Puzzle
# from customExcept import OverwriteSave

# State class holding all save, load, and related methods


class SaveAndLoad:
    __SAVE_DIR = "saveFiles"

    # Display all save names held in json master save file
    @classmethod
    def allSaveNames(cls) -> list[str]:
        # list that is returned
        retNames = []
        # check if file exists, otherwise raise exception
        if os.path.exists(cls.__SAVE_DIR):
            tempList = os.listdir(cls.__SAVE_DIR)
            for i in tempList:
                retNames.append(os.path.splitext(i)[0])
        return retNames

    # isSaved checks the filename in the master save file to see if it is already an in use save name
    @classmethod
    def isSaved(cls, saveName: str) -> bool:
        if "/" in saveName:
            return os.path.exists(saveName)
        else:
            return os.path.exists(f"{os.getcwd()}/{saveName}.json")
        # Check if master save file exists
        

    # Save shell that allows for calling save data in 4 different ways scratch, current, overwrite scratch, and overwrite current
    # This is what is called for the user interface in the form state.save(state, "saveName", "saveType")
    @classmethod
    def saveCurrent(cls, puzzle: Puzzle, saveName: str):
        cls.saveData(saveName, puzzle.getPuzzleLetters(), puzzle.getWordList(),
                     puzzle.getGuessedWords(), puzzle.getCurrentPoints(), puzzle.getMaxPoints())
        # Save shell that allows for calling save data in 4 different ways scratch, current, overwrite scratch, and overwrite current
        # This is what is called for the user interface in the form state.save(state, "saveName", "saveType")

    @staticmethod
    def saveScratch(puzzle: Puzzle, saveName: str):
        SaveAndLoad.saveData(saveName, puzzle.getPuzzleLetters(),
                             puzzle.getWordList(), [], 0, puzzle.getMaxPoints())

    # Main saving function that is only called within the state class
    # Originally two functions, was able to be condensed with the use of default parameters
    # Using default parameters we can do all 4 save routines
    # empty parameters with only cls, savename, wordPuzzle, will default the rest and save from the baseline
    # ^ but with type 1 will overwrite the savefile with scratch
    # full parameters without a type will save current
    # ^ but with type 1 will overwrite the savefile with current
    @ classmethod
    def saveData(cls, saveName, puzzleLetters, wordList, foundWords=[], currentPoints=0, maxPoints=0):

        # checking if the wordListSize is None, meaning a scratch or overwrite scratch

        # transform data from variables into json format to dump into file
        puzzleLettersStr = ''.join(puzzleLetters)
        requiredLetter = puzzleLetters[0]
        data = cls.saveParse(puzzleLettersStr, wordList,
                             foundWords, currentPoints, requiredLetter, maxPoints)

        # dump new save data into master file and create if none is present
        if "/" in saveName:
            with open(saveName, "w") as f:
                json.dump(data, f, indent=2)
        else:
            with open(f"{os.getcwd()}/{saveName}.json", "w") as f:
                json.dump(data, f, indent=2)
        

    # load the save data into the class variables into the puzzle class
    @ classmethod
    def load(cls, saveName: str) -> Puzzle:

        if "/" in saveName:
            with open(saveName, "r") as loadFile:
                data = json.load(loadFile)
        else:
            with open(f"{os.getcwd()}/{saveName}.json", "r") as loadFile:
                data = json.load(loadFile)

        puzzleLettersStr: str = data["PuzzleLetters"]
        requiredLetter = data["RequiredLetter"]
        puzzleLetters = []
        puzzleLetters.append(requiredLetter)
        # erasing the required letter
        puzzleLettersStr = puzzleLettersStr.replace(requiredLetter, "")
        for i in puzzleLettersStr:
            puzzleLetters.append(i)

        myPuzzle = Puzzle(puzzleLetters, data["WordList"])

        # shove them straight into puzzle class
        myPuzzle.guessedWords = data["GuessedWords"]
        myPuzzle.currentPoints = data["CurrentPoints"]
        myPuzzle.currentRank = myPuzzle.calcCurrentRank()

        return myPuzzle

    # Translate from variables into json format
    @ staticmethod
    def saveParse(puzzleLetters="", wordList=[], guessedWords=[], currentPoints=0, requiredLetter="", maxPoints=0):
        # Translate to json format
        retData = {
            "GuessedWords": guessedWords,
            "WordList": wordList,
            "PuzzleLetters": puzzleLetters,
            "RequiredLetter": requiredLetter,
            "CurrentPoints": currentPoints,
            "MaxPoints": maxPoints
        }

        return retData
