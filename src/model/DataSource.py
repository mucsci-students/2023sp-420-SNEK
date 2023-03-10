import numpy as np
import sqlite3
import pandas as pd
import random


class DataSource:
    numberOfLetters = 0
    wordList = dict()  # this is going to be a dicctionary just contianing the words

    def __init__(self, mandatoryLetter=None, optionalLetters=None):
        if mandatoryLetter == None or optionalLetters == None:
            return

        con = sqlite3.connect("spellingBee.db")
        cur = con.cursor()
        if len(mandatoryLetter) > 1:  # to avoid the user makes an injection
            return
        cur.execute(
            "SELECT word FROM word_list WHERE word like '%"+mandatoryLetter+"%'")
        output = cur.fetchall()
        con.commit()

        treatmentMat = np.array(output)
        wordSet = set(treatmentMat[:, 0])
        # just keep the words that contain only the desired letters
        treatmentMat = np.array(output)
        wordSet = set(treatmentMat[:, 0])
        boolList = []
        for word in wordSet:
            approved = True
            for letter in word:
                if (letter not in optionalLetters):
                    approved = False
            boolList.append(approved)
        wordDF = pd.DataFrame(wordSet)
        wordDF = wordDF[boolList]

        con.close()
        self.wordList = wordDF
        numberLettersList = [len(set(list(word)))
                             for word in list(self.wordList[0])]
        self.numberOfLetters = sum(numberLettersList)

    # checks if a word is in the db
    def checkWord(self, searchedWord):
        con = sqlite3.connect("spellingBee.db")
        cur = con.cursor()

        cur.execute(
            "SELECT word FROM word_list WHERE word like '"+searchedWord+"'")
        output = cur.fetchall()
        con.commit()
        con.close()
        return len(output) > 0

    def getRandomWord(self):
        con = sqlite3.connect("spellingBee.db")
        cur = con.cursor()

        cur.execute(
            "SELECT word,differentLetters FROM word_list WHERE numLetter = 7 or numLetter > 7")
        output = cur.fetchall()
        treatmentMat = np.array(output)
        wordDF = (treatmentMat[:, 1])
        depWordDF = pd.DataFrame(treatmentMat[:, 0])

        boolList = []
        for word in wordDF:
            approved = True
            if (len(word) < 7):
                approved = False
            boolList.append(approved)

        depWordDF = depWordDF[boolList]
        con.commit()
        numero = random.randint(0, len(depWordDF)-1)

        auxList = list(depWordDF.iloc[numero])

        con.close()
        return auxList[0]

    # returns a  dataSource object built with the word and the mandatory letter
    def grabWordsFor(self, word, mandatoryLetter):
        dt = DataSource(mandatoryLetter, list(word))
        self.numberOfLetters = dt.numberOfLetters
        self.wordList = list(dt.wordList[0])
        dt.wordList = list(dt.wordList[0])

        return dt
