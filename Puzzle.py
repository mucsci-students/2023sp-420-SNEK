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
#       word into the constructor of Puzzle:
#       EX:
#           word = "zombify"
#           P1 = Puzzle(word)
#           print(P1.wordPuzzle)
#           print(P1.word)
#       Returns:
#           ['f', 'i', 'z', 'o', 'm', 'b', 'y']
#           zombify
import random

# wordList = DataSource.grabWords()
wordList = []
wordList = sorted(wordList)

class Puzzle:
    foundWords = []           # Already guessed words
    status = ""               # Current score/status (beginner etc..)
    points = 0                # Current number of points for the puzzle
    wordListSize = 0          # Number of possible words for the puzzle

    def __init__(self, word):
        # Check that word has enough unique letters
        uniqueLetters = ""
        if len(set(list(word))) != 7:
            print(word + ' does not have exactly 7 unique letters!')
            return
        
        # Word is not in the database of words
        if word not in wordList:  # Statement may need to change to include the ability to look into 
            print(word + " is not in the dictionary!")  # the DB and make sure word is in there.
            return
        
        # Split word into a puzzle (array of characters that make up word).
        self.wordPuzzle = []
        for i in word:
            self.wordPuzzle.append(i)
        
        random.shuffle(self.wordPuzzle)  # Shuffles the character array for the first time
        self.word = word                 # The word itself

        # self.wordsList = DataSource.grabWordsFor(word, wordPuzzle[0])   # List of possible words for the puzzle
        # wordListSize = len(self.wordsList)                     # Defining number of possible words for the puzzle