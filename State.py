import json
import os
from customExcept import SaveNotFound
from customExcept import MasterFileNotFound
from customExcept import WrongSaveType
#from customExcept import OverwriteSave

# State class holding all save, load, and related methods


class State:

    def __init__(self, puzzle):
        self.myPuzzle = puzzle

    # Display all save names held in json master save file
    def allSaveNames(self):
        # list that is returned
        retNames = []
        # check if file exists, otherwise raise exception
        if os.path.exists(f"saveFiles"):
            tempList = os.listdir(f"saveFiles")
            for i in tempList:
                retNames.append(os.path.splitext(i)[0])
        return retNames


    # isSaved checks the filename in the master save file to see if it is already an inuse save name

    def isSaved(self, saveName):
        # Check if master save file exists
        if os.path.exists(f"saveFiles/{saveName}.json"):
            return 1
        else:
            # if master save file does not exist throw exception
            return -1

    # Save shell that allows for calling save data in 4 different ways scratch, current, overwrite scratch, and overwrite current
    # This is what is called for the user interface in the form state.save(state, "saveName", "saveType")
    def save(self, saveName, typeSave):
        # type "current" = current, "scratch" = scratch, "OverS" = Overwrite Scratch, "OverC" = Overwrite Current
        if (typeSave.lower() == "scratch"):
            self.saveData(saveName, self.myPuzzle.wordPuzzle, self.myPuzzle.wordsList)
        elif (typeSave.lower() == "overs"):
            self.saveData(saveName, self.myPuzzle.wordPuzzle, self.myPuzzle.wordsList, typeSave = 1)
        elif (typeSave.lower() == "current"):
            self.saveData(saveName, self.myPuzzle.wordPuzzle, self.myPuzzle.wordsList, self.myPuzzle.foundWords, self.myPuzzle.points, self.myPuzzle.maxPoints,  0)
        elif (typeSave.lower() == "overc"):
            self.saveData(saveName, self.myPuzzle.wordPuzzle, self.myPuzzle.wordsList, self.myPuzzle.foundWords, self.myPuzzle.points, self.myPuzzle.maxPoints, 1)
        else:
            # if save type does not match any of the above, an exception will be raised
            raise WrongSaveType

    # Main saving function that is only called within the state class
    # Originally two functions, was able to be condensed with the use of default parameters
    # Using default parameters we can do all 4 save routines
    # empty parameters with only self, savename, wordPuzzle, will defualt the rest and save from the baseline
    # ^ but with type 1 will overwrite the savefile with scratch
    # full parameters without a type will save current
    # ^ but with type 1 will overwrite the savefile with current

    def saveData(self, saveName, puzzle, wordList, foundWords=[], points=0, maxPoints=0, typeSave=0):

        # checking if the wordListSize is None, meaning a scratch or overwrite scratch

        # transform data from variables into json format to dump into file
        data = self.saveParse(saveName, ''.join(str(x) for x in puzzle), wordList, foundWords, points, puzzle[0], maxPoints)
        sanityChecker = 0
        # check if file exists
        if os.path.exists(f"saveFiles/{saveName}.json"):
            # open file for reading
            with open(f"saveFiles/{saveName}.json", "r") as f:
                # save contents of json into master save file
                save = json.load(f)
                # if saved return index of save, if not return -1 meaning that the save file is usable
                # if not overwrite, raise Exception
                i = self.isSaved(saveName)
                if (typeSave != 0):
                    # if saved pop old save file of same name then add new data
                    if (i == -1):
                        raise SaveNotFound
                    #save.pop(0)
                    sanityChecker = 1
                elif (i == -1):
                    # if not saved, append new save file
                    save.append(data)
        # if master file does not exist create json list
        else:
            save = data
        # dump new save data into master file and create if none is present
        with open(f"saveFiles/{saveName}.json", "w") as f:
            if sanityChecker == 0:
                json.dump(save, f, indent=2)
            else:
                json.dump(data, f, indent = 2)

        return

    # load the save data into the class variables into the puzzle class

    def load(self, saveName):

        retData = []
        # check if master file exists, if not raise exception
        if os.path.exists(f"saveFiles/{saveName}.json"):
            with open(f"saveFiles/{saveName}.json", "r") as f:
                save = json.load(f)
        else:
            raise MasterFileNotFound

        # translate data from json format to a list
        # in the form of [[wordPuzzle], [wordList], [foundWords], "status", points, wordListSize]
        if (self.isSaved(saveName) == -1):
            raise SaveNotFound

        data = self.saveParse(saveName, data=save)
        puzzleArr = data[2]
        retPuzzleArr = []
        retPuzzleArr.append(data[3])
        for i in puzzleArr:
            if i == data[3]:
                pass
            else:
                retPuzzleArr.append(i)
                
        # shove them straight into puzzle class
        self.myPuzzle.wordPuzzle = retPuzzleArr
        self.myPuzzle.wordsList = data[1]
        self.myPuzzle.foundWords = data[0]
        self.myPuzzle.points = data[4]
        self.myPuzzle.wordListSize = len(self.myPuzzle.wordsList) - len(self.myPuzzle.foundWords)
        self.myPuzzle.maxPoints = data[5]

        return retData

    # Translate from variables into json format, parse from json format into variables

    def saveParse(self, saveName="tempName", puzzle="", wordList=[], foundWords=[], points=0, requiredLetter = "", maxPoints = 0, data=[]):

        retData = []
        # if data value not given translate to json format
        if (data == []):

            retData = {
                "GuessedWords": foundWords,
                "WordList": wordList,
                "PuzzleLetters": puzzle,
                "RequiredLetter": requiredLetter,
                "CurrentPoints": points,
                "MaxPoints": maxPoints
            }
            return retData

        # if data has a json entry or loaded file, parse from json to dictionary
        elif (data != []):
            retData = list(data.values())


        return retData

