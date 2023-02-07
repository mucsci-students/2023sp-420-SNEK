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
from customExcept import UniqueLetterException
from customExcept import WordNotFoundException

wordList = []
wordList = sorted(wordList)

class Puzzle:
    foundWords = []           # Already guessed words
    status = ""               # Current score/status (beginner etc..)
    points = 0                # Current number of points for the puzzle
    wordListSize = 0          # Number of possible words for the puzzle
    wordPuzzle = []           # The word split into an array of characters
    word = ""                 # The word itself
    wordsList = []            # Words relative to the puzzle

    def createPuzzle(self, word, dataSource):
        # wordList = dataSource.grabWords()
        # Check that word has enough unique letters
        if len(set(list(word))) != 7:
            raise UniqueLetterException
        
        # Word is not in the database of words
        if word not in wordList:  # Statement may need to change to include the ability to look into 
            raise WordNotFoundException
        
        # Split word into a puzzle (array of characters that make up word).
        self.wordPuzzle = []
        for i in word:
            self.wordPuzzle.append(i)
        
        random.shuffle(self.wordPuzzle)  # Shuffles the character array for the first time
        self.word = word                 # The word itself

        # self.wordsList = dataSource.grabWordsFor(word, self.wordPuzzle[0])   # List of possible words for the puzzle
        # self.wordListSize = len(self.wordsList)                     # Defining number of possible words for the puzzle

    # sets the foundWords variable.
    # Usage: Puzzle.setFoundWords(Puzzle, [])
    def setFoundWords(self, found):
        self.foundWords = found

    # gets the foundWords variable.
    # Usage: Puzzle.getFoundWords(Puzzle)
    # returns list
    def getFoundWords(self):
        return self.foundWords

    # sets the status variable.
    # Usage: Puzzle.setStatus(Puzzle, "")
    def setStatus(self, stat):
        self.status = stat
    
    # gets the status variable.
    # Usage: Puzzle.getStatus(Puzzle)
    # Returns string
    def getStatus(self):
        return self.status
    
    # sets the points variable.
    # Usage: Puzzle.setPoints(Puzzle, 0)
    def setPoints(self, pts):
        self.points = pts

    # gets the points variable.
    # Usage: Puzzle.getPoints(Puzzle)
    # Returns int
    def getPoints(self):
        return self.points
    
    # sets the size variable.
    # Usage: Puzzle.setSize(Puzzle, 0)
    def setSize(self, size):
        self.wordListSize = size

    # gets the size variable.
    # Usage: Puzzle.getSize(Puzzle)
    # Returns int
    def getSize(self):
        return self.wordListSize
    
    # sets the wordPuzzle variable.
    # Usage: Puzzle.setWordPuzzle(Puzzle, [])
    def setWordPuzzle(self, puzzle):
        self.wordPuzzle = puzzle

    # gets the wordPuzzle variable.
    # Usage: Puzzle.getWordPuzzle(Puzzle)
    # Returns array of chars
    def getWordPuzzle(self):
        return self.wordPuzzle
    
    # sets the word variable.
    # Usage: Puzzle.setWord(Puzzle, "")
    def setWord(self, wrd):
        self.word = wrd

    # gets the word variable.
    # Usage: Puzzle.getWord(Puzzle)
    # Returns string
    def getWord(self):
        return self.word