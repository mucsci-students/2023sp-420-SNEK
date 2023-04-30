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


class GameController:
    __EXIT_MSG = "WARNING:\n\tYou are implicitly exiting this game,\n\tbut you'll be able to save it later.\n\nDo you want to exit the game? "
    __EXPLICIT_EXIT_MSG = "Do you want to save before exiting?"
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
        self.myUserInterface: view.UserInterface.UserInterface = None
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

            
        if self.playing:
            self.myUserInterface.showPuzzle(self.myPuzzle)

    # A private function that asks whether the user wants to save when the program is in the process of exiting.
    def __askExitAndSave(self, explicit=False) -> bool:
        if not explicit:
            exitGame = self.myUserInterface.getConfirmation(self.__EXIT_MSG)

            if exitGame == self.myUserInterface.defaultYes:
                choice = self.__handleHighScores()
                if choice != self.myUserInterface.defaultYes:
                    save = self.myUserInterface.getConfirmation(
                        "Do you want to save?")
                    if save == self.myUserInterface.defaultYes:
                        canceled = self.__saveFile()
                        if canceled:
                            exitGame = self.myUserInterface.defaultCancel

                    elif save == self.myUserInterface.defaultCancel:
                        exitGame = self.myUserInterface.defaultCancel

        else:
            choice = self.__handleHighScores()
            if choice != self.myUserInterface.defaultYes:
                exitGame = self.myUserInterface.defaultYes
                save = self.myUserInterface.getConfirmation(
                    self.__EXPLICIT_EXIT_MSG)
                if save == self.myUserInterface.defaultYes:
                    canceled = self.__saveFile()
                    if canceled:
                        exitGame = self.myUserInterface.defaultCancel

                elif save == self.myUserInterface.defaultCancel:
                    exitGame = self.myUserInterface.defaultCancel
            else:
                exitGame = choice

        return exitGame == self.myUserInterface.defaultYes

    # A private function that handles the functionality of saving a file and all of its cases.
    # Uses the SaveAndLoad module to handle saving a game into the json format.

    def __saveFile(self) -> bool:
        saveMode = self.myUserInterface.getConfirmation(
            "How do you want to save?", okStr="scratch", nokStr="current", canStr="cancel")

        if saveMode != "cancel":
            fileName = self.myUserInterface.getSaveFileName()
            if fileName == "":
                return
            elif fileName == None:
                return True

            if not os.path.basename(fileName) == ".json":
                if saveMode == "scratch":
                    SaveAndLoad.saveScratch(self.myPuzzle, fileName)
                else:
                    SaveAndLoad.saveCurrent(self.myPuzzle, fileName)

                self.myUserInterface.showMessage(
                    "The file has been saved: " + fileName)

        return saveMode == "cancel"
    

    def __saveSecretFile(self) -> bool:
        saveMode = self.myUserInterface.getConfirmation(
            "How do you want to save?", okStr="scratch", nokStr="current", canStr="cancel")

        if saveMode != "cancel":
            fileName = self.myUserInterface.getSaveFileName()
            print(fileName)
            if fileName == "":
                return
            elif fileName == None:
                return True

            if not os.path.basename(fileName) == ".json":
                if saveMode == "scratch":
                    SaveAndLoad.saveScratch(self.myPuzzle, fileName, True)
                else:
                    SaveAndLoad.saveCurrent(self.myPuzzle, fileName, True)

                self.myUserInterface.showMessage(
                    "The file has been saved: " + fileName)

        return saveMode == "cancel"

    def __saveImg(self) -> bool:
        
        retLis = self.myUserInterface.saveScreenshot(self.myPuzzle)
        if retLis == None:
            return False

        imgFile = retLis[0]
        fileName = retLis[1]

        if fileName == "":
            return False
        elif fileName == None:
            return True
        
        if not os.path.basename(fileName) == ".png":

            SaveAndLoad.saveImg(imgFile, fileName)

            self.myUserInterface.showMessage(
                    "The file has been saved: " + fileName)


    # Private function to create a new game from a newBaseWord
    # Sets the puzzle attributes accordingly, sets the GameController to playing,
    # and tells the UI to display the puzzle
    def __createGame(self, newBaseWord):
        newPuzzleLetters = list(set(newBaseWord))
        random.shuffle(newPuzzleLetters)

        wordList = self.myDataSource.grabWordsFor(
            newBaseWord, newPuzzleLetters[0])

        self.myPuzzle = Puzzle(newPuzzleLetters, wordList)
        newHints = self.myDataSource.getHints(
            self.myPuzzle.wordList, self.myPuzzle.puzzleLetters)
        self.myPuzzle.setHint(newHints)
        self.myPuzzle.setHighScores(self.myDataSource.getHighScores(self.myPuzzle.getPuzzleLetters()))
        self.myPuzzle.setMinimumHighScore(self.myDataSource.getMinimumHighScore(self.myPuzzle.getPuzzleLetters()))

        self.playing = True
        # self.myUserInterface.showPuzzle(self.myPuzzle)

    def __handleHighScores(self) -> bool:
        if self.myPuzzle.getCurrentPoints() > self.myPuzzle.getMinimumHighScore(): 
            confirm = self.myUserInterface.getConfirmation("WARNING:\n\t You won't be able to save the puzzle if you save your score!\n\nSave your score?")
            if confirm == self.myUserInterface.defaultYes:
                self.myDataSource.setHighScore(self.myPuzzle.getPuzzleLetters(), self.myUserInterface.getScoreName(), self.myPuzzle.getCurrentPoints())
                self.myPuzzle.setHighScores(self.myDataSource.getHighScores(self.myPuzzle.getPuzzleLetters()))
                # self.myUserInterface.showMessage("Congrats! Your score is now entered into the top 10 leaderboard for this puzzle!\n")
                self.playing = False
                self.myUserInterface.showHighScores(self.myPuzzle, isEnd = True)
                
            return confirm
        else:
            # self.myUserInterface.showMessage("Sorry! Your score is NOT high enough to enter into the top 10 leaderboard for this puzzle :(\n")
            self.myUserInterface.showHighScores(self.myPuzzle, isEnd = True)
            return self.myUserInterface.defaultNo

    # Function to process the command from a user. processCommand is called from processUserInput.
    # Handles all commands, such as exit, help, load, save, rank, guessed words, shuffle, new random, new word, and show status
    def processCommand(self, command: Commands) -> None:

        if command == Commands.QUIT:
            if self.playing:                        
                exit = self.__askExitAndSave(explicit=True)
                if exit:
                    self.playing = False
                    self.myUserInterface.showExit()
                    self.myUserInterface.quitInterface()
            else:
                self.myUserInterface.quitInterface()

        elif command == Commands.EXIT:
            if self.playing:

                exit = self.__askExitAndSave(explicit=True)
                if exit:
                    self.playing = False
                    self.myUserInterface.showExit()
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("exit"))

        elif command == Commands.HELP:
            self.myUserInterface.showHelp()

        elif command == Commands.LOAD:
            if self.playing:
                exitGame = self.myUserInterface.getConfirmation(
                    self.__EXIT_MSG)
                if exitGame == self.myUserInterface.defaultYes:
                    save = self.myUserInterface.getConfirmation(
                        "Do you want to save the game?")
                    if save == self.myUserInterface.defaultYes:
                        canceled = self.__saveFile()
                        if canceled:
                            return
                        else:
                            self.playing = False

                elif exitGame == self.myUserInterface.defaultCancel:
                    return

            loadingFile = self.myUserInterface.getLoadFileName()
            if loadingFile == ".json":
                self.myUserInterface.showError("The file has to have a name.")
                return
            if loadingFile == "":
                return

            if SaveAndLoad.isSaved(loadingFile):
                try:
                    self.myPuzzle = SaveAndLoad.load(loadingFile)
                    newHints = self.myDataSource.getHints(self.myPuzzle.wordList, self.myPuzzle.puzzleLetters)
                    self.myPuzzle.setHint(newHints)
                    self.myPuzzle.setHighScores(self.myDataSource.getHighScores(self.myPuzzle.getPuzzleLetters()))
                    self.myPuzzle.setMinimumHighScore(self.myPuzzle.getCurrentPoints())
                    self.playing = True
                    self.myUserInterface.showMessage("The file has been loaded: " + loadingFile)
                except:
                    self.myUserInterface.showError("Load Failed", "Reverting operation...")
            else:
                self.myUserInterface.showError("That file does not exist.", "Reverting operation...")

        elif command == Commands.SAVE:
            if self.playing:
                canceled = self.__saveFile()
                if canceled:
                    return
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("save"))

        elif command == Commands.SAVE_SECRET:
            if self.playing:
                canceled = self.__saveSecretFile()
                if canceled:
                    return
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("save")
                )
        elif command == Commands.SAVE_IMG:
            if self.playing:
                canceled = self.__saveImg()
                if canceled:
                    return
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("save an image")
                )
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
                # self.myUserInterface.showPuzzle(self.myPuzzle)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("shuffle letters of"))

        elif command == Commands.NEW_GAME_RND:
            if self.playing:
                exit = self.__askExitAndSave(explicit=False)
                if exit:
                    newBaseWord = self.myDataSource.getRandomWord()
                    self.__createGame(newBaseWord)

            else:
                newBaseWord = self.myDataSource.getRandomWord()
                self.__createGame(newBaseWord)

        elif command == Commands.NEW_GAME_WRD:
            if self.playing:
                exit = self.__askExitAndSave(explicit=False)

                if exit:
                    newBaseWord = self.myUserInterface.getBaseWord().lower()
                    if (len(set(newBaseWord)) < 7):
                        self.myUserInterface.showError(
                            f"The word {newBaseWord.upper()} does not have 7 different letters.", "Reverting operation...")
                    elif (len(set(newBaseWord)) > 7):
                        self.myUserInterface.showError(
                            f"The word {newBaseWord.upper()} has more then 7 different letters.", "Reverting operation...")
                    elif (not self.myDataSource.checkWord(newBaseWord)):
                        self.myUserInterface.showError(
                            f"The word {newBaseWord.upper()} is not in the DB.", "Reverting operation...")
                    else:
                        self.__createGame(newBaseWord)
            else:
                newBaseWord = self.myUserInterface.getBaseWord()
                if (len(set(newBaseWord)) != 7):
                    self.myUserInterface.showError(
                        f"The word {newBaseWord.upper()} does not have 7 different letters.", "Reverting operation...")
                elif (not self.myDataSource.checkWord(newBaseWord)):
                    self.myUserInterface.showError(
                        f"The word {newBaseWord.upper()} is not in the DB.", "Reverting operation...")
                else:
                    self.__createGame(newBaseWord)

        elif command == Commands.SCORES:
            if self.playing:
                self.myUserInterface.showHighScores(self.myPuzzle)
            else:
                self.myUserInterface.showError(
                    self.__NO_GAME_TITLE, self.__NO_GAME_DESC("show the scores of a game of"))

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
        userLetters = list(userGuess)
        puzzleLetters = self.myPuzzle.getPuzzleLetters()
        for letter in userLetters:
            if letter not in puzzleLetters:
                self.myUserInterface.showWrongGuess(f"The letter {letter.upper()} is not valid.")
                return

        if len(userGuess) < Puzzle.MIN_WRD_LEN:
            self.myUserInterface.showWrongGuess(
                f"The word {userGuess.upper()} doesn't have {Puzzle.MIN_WRD_LEN} letters.")
            return
        
        requiredLetter = self.myPuzzle.getPuzzleLetters()[0]
        if requiredLetter not in list(userGuess):
            self.myUserInterface.showWrongGuess(
                f"The word {userGuess.upper()} doesn't have the required letter ({requiredLetter.upper()}).")
            return

        if userGuess in self.myPuzzle.getGuessedWords():
            self.myUserInterface.showWrongGuess(
                f"The word {userGuess.upper()} has already been guessed.")
            return

        if userGuess not in self.myPuzzle.getWordList():
            self.myUserInterface.showWrongGuess(f"The word {userGuess.upper()} is not recognized.")
            return

        self.myPuzzle.addGuessWord(userGuess)
        currentPoints = self.myPuzzle.getCurrentPoints()
        maxPoints = self.myPuzzle.getMaxPoints()
        # self.myUserInterface.showPuzzle(self.myPuzzle)
        self.myUserInterface.showCorrectGuess(userGuess.upper())
        if currentPoints == maxPoints:
            self.playing = False
            self.myUserInterface.showEnd()
            self.__handleHighScores()
            self.myUserInterface.showExit()
