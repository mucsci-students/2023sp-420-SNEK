


import sys
sys.path.append('./src')

import sqlite3
from model.DataSource import DataSource
from model.Hint import Hint
import os
import unittest


class test_DataSource(unittest.TestCase):
    word = "waxworks"
    puzzleLetters = list(set(word))

    def setUp(self):
        if not os.path.exists("test1.db"):
            con = sqlite3.connect("test1.db")
            cur = con.cursor()
            cur.execute("CREATE TABLE word_list ( numLetter INT,letter VARCHAR(10) NOT NULL,differentLetters VARCHAR(45) NOT NULL, word VARCHAR(45) NOT NULL, PRIMARY KEY (word));")
            con.commit()
            cur.execute(
                "INSERT INTO word_list (letter,differentLetters , word,numLetter) VALUES ('w','waxrok', 'waxwork', '7');")
            con.commit()
            cur.execute(
                "INSERT INTO word_list (letter, word,differentLetters,numLetter) VALUES ('w','waxworks', 'waxorks', '8');")
            con.commit()
            con.close()

    def test_createWordListFromWord(self):
        dataSource = DataSource("test1.db")
        myList = dataSource.grabWordsFor("waxworks", "x")
        self.assertTrue("waxwork" in dataSource.wordList,
                        f"the word waxwork is not in {dataSource.wordList}")
        self.assertTrue("waxworks" in dataSource.wordList,
                        f"the word waxworks is not in {dataSource.wordList}")

    def test_getRandomWord(self):
        dataSource = DataSource("test1.db")
        actualWord = dataSource.getRandomWord()
        expectedWord = "waxworks"
        self.assertEqual(actualWord, expectedWord,
                         f"the word is not the expected one, the one expected was {expectedWord} and the one recieved was {actualWord}")

    def test_getHints(self):
        dataSource = DataSource("test1.db")
        dataSource.grabWordsFor("waxworks", "x")
        actualHints:Hint = dataSource.getHints(
            dataSource.wordList, list(set("waxworks")))
        letterMat = dict()
        letters = list(set("waxworks"))
        maximum = 8
        for letter in letters:
            letterMat[letter] = dict()
            for number in range(4, maximum+1):
                letterMat[letter][str(number)] = 0
            letterMat[letter]['Σ'] = 0
        letterMat['Σ'] = dict()
        for number in range(4, maximum+1):
            letterMat['Σ'][str(number)] = 0
        
        letterMat['w']['8'] = 1
        letterMat['w']['7'] = 1
        letterMat['w']['Σ'] = 2
        letterMat['Σ']['8'] = 1
        letterMat['Σ']['7'] = 1
        letterMat['Σ']['Σ'] = 2
        beginning = dict()
        beginning['wa'] = 2
        self.assertEqual(actualHints.beginningList, beginning,
                         f"the list is not the expected one, the one expected was {beginning} and the one recieved was {actualHints.beginningList}")
        self.assertEqual(actualHints.letterMatrix, letterMat,
                         f"the list is not the expected one, the one expected was {letterMat} and the one recieved was {actualHints.letterMatrix}")
        

    def test_notInDataBase(self):
        dataSource = DataSource("test1.db")
        self.assertFalse(dataSource.checkWord("pamplona"),"this word shouldnt be in this db")
        self.assertTrue(dataSource.checkWord("waxworks"),"this word should be in the db")


if __name__ == '__main__':
    unittest.main()

