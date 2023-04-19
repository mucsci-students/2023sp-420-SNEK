
import sys
sys.path.append('./src')

import sqlite3
from model.DataSource import DataSource
from model.Hint import Hint
import os
import unittest
import numpy as np


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
            cur.execute("CREATE TABLE high_scores (puzzleName VARCHAR(10) NOT NULL, PRIMARY KEY (puzzleName));")
            con.commit()
            con.close()
            
    def tearDown(self) -> None:
        os.remove("test1.db")
            

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
            letterMat[letter.upper()] = dict()
            for number in range(4, maximum+1):
                letterMat[letter.upper()][str(number)] = 0
            letterMat[letter.upper()]['Σ'] = 0
        letterMat['Σ'] = dict()
        for number in range(4, maximum+1):
            letterMat['Σ'][str(number)] = 0
        
        letterMat['W']['8'] = 1
        letterMat['W']['7'] = 1
        letterMat['W']['Σ'] = 2
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
        self.assertFalse(dataSource.checkWord("pamplona"),
                         "this word shouldnt be in this db")
        self.assertTrue(dataSource.checkWord("waxworks"),
                        "this word should be in the db")
        
    def test_notHighScoresReturnsMinimumHighScoreO(self):
        dataSource:DataSource = DataSource("test1.db")
        letters = list(set("waxworks"))
        self.assertEqual(dataSource.getMinimumHighScore(letters),0,"should be 0 as that puzzle has no highscores")
    
    def test_hasHighScoresIsFalseWhenNoHighScores(self):
        dataSource:DataSource = DataSource("test1.db")
        letters = list(set("waxworks"))
        self.assertFalse(dataSource.hasHighScores(letters),"should be false as that puzzle has no highscores")

    def test_hasHighScoresIsTrueWhenAnyScore(self):
        dataSource:DataSource = DataSource("test1.db")
        letters = list(set("waworks"))
        con = sqlite3.connect("test1.db")
        cur = con.cursor()
        self.assertFalse(dataSource.hasHighScores(letters),"should be false as that puzzle has no highscores")

        mandatoryLetter = "x"
        restOfLetters = letters
        restOfLetters.sort()
        puzzleName = ''.join(mandatoryLetter)+''.join(restOfLetters)
        cur.execute("CREATE TABLE "+puzzleName+" (playerName VARCHAR(50) NOT NULL, numLetter INT NOT NULL);")
        cur.execute(
                "INSERT INTO high_scores VALUES ('"+puzzleName+"');")
        con.commit()
        output = cur.fetchall()
        self.assertTrue(dataSource.hasHighScores(list(puzzleName)),"should be true as that puzzle has a highscore table")
        con.close()

        

    def test_notHighScoresReturnsEmptyDictionaryOfHighScores(self):
        dataSource:DataSource = DataSource("test1.db")
        letters = list(set("waxworks"))
        result = dataSource.getHighScores(letters)
        expected = dict()
        self.assertEqual(result,expected,"should be an empty dictionary")
        self.assertEqual(len(result),0,"should be an empty dictionary, with length 0")
    
    def test_setHighScoreCreatesTableWhenNoHighScores(self):
        dataSource:DataSource = DataSource("test1.db")
        letters = list("xawrkos")
        self.assertFalse(dataSource.hasHighScores(letters),"should be an empty list, this table should not exist")

        dataSource.setHighScore(letters,"example",1000)
        self.assertTrue(dataSource.hasHighScores(letters),"should be an empty dictionary")

        mandatoryLetter = letters[0]
        restOfLetters = letters[1:]
        restOfLetters.sort()
        puzzleName = ''.join(mandatoryLetter)+''.join(restOfLetters)
        con = sqlite3.connect("test1.db")
        cur = con.cursor()
        cur.execute("SELECT* FROM '"+puzzleName+"' ORDER BY points DESC, playerName DESC ")
        con.commit()
        con.close()

    def test_setHighScoreInsertsCorrectly(self):
        dataSource:DataSource = DataSource("test1.db")
        letters = list("xawrkos")
        dataSource.setHighScore(letters,"example",1000)
     

        mandatoryLetter = letters[0]
        restOfLetters = letters[1:]
        restOfLetters.sort()
        puzzleName = ''.join(mandatoryLetter)+''.join(restOfLetters)
        con = sqlite3.connect("test1.db")
        cur = con.cursor()
        cur.execute("SELECT* FROM '"+puzzleName+"' ORDER BY points DESC, playerName DESC ")
        output = cur.fetchall()
        con.commit()
        con.close()
        results = np.array(output)
        self.assertEqual('1000',results[0][1],f"the insertion is not correct expected 1000, actual: {results[0][1]} ")
        self.assertEqual('example',results[0][0],f"the insertion is not correct expected 'example', actual: {results[0][0]} ")

    def test_getMinimumHighScoreFromExistingHighScoreTable(self):
        dataSource:DataSource = DataSource("test1.db")
        letters = list("xawrkos")
        dataSource.setHighScore(letters,"example",1000)
        dataSource.setHighScore(letters,"example",1000)
        dataSource.setHighScore(letters,"example",1000)
        dataSource.setHighScore(letters,"example",1000)
        dataSource.setHighScore(letters,"example",1000)
        dataSource.setHighScore(letters,"example",1000)
        dataSource.setHighScore(letters,"example",1000)
        dataSource.setHighScore(letters,"example",1000)
        dataSource.setHighScore(letters,"example",1000)
        dataSource.setHighScore(letters,"example",999)     
        dataSource.setHighScore(letters,"example",998) 

        actual = dataSource.getMinimumHighScore(letters);
        self.assertEqual(999,actual,f"the insertion is not correct expected 999, actual: {actual} ")

    def test_getHighScoreFromExistingHighScoreTable(self):
        dataSource:DataSource = DataSource("test1.db")
        letters = list("xawrkos")
        dataSource.setHighScore(letters,"example",423)
        results = dataSource.getHighScores(letters)
        self.assertEqual('423',results[0][1],f"the insertion is not correct expected 423, actual: {results[0][1]} ")
        self.assertEqual('example',results[0][0],f"the insertion is not correct expected 'example', actual: {results[0][0]} ")
     
        



if __name__ == '__main__':
    unittest.main()
