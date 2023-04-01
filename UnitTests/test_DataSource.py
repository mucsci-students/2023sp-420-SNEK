


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



if __name__ == '__main__':
    unittest.main()

