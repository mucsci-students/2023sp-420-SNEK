# GENERATE PUZZLE FROM BASE WORD
# Takes commands 'new (word)'
#   - Generates puzzle off of word
#   - Check that:
#     - Word has enough unique letters
#     - Word is not in the database of words
#     - Puzzle is already open?
#
#
# Puzzle Class
# Nick Hoopes
# Creates a Puzzle object that has the following characteristics:
#       foundWords        Already guessed words
#       status            Current score/status (beginner etc..)
#       points            Current points for players
#       wordListSize      All possible words for the puzzle
#       wordPuzzle        The pangram used to build puzzle split into array
#       wordsList         Related words to the puzzle
#
# Class can be used in two ways to create a word:
#       1. Word is given by the user
#       2. Word is pulled randomly from DB
#
#       The call for both will work the same, you simply pass a
#       word into the createPuzzle function:
#       EX:
#           Puzzle.createPuzzle(Puzzle, "zombify")
#           print(Puzzle.getWordPuzzle(Puzzle))
#           print(Puzzle.wordPuzzle)
#       returns:
#           ['o', 'm', 'b', 'i', 'z', 'y', 'f']
#           ['o', 'm', 'b', 'i', 'z', 'y', 'f']
#
#       You can also set or get any class variable by either reaching
#       directly into the class (Puzzle.word = "zombify")/(return Puzzle.word)
#       or by using the built in functions
#           (Puzzle.setWord(Puzzle, "zombify"))/(return Puzzle.getWord(Puzzle))
#
# Two exceptions may be raised when calling createPuzzle():
#       UniqueLetterException - If given word does not contain 7 unique letter
#       WordNotFoundException - If given word is not found in the dictionary
#

import random


class Puzzle:
    MIN_WRD_LEN = 4         # Minimum length of the guessed words
    __MIN_POINTS = 1        # Minimum points you can get from a guessed word
    __PANGRAM_BONUS = 7     # Bonus points for pangram
    # The list of names of the rankigs
    __RANK_NAMES_LIST = ["Beginner", "Good Start", "Moving Up", "Good",
                         "Solid", "Nice", "Great", "Amazing", "Genius"]

    def __init__(self, puzzleLetters: str, WordList: list[str]) -> None:
        # The word split into an array of characters
        self.puzzleLetters: list[str] = puzzleLetters
        # Words relative to the puzzle
        self.WordList: list[str] = WordList
        # Already guessed words
        self.guessedWords: list[str] = []
        # Current rank (beginner etc..)
        self.currentRank: str = self.__RANK_NAMES_LIST[0]
        # Current number of points for the puzzle
        self.currentPoints: int = 0
        # Total number of points of given game
        self.maxPoints: int = self.__calcMaxPoints(WordList)
        self.rankingsAndPoints: dict[str,
                                     int] = self.__rankDict(self.maxPoints)

    @classmethod
    def __calcMaxPoints(cls, WordList: list[str], puzzleLetters: list[str]) -> int:
        sum = 0
        for word in WordList:
            sum = sum + cls.__pointsOf(word, puzzleLetters)
        return sum

    @classmethod
    def __pointsOf(cls, word: str, puzzleLetters: list[str]) -> int:
        ''' Precondition:
                All words are correct and theire lenghts are more than __MIN_WRD_LEN
        '''
        if len(word) == cls.MIN_WRD_LEN:
            return cls.__MIN_POINTS
        elif set(word) == set(puzzleLetters):
            return len(word) + cls.__PANGRAM_BONUS
        else:
            return len(word)

    @classmethod
    def __rankDict(cls, maxPoints: int) -> dict[str, int]:
        n = len(cls.__RANK_NAMES_LIST)
        if maxPoints < (n - 1):
            return None

        rankingFunction: function = lambda x: (maxPoints/((n-1)**2)) * x**2

        pointList = [round(rankingFunction(i)) for i in range(n)]

        rankDict = dict(zip(cls.__RANK_NAMES_LIST, pointList))
        return rankDict

    def getMaxPoints(self) -> int:
        return self.maxPoints

    def getRanks(self) -> dict[str, int]:
        return self.rankingsAndPoints

    def getCurrentRank(self) -> str:
        return self.currentRank

    def __calcCurrentRank(self) -> str:
        i: int = 0
        newRank: str = self.__RANK_NAMES_LIST[i]
        while self.currentPoints > self.rankingsAndPoints[newRank]:
            newRank = self.__RANK_NAMES_LIST[i]
            i += 1

        return newRank

    def addFoundWord(self, word: str) -> None:
        self.guessedWords.append(word)
        self.currentPoints += self.__pointsOf(word)
        self.currentRank = self.__calcCurrentRank()

    def getGuessedWords(self) -> list[str]:
        '''Gets the list of words found by the user.'''
        return self.guessedWords

    # gets the points variable.
    # Usage: Puzzle.getPoints(Puzzle)
    # Returns int
    def getCurrentPoints(self) -> int:
        return self.currentPoints

    # gets the size variable.
    # Usage: Puzzle.getWordList(Puzzle)
    # Returns a list
    def getWordList(self) -> list[str]:
        return self.wordListSize

    # gets the wordPuzzle variable.
    # Usage: Puzzle.getWordPuzzle(Puzzle)
    # Returns array of chars
    def getPuzzleLetters(self) -> list[str]:
        return self.puzzleLetters

    def getState(self) -> None:
        raise ("State is not implemented, jet.")

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
        """
        shuffle function
        Bogdan Balagurak
        this function takes the list of letters of the Puzzle and
        shuffles the letters around if the user enters the shuffle command
        in the CLI.
        """
        restOfLetters = list(self.puzzleLetters[1:])
        random.shuffle(restOfLetters)
        letters = [self.puzzleLetters[0]] + restOfLetters
        self.puzzleLetters = letters
