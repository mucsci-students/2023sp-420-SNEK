
import json
import os
from model.Puzzle import Puzzle
from PIL import Image, ImageDraw, ImageFont, ImageColor
from cryptography.fernet import Fernet
import base64
from controller.Context import Context
from controller.Strategy import plainSave, encryptSave
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
        return os.path.exists(saveName)
        

    # Save shell that allows for calling save data in 4 different ways scratch, current, overwrite scratch, and overwrite current
    # This is what is called for the user interface in the form state.save(state, "saveName", "saveType")
    @staticmethod
    def saveCurrent(puzzle: Puzzle, saveName: str, encrypt: bool = False):
        if encrypt:
            SaveAndLoad.saveData(saveName, puzzle.getPuzzleLetters(), puzzle.getWordList(),
                        puzzle.getGuessedWords(), puzzle.getCurrentPoints(), puzzle.getMaxPoints(), encrypt = True)
        else:
            SaveAndLoad.saveData(saveName, puzzle.getPuzzleLetters(), puzzle.getWordList(),
                        puzzle.getGuessedWords(), puzzle.getCurrentPoints(), puzzle.getMaxPoints(), encrypt = False)
        # Save shell that allows for calling save data in 4 different ways scratch, current, overwrite scratch, and overwrite current
        # This is what is called for the user interface in the form state.save(state, "saveName", "saveType")

    @staticmethod
    def saveScratch(puzzle: Puzzle, saveName: str, encrypt: bool = False):
        if encrypt:
            SaveAndLoad.saveData(saveName, puzzle.getPuzzleLetters(), 
                        puzzle.getWordList(), [], 0, puzzle.getMaxPoints(), encrypt = True)
        else:
            SaveAndLoad.saveData(saveName, puzzle.getPuzzleLetters(), 
                        puzzle.getWordList(), [], 0, puzzle.getMaxPoints(), encrypt = False)
        
    @classmethod
    def saveImg(cls, img: Image, imgName: str):
        if type(img) == str :
            fnt = font = ImageFont.load_default()

            image = Image.new(mode = "RGB", size = (200,160), color = "black")
            draw = ImageDraw.Draw(image)
            
            draw.text((10,10), img, font=fnt, fill=(255,255,0))

            image = image.resize((900, 700), resample=Image.NEAREST)
        image.save(imgName)
        
    @classmethod
    def __checkJsonExt(cls, fileName:str):
        fileName = fileName.strip()
        if not fileName.endswith(".json"):
            fileName += ".json"
            
        return fileName

    # Main saving function that is only called within the state class
    # Originally two functions, was able to be condensed with the use of default parameters
    # Using default parameters we can do all 4 save routines
    # empty parameters with only cls, savename, wordPuzzle, will default the rest and save from the baseline
    # ^ but with type 1 will overwrite the savefile with scratch
    # full parameters without a type will save current
    # ^ but with type 1 will overwrite the savefile with current
    @classmethod
    def saveData(cls, saveName:str, puzzleLetters, wordList, foundWords=[], currentPoints=0, maxPoints=0, author = "Team SNEK", encrypt = False):
        
        saveName = cls.__checkJsonExt(saveName)
        # checking if the wordListSize is None, meaning a scratch or overwrite scratch
        save = Context()
        if encrypt:
            save.setStrategy(encryptSave())
        else:
            save.setStrategy(plainSave())

        retList = save.executeStrategy(puzzleLetters, wordList)
        puzzleLettersStr = retList[0]
        listType = retList[1]
        wordList = retList[2]
        requiredLetter = retList[3]
        data = cls.saveParse(puzzleLettersStr, listType, wordList,
                             foundWords, currentPoints, requiredLetter, maxPoints, author, encrypt)

        # dump new save data into master file and create if none is present
        dirs = os.path.dirname(saveName)
        
        os.makedirs(dirs, exist_ok=True)
        
        with open(saveName, "w") as f:
            json.dump(data, f, indent=2)
        

    # load the save data into the class variables into the puzzle class
    @ classmethod
    def load(cls, loadName: str) -> Puzzle:
        loadName = cls.__checkJsonExt(loadName)
        
        with open(loadName, "r") as loadFile:
            data = json.load(loadFile)

        puzzleLettersStr: str = data["PuzzleLetters"]
        requiredLetter = data["RequiredLetter"]
        puzzleLetters = []
        puzzleLetters.append(requiredLetter)
        # putting the req letter in front
        puzzleLetters = [requiredLetter] + list(puzzleLettersStr.replace(requiredLetter, ""))
        

        if list(data)[2] == "SecretWordList":
            decrypLis = []
            key = data["Author"]

            for i in range(0, 32-len(key)):
                key += "$"

            key = key.encode("utf-8")
            key = base64.b64encode(key)
            f = Fernet(key)

            temp = data["SecretWordList"].encode("utf-8")
            decrypLis = f.decrypt(temp).decode("utf-8").split(",")
            decrypLis.remove("")
            
            myPuzzle = Puzzle(puzzleLetters, decrypLis, data["GuessedWords"], data["MaxPoints"], data["CurrentPoints"])
        else:
            myPuzzle = Puzzle(puzzleLetters, data["WordList"], data["GuessedWords"], data["MaxPoints"], data["CurrentPoints"])
            
        return myPuzzle

    # Translate from variables into json format
    @ staticmethod
    def saveParse(puzzleLetters="", wordListType="WordList", wordList=[], guessedWords=[], currentPoints=0, requiredLetter="", maxPoints=0, author = "Team SNEK", crypBool: bool = False):
        # Translate to json format
        retData = {
            "Author": author,
            "GuessedWords": guessedWords,
            wordListType: wordList,
            "PuzzleLetters": puzzleLetters,
            "RequiredLetter": requiredLetter,
            "CurrentPoints": currentPoints,
            "MaxPoints": maxPoints
        }
        return retData
    