import json
import os
from customExcept import SaveNotFound
from customExcept import MasterFileNotFound
from customExcept import WrongSaveType
from customExcept import OverwriteSave

# State class holding all save, load, and related methods


class State:

    def __init__(self, puzzle):
        self.myPuzzle = puzzle

    # Display all save names held in json master save file
    def allSaveNames(self):
        # list that is returned
        retNames = []
        # check if file exists, otherwise raise exception
        if os.path.exists("saveFile.json"):
            # while master file open, enumerate saves and appen every save name into list (retNames)
            with open("saveFile.json", "r") as f:
                save = json.load(f)
                for i, val in enumerate(save):
                    retNames.append(list(val.keys())[0])
        else:
            raise MasterFileNotFound
        # sort lsit alphanumerically
        retNames.sort()

        return retNames

    # isSaved checks the filename in the master save file to see if it is already an inuse save name

    def isSaved(self, saveName):
        # Check if master save file exists
        if os.path.exists("saveFile.json"):
            # open master save file and store contents in save
            with open("saveFile.json", "r") as f:
                save = json.load(f)
                # iterated through and check for saveName
                for i, val in enumerate(save):
                    if (list(val.keys())[0] == saveName):
                        # return the enumerated index of the saveName if present
                        return i
                # return -1 if saveName is unused
                return -1
        else:
            # if master save file does not exist throw exception
            raise MasterFileNotFound

    # Save shell that allows for calling save data in 4 different ways scratch, current, overwrite scratch, and overwrite current
    # This is what is called for the user interface in the form state.save(state, "saveName", "saveType")
    def save(self, saveName, typeSave):
        # type "current" = current, "scratch" = scratch, "OverS" = Overwrite Scratch, "OverC" = Overwrite Current
        if (typeSave.lower() == "scratch"):
            self.saveData(saveName, self.myPuzzle.wordPuzzle,
                          self.myPuzzle.wordsList)
        elif (typeSave.lower() == "overs"):
            self.saveData(saveName, self.myPuzzle.wordPuzzle,
                          self.myPuzzle.wordsList, typeSave = 1)
        elif (typeSave.lower() == "current"):
            self.saveData(saveName, self.myPuzzle.wordPuzzle, self.myPuzzle.wordsList,
                          self.myPuzzle.foundWords, self.myPuzzle.status, self.myPuzzle.points, self.myPuzzle.wordListSize, self.numberOfLetters, 0)
        elif (typeSave.lower() == "overc"):
            self.saveData(saveName, self.myPuzzle.wordPuzzle, self.myPuzzle.wordsList,
                          self.myPuzzle.foundWords, self.myPuzzle.status, self.myPuzzle.points, self.myPuzzle.wordListSize, self.myPuzzle.numberOfLetters, 1)
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

    def saveData(self, saveName, puzzle, wordList, foundWords=[], status="Beginner", points=0, wordListSize=None, numberOfLetters=0, typeSave=0):
        numberOfLetters = self.myPuzzle.numberOfLetters

        # checking if the wordListSize is None, meaning a scratch or overwrite scratch
        if (wordListSize == None):
            # set wordListSize to the full len of the wordList
            wordListSize = len(wordList)

        # transform data from variables into json format to dump into file
        data = self.saveParse(saveName, puzzle, wordList, foundWords,
                              status, points, wordListSize, numberOfLetters)

        # check if file exists
        if os.path.exists("saveFile.json"):
            # open file for reading
            with open("saveFile.json", "r") as f:
                # save contents of json into master save file
                save = json.load(f)
                # if saved return index of save, if not return -1 meaning that the save file is usable
                # if not overwrite, raise Exception
                print(saveName)
                i = self.isSaved(saveName)
                print(typeSave)
                if (typeSave != 0):
                    # if saved pop old save file of same name then add new data
                    if (i == -1):
                        raise SaveNotFound
                    save.pop(i)
                    save.append(data)
                elif (i == -1):
                    # if not saved, append new save file
                    save.append(data)
        # if master file does not exist create json list
        else:
            save = [data]
        # dump new save data into master file and create if none is present
        with open("saveFile.json", "w") as f:
            json.dump(save, f, indent=2)

        return

    # load the save data into the class variables into the puzzle class

    def load(self, saveName):

        retData = []
        # check if master file exists, if not raise exception
        if os.path.exists("saveFile.json"):
            with open("saveFile.json", "r") as f:
                save = json.load(f)
        else:
            raise MasterFileNotFound

        # translate data from json format to a list
        # in the form of [[wordPuzzle], [wordList], [foundWords], "status", points, wordListSize]
        if (self.isSaved(saveName) == -1):
            raise SaveNotFound

        data = self.saveParse(saveName, data=save)
        retData = list(data.values())

        # shove them straight into puzzle class
        self.myPuzzle.wordPuzzle = retData[0]
        self.myPuzzle.wordsList = retData[1]
        self.myPuzzle.foundWords = retData[2]
        self.myPuzzle.status = retData[3]
        self.myPuzzle.points = retData[4]
        self.myPuzzle.wordListSize = retData[5]
        self.myPuzzle.numberOfLetters = retData[6]

        return 0

    # Translate from variables into json format, parse from json format into variables

    def saveParse(self, saveName="tempName", puzzle=[], wordList=[], foundWords=[], status="Beginner", points=0, wordListSize=0, numberOfLetters=0, data=[]):
        numberOfLetters = self.myPuzzle.numberOfLetters

        retData = []
        # if data value not given translate to json format
        if (data == []):

            retData = {

                saveName:
                [
                    {
                        'wordPuzzle': puzzle,
                        'wordList': wordList,
                        'foundWords': foundWords,
                        'status': status,
                        'percent': points,
                        'wordListSize': wordListSize,
                        'totalWordLength': numberOfLetters
                    }
                ]
            }

        # if data has a json entry or loaded file, parse from json to dictionary
        elif (data != []):
            for i in data:
                if (list(i)[0] == saveName):
                    retData.append(list(i.values()))

            return retData[0][0][0]

        return retData
