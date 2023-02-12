# Unit Test cases for Puzzle.py
# Nicholas Hoopes
#
# Will test the creation of a puzzle, assuring that
# all fields are correctly populated, and assures that
# getter and setter methods correctly return the right
# data.  Also assures that the correct exceptions
# are thrown for their respective cases.


from Puzzle import Puzzle
from customExcept import UniqueLetterException
from customExcept import WordNotFoundException
import unittest

class TestPuzzleCreation(unittest.TestCase):
    def test_createPuzzle(self):
        word = "zombify"
        pzzle = Puzzle()
        pzzle.createPuzzle(word)

        # Assure that word is set correctly
        self.assertEqual(pzzle.word, word)

        # Assure that wordPuzzle contains all letters of word
        self.assertTrue('z' in pzzle.wordPuzzle)
        self.assertTrue('o' in pzzle.wordPuzzle)
        self.assertTrue('m' in pzzle.wordPuzzle)
        self.assertTrue('b' in pzzle.wordPuzzle)
        self.assertTrue('i' in pzzle.wordPuzzle)
        self.assertTrue('f' in pzzle.wordPuzzle)
        self.assertTrue('y' in pzzle.wordPuzzle)

        # Assure wordPuzzle is correctly shuffled
        self.assertTrue(['z', 'o', 'm', 'b', 'i', 'f', 'y'] != pzzle.wordPuzzle)

        # Assure that wordList was populated
        self.assertFalse([] == pzzle.wordsList)
        self.assertFalse(0 == pzzle.wordListSize)

        # Assure that maximum score cannot be zero
        self.assertFalse(0 == pzzle.numberOfLetters)

        # Change the puzzle
        wordsList = pzzle.wordsList
        word2 = "volcanos"
        pzzle.createPuzzle(word2)

        # Assure that word2 is set correctly
        self.assertEqual(pzzle.word, word2)

        # Assure that wordPuzzle contains all letters of word2
        self.assertTrue('v' in pzzle.wordPuzzle)
        self.assertTrue('o' in pzzle.wordPuzzle)
        self.assertTrue('l' in pzzle.wordPuzzle)
        self.assertTrue('c' in pzzle.wordPuzzle)
        self.assertTrue('a' in pzzle.wordPuzzle)
        self.assertTrue('n' in pzzle.wordPuzzle)
        self.assertTrue('s' in pzzle.wordPuzzle)

        # Assure wordPuzzle is correctly shuffled
        self.assertTrue(['v', 'o', 'l', 'c', 'a', 'n', 's'] != pzzle.wordPuzzle)

        # Assure that wordList was populated
        self.assertFalse([] == pzzle.wordsList)
        self.assertFalse(0 == pzzle.wordListSize)

        # Assure that wordList was reset
        self.assertTrue(wordsList != pzzle.wordsList)

        # Assure that maximum score cannot be zero
        self.assertFalse(0 == pzzle.numberOfLetters)

    def test_createIncorrectPuzzleUnique(self):
        word = "zom"
        pzzle = Puzzle()

        # Assure puzzle will not be generated without 7 unique letters
        try:
            pzzle.createPuzzle(word)
        except UniqueLetterException:
            self.assertTrue(True)
            return

        self.assertFalse(True)

    def test_createIncorrectPuzzleDB(self):
        word = "abcdefg"
        pzzle = Puzzle()

        # Assure puzzle will not be generated if word doesn't exist in DB
        try:
            pzzle.createPuzzle(word)
        except WordNotFoundException:
            self.assertTrue(True)
            return

        self.assertFalse(True)

class TestSetterGetters(unittest.TestCase):
    # for testing all getter and setter methods
    def test_setterGetters(self):
        word = "zombify"
        wordPuzzle = set(word)
        foundWords = ['zombi', 'boyo']
        status = "Genius"
        points = 123456
        wordsList = ['zombi', 'boyo', 'momi', 'wordsss']
        wordListSize = len(wordsList)

        pzzle = Puzzle()

        pzzle.setFoundWords(foundWords)
        pzzle.setPoints(points)
        pzzle.setSize(wordListSize)
        pzzle.setStatus(status)
        pzzle.setWord(word)
        pzzle.setWordPuzzle(wordPuzzle)

        self.assertTrue(pzzle.getWord() == word)
        self.assertTrue(pzzle.getFoundWords() == foundWords)
        self.assertTrue(pzzle.getPoints() == points)
        self.assertTrue(pzzle.getSize() == wordListSize)
        self.assertTrue(pzzle.getStatus() == status)
        self.assertTrue(pzzle.getWordPuzzle() == wordPuzzle)

    def test_getState(self):
        pzzle = Puzzle()

        state = pzzle.getState()

        # Assure getState() returns something other than None
        self.assertTrue(state != None)

if __name__ == '__main__':
    unittest.main()