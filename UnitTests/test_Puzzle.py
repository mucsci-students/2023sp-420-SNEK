# Unit Test cases for Puzzle.py
# Nicholas Hoopes
#
# Will test the creation of a puzzle, assuring that
# all fields are correctly populated, and assures that
# getter and setter methods correctly return the right
# data.  Also assures that the correct exceptions
# are thrown for their respective cases.

import unittest
from model.Puzzle import Puzzle
import os
import sqlite3
import random
import sys


from model.DataSource import DataSource
sys.path.append('src/model')


class test_Puzzle(unittest.TestCase):
    word = "volcanos"
    puzzleLetters = list(set(word))
    wordsList = ["cava", "volcano", "volcanos"]

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

    


if __name__ == '__main__':
    unittest.main()
