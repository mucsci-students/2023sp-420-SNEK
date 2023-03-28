# gameController class to handle functionality of the Puzzle
# Stephen Clugston

import random
import os

from model.Puzzle import Puzzle
from model.Commands import *
from controller.customExcept import *
import view.UserInterface
from model.DataSource import DataSource
from controller.SaveAndLoad import SaveAndLoad
from model.Hint import Hint


class GameController:
    __EXIT_MSG = "Do you want to exit the game? (You'll be able to save it)"
    __SAVE_MSG = "Do you want to save the game?"
    __OVERRIDE_MSG = "Do you want to overwrite the game?"
    __STILL_LOAD_MSG = "Do you want to load another game?"
    __NO_GAME_TITLE = "Not Currently in game:"

    # Private function that is an error message template for actions that aren't allowed when a game is not being played.
    def __NO_GAME_DESC(self, description):
        return f"You can't {description} a game if you are not playing one."

    # Constructor that instantiates a new GameController object.
    def __init__(self, dataSource: DataSource) -> None:
        self.myPuzzle: Puzzle = None
        self.myUserInterface: view.UserInterface  = None
        self.playing: bool = False
        self.myDataSource: DataSource = dataSource

    # Sets the GameController myUserInterface attribute to the the passes UserInterface.
    def setUserInterface(self, myUserInterface):
        self.myUserInterface = myUserInterface

    # Function to process input from the user. 
    # Correctly handles the cases in which a command is called, for when a game is playing and not. 
    # If the input is not a command, the string is passed to processGuess and evaluated.
    def processInput(self, userInput) -> None:
        if Commands.isCommand(userInput):
            self.processCommand(userInput)
        elif not self.playing:
            self.myUserInterface.showError(
                "That is not a command, to show commands, type !help")
        else:
            self.processGuess(userInput)

    # A private function that asks whether the user wants to save when the program is in the process of exiting.
    def __askExitAndSave(self) -> bool:
        exitGame = self.myUserInterface.getConfirmation(self.__EXIT_MSG)
        if exitGame:
            self.playing = False
            save = self.myUserInterface.getConfirmation("Do you want to save?")
            if save:
                self.__saveFile()
                
            self.myUserInterface.showExit()
            
        return exitGame
            

    # A private function that handles the functionality of saving a file and all of its cases.
    # Uses the SaveAndLoad module to handle saving a game into the json format.
    def __saveFile(self) -> None:
        scratchMode = self.myUserInterface.getConfirmation(
            "How do you want to save?", okStr="scratch", nokStr="current")
        
        fileName = self.myUserInterface.getSaveFileName()
        
        if not os.path.basename(fileName) == ".json":
            if scratchMode:
                SaveAndLoad.saveScratch(self.myPuzzle, fileName)
            else:
                SaveAndLoad.saveCurrent(self.myPuzzle, fileName)

            self.myUserInterface.showMessage("The file has been saved: " + fileName)

    # Private function to create a new game from a newBaseWord 
    # Sets the puzzle attributes accordingly, sets the GameController to playing,
    # and tells the UI to display the puzzle
    def __createGame(self, newBaseWord):
        newPuzzleLetters = list(set(list(newBaseWord)))
        random.shuffle(newPuzzleLetters)
        self.myDataSource.grabWordsFor(newBaseWord, newPuzzleLetters[0])
        
        self.myPuzzle = Puzzle(
            newPuzzleLetters, self.myDataSource.wordList)
        self.myPuzzle.setHint(self.myDataSource.getHints(self.myPuzzle.wordList, self.myPuzzle.puzzleLetters))
        self.playing = True
        self.myUserInterface.showPuzzle(self.myPuzzle)

    # Function to process the command from a user. processCommand is called from processUserInput.
    # Handles all commands, such as exit, help, load, save, rank, guessed words, shuffle, new random, new word, and show status
    def processCommand(self, command: Commands) -> None:
        if command == Commands.QUIT:
            if self.playing:
                exit = self.__askExitAndSave()
                if exit:
                    self.myUserInterface.quitInterface()
            else:
                self.myUserInterface.quitInterface()

        elif command == Commands.EXIT:
            if self.playing:
                self.__askExitAndSave()
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("exit"))

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

            loadingFile = self.myUserInterface.getLoadFileName()
            if loadingFile == ".json":
                self.myUserInterface.showError("The file has to have a name.")
                return


            if SaveAndLoad.isSaved(loadingFile):
                self.myPuzzle = SaveAndLoad.load(loadingFile)
                self.playing = True
                self.myUserInterface.showMessage("The file has been loaded: " + loadingFile)
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
                self.__askExitAndSave()

            newBaseWord = self.myDataSource.getRandomWord()
            self.__createGame(newBaseWord)

        elif command == Commands.NEW_GAME_WRD:
            if self.playing:
                self.__askExitAndSave()

            newBaseWord = self.myUserInterface.getBaseWord()
            if(len(set(newBaseWord)) != 7):
                self.myUserInterface.showError("That word does not have 7 different letters.")
            elif(not self.myDataSource.checkWord(newBaseWord) ):
                self.myUserInterface.showError("That word is not in the DB.")
            else:                    
                self.__createGame(newBaseWord)

        elif command == Commands.SHOW_STATUS:
            if self.playing:
                self.myUserInterface.showStatus(
                    self.myPuzzle.getCurrentRank(), self.myPuzzle.getCurrentPoints())
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("show status of"))
        elif command == Commands.SHOW_HINTS:
            if self.playing:
                self.myUserInterface.showHints(
                    self.myPuzzle)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("show hints of"))
        else:
            self.myUserInterface.showError(
                "Not a valid command:", 'Type "!help" to show all possibilities')

    # Function to process the guess from the user. Called by processInput.
    # Correctly handles the situations in which the guess is correct, but also when the guess is simply incorrect 
    # (not a word, or not in the database), and more specifically when the guess isn't longer than 3 letters, 
    # if the guess doesn't have the required letter, and the word was already guessed.
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
           