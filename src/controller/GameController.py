# gameController class to handle functionailty of the Puzzle
# Stephen Clugston

import sys
sys.path.append('../model')


import random

from Puzzle import Puzzle
from Commands import *
from customExcept import *
import UserInterface
from DataSource import DataSource
from SaveAndLoad import SaveAndLoad


class GameController:
    __EXIT_MSG = "Do you want to exit the game? (You'll be able to save it)"
    __SAVE_MSG = "Do you want to save the game?"
    __OVERRIDE_MSG = "Do you want to overwrite the game?"
    __STILL_LOAD_MSG = "Do you want to load another game?"
    __NO_GAME_TITLE = "Not Currently in game:"

    def __NO_GAME_DESC(self, description):
        return f"You can't {description} a game if you are not playing one."

    def __init__(self, dataSource: DataSource) -> None:
        self.myPuzzle: Puzzle = None
        self.myUserInterface = None
        self.playing = False
        self.myDataSource: DataSource = dataSource

    def setUserInterface(self, myUserInterface: UserInterface.UserInterface):
        self.myUserInterface = myUserInterface

    def processInput(self, userInput: str) -> None:
        if Commands.isCommand(userInput):
            self.processCommand(userInput)
        elif not self.playing:
            self.myUserInterface.showError(
                "That is not a command, to show commands, type !help")
        else:
            self.processGuess(userInput)

    def __askExitAndSave(self) -> bool:
        exitGame = self.myUserInterface.getConfirmation(self.__EXIT_MSG)
        if exitGame:
            self.playing = False
            save = self.myUserInterface.getConfirmation("Do you want to save?")
            if save:
                self.__saveFile()
        return exitGame

    def __saveFile(self) -> None:
        overwrite = True
        scratchMode = self.myUserInterface.getConfirmation(
            "How do you want to save?", okStr="scratch", nokStr="current")
        fileName = self.myUserInterface.getSaveFileName(saveType="save")
        if SaveAndLoad.isSaved(fileName):
            self.myUserInterface.showMessage(
                "This file already exists")
            overwrite = self.myUserInterface.getConfirmation(
                "Do you want to overwrite it?")
        if overwrite:
            if scratchMode:
                SaveAndLoad.saveScratch(self.myPuzzle, fileName)
            else:
                SaveAndLoad.saveCurrent(self.myPuzzle, fileName)

    def __createGame(self, newBaseWord):
        newPuzzleLetters = list(set(list(newBaseWord)))
        random.shuffle(newPuzzleLetters)
        self.myPuzzle = Puzzle(
            newPuzzleLetters, self.myDataSource.grabWordsFor(newBaseWord, newPuzzleLetters[0]).wordList)
        self.playing = True
        self.myUserInterface.showPuzzle(self.myPuzzle)

    def processCommand(self, commandStr: str) -> None:
        command = Commands.getCommandFromName(commandStr)
        if command == Commands.EXIT:
            if self.playing:
                self.__askExitAndSave()
            else:
                self.myUserInterface.quitInterface()

        elif command == Commands.HELP:
            self.myUserInterface.showHelp()

        elif command == Commands.LOAD:
            if self.playing:
                exitGame = self.myUserInterface.getConfirmation(
                    self.__EXIT_MSG)
                if exitGame:
                    self.playing = False
                    save = self.myUserInterface.getConfirmation(
                        "Do you want to save the game?")
                    if save:
                        self.__saveFile()

            loadingFile = self.myUserInterface.getSaveFileName(saveType="load")
            if SaveAndLoad.isSaved(loadingFile):
                self.myPuzzle = SaveAndLoad.load(loadingFile)
                self.playing = True
                self.myUserInterface.showPuzzle(self.myPuzzle)
            else:
                self.myUserInterface.showError("That file does not exist.")

        elif command == Commands.SAVE:
            if self.playing:
                self.__saveFile()
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("save"))

        elif command == Commands.RANK:
            if self.playing:
                self.myUserInterface.showRanking(
                    self.myPuzzle.getRankingsAndPoints())
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("the rank of"))

        elif command == Commands.GUESSED_WORDS:
            if self.playing:
                self.myUserInterface.showGuessedWords(
                    self.myPuzzle.getGuessedWords())
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("show guessed words"))

        elif command == Commands.SHUFFLE:
            if self.playing:
                self.myPuzzle.shuffle()
                self.myUserInterface.showPuzzle(self.myPuzzle)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("shuffle letters of"))

        elif command == Commands.NEW_GAME_RND:
            if self.playing:
                exitGame = self.__askExitAndSave()
                if exitGame:
                    self.playing = False

            newBaseWord = self.myDataSource.getRandomWord()
            self.__createGame(newBaseWord)

        elif command == Commands.NEW_GAME_WRD:
            if self.playing:
                exitGame = self.__askExitAndSave()
                if (exitGame):
                    self.playing = False

            newBaseWord = self.myUserInterface.getBaseWord()
            if(len(set(newBaseWord)) != 7):
                self.myUserInterface.showError("That word does not have 7 different letters")
            elif(not self.myDataSource.checkWord(newBaseWord) ):
                self.myUserInterface.showError("That word is not in the DB")
            else:                    
                self.__createGame(newBaseWord)

        elif command == Commands.SHOW_STATUS:
            if self.playing:
                self.myUserInterface.showStatus(
                    self.myPuzzle.getCurrentRank(), self.myPuzzle.getCurrentPoints())
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("show status of"))
        else:
            self.myUserInterface.showError(
                "Not a valid command:", 'Type "!help" to show all possibilities')

    def processGuess(self, userGuess: str):
        if len(userGuess) < Puzzle.MIN_WRD_LEN:
            self.myUserInterface.showWrongGuess(
                f"The word doesn't have {Puzzle.MIN_WRD_LEN} letters.")
            return
        requiredLetter = self.myPuzzle.getPuzzleLetters()[0]
        if requiredLetter not in list(userGuess):
            self.myUserInterface.showWrongGuess(
                f"The word doesn't have the required letter ({requiredLetter.upper()}).")
            return

        if userGuess in self.myPuzzle.getGuessedWords():
            self.myUserInterface.showWrongGuess(
                f"The word has already been guessed.")
            return

        if userGuess not in self.myPuzzle.getWordList():
            self.myUserInterface.showWrongGuess(f"The word is not recognized.")
            return

        self.myPuzzle.addGuessWord(userGuess)
        currentPoints = self.myPuzzle.getCurrentPoints()
        maxPoints = self.myPuzzle.getMaxPoints()
        self.myUserInterface.showPuzzle(self.myPuzzle)
        self.myUserInterface.showCorrectGuess()
        if currentPoints == maxPoints:
            self.myUserInterface.showEnd()
            self.playing = False
