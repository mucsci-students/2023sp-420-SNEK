# gameController class to handle functionailty of the Puzzle
# Stephen Clugston

import random
from Puzzle import Puzzle
from customExcept import *
import string


class GameController:

    # Class Attributes
    gameOver = False

    def __init__(self) -> None:
        self.puzzle = Puzzle()
        self.lableList = ["Beginner", "Good Start", "Moving Up", "Good",
                          "Solid", "Nice", "Great", "Amazing", "Genius"]

    def __rankDict(self, maxPoints):
        n = len(self.lableList)
        if maxPoints < (n - 1):
            return None

        rankingFunction: function = lambda x: (maxPoints/((n-1)**2)) * x**2

        pointList = [round(rankingFunction(i)) for i in range(n)]
        for i in range(1, n-1):
            if pointList[i] <= pointList[i-1]:
                pointList[i] += (pointList[i-1] - pointList[i] + 1)
                pointList[i+1] -= (pointList[i-1] - pointList[i] + 1)

        rankDict = dict(zip(self.lableList, pointList))
        return rankDict

    # Guess function to handle the functionailty of making a guess.
    # Stephen Clugston

    def guess(self, userGuess: str):
        if len(userGuess) >= 4:
            print(self.puzzle.wordPuzzle[0], list(userGuess))
            print(self.puzzle.wordPuzzle[0] in list(userGuess))

            if self.puzzle.wordPuzzle[0] in list(userGuess):
                rankDict = self.__rankDict(self.puzzle.numberOfLetters)

                # If this guess is a valid correct guess
                if not userGuess in self.puzzle.foundWords and userGuess in self.puzzle.wordsList:

                    # If this guess is the last possible guess, increment points, decrement wordListSize and set class variable gameOver to true
                    if self.puzzle.wordListSize == 1:
                        self.puzzle.points += len(userGuess)
                        level = self.lableList[0]
                        for i, rank in enumerate(self.lableList):
                            if self.puzzle.points == rankDict[rank]:
                                level = rank
                                break
                            elif self.puzzle.points < rankDict[rank]:
                                level = self.lableList[i-1]
                                break
                        self.puzzle.status = level
                        --self.puzzle.wordListSize
                        gameOver = True
                        return gameOver

                    # If the guessed word was already correctly guessed
                    if userGuess in self.puzzle.foundWords:
                        raise guessAlreadyMade

                    # If the guessed word is not in the array of possible solutions
                    if not userGuess in self.puzzle.wordsList:
                        # Output error saying the guess was incorrect
                        raise incorrectGuess

                    # If there are still possible guesses, increments points, and add the word to found words
                    self.puzzle.points += len(userGuess)
                    level = self.lableList[0]
                    for i, rank in enumerate(self.lableList):
                        if self.puzzle.points == rankDict[rank]:
                            level = rank
                            break
                        elif self.puzzle.points < rankDict[rank]:
                            level = self.lableList[i-1]
                            break
                        self.puzzle.status = level
                    --self.puzzle.wordListSize
                    self.puzzle.foundWords.append(userGuess)

                    return True
                return False

                # The guess did not contain the required letter
                raise noReqLetter

            # The guess was less than 4 letters
            raise lessThanFourLetters

    """
    shuffle function
    Bogdan Balagurak
    this function takes the list of letters of the Puzzle and
    shuffles the letters around if the user enters the shuffle command
    in the CLI.
    """
    # tests
    # letters = ['a','b','c','d','e','f','g']
    # userInput = input()

    # shuffles letters in list
    # using random.shuffle.
    # first slice list where all but 0 is rearranged
    # 0 is the center letter that is not
    # supposed to be rearranged.
    # after slice, use random shuffle on the
    # new list that was created and then return
    # element 0 form original list and join the
    # shuffled list to it.
    def shuffle(self):
        restOfLetters = list(self.puzzle.wordPuzzle[1:])
        random.shuffle(restOfLetters)
        letters = [self.puzzle.wordPuzzle[0]] + restOfLetters
        self.puzzle.setWordPuzzle(letters)

    def getPuzzle(self):
        return self.puzzle
