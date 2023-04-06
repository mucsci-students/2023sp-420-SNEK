import numpy as np
import sqlite3
import pandas as pd
import random

from model.Hint import Hint


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DataSource(metaclass=SingletonMeta):

    def __init__(self, dbName: str = None):
        self.dbName = dbName
        self.numberOfLetters = 0
        self.wordList = list()

    # checks if a word is in the db

    def checkWord(self, searchedWord):
        con = sqlite3.connect(self.dbName)
        cur = con.cursor()

        cur.execute(
            "SELECT word FROM word_list WHERE word like '"+searchedWord+"'")
        output = cur.fetchall()
        con.commit()
        con.close()
        return len(output) > 0

    def getRandomWord(self):
        con = sqlite3.connect(self.dbName)
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
        optionalLetters = list(set(word))
        if mandatoryLetter == None or optionalLetters == None:
            return
        con = sqlite3.connect(self.dbName)
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
        self.wordList = list(self.wordList[0])
        return self.wordList

    def getHighScores(self, requiredLetters:list):
        return 0;
    def getMinimumHighScore(self, requiredLetters:list):
        return 0;
    def setHighScore(self, requiredLetter:list,name:str,points:int):
        return;
        
    def getHints(self, inputWordList:list,inputOptionalLetters:list)->Hint:
        letterMat = dict()
        maximum = 0
        beginDict = dict()
        optionalLetters = inputOptionalLetters.copy()
        wordList = inputWordList.copy()
        for word in wordList:
            if (maximum < len(word)):
                maximum = len(word)
        optionalLetters.sort()
        wordList.sort()
        for letter in optionalLetters:
            letterMat[letter.upper()] = dict()
            for number in range(4, maximum+1):
                letterMat[letter.upper()][str(number)]= 0
            letterMat[letter.upper()]['Σ']= 0
        letterMat['Σ']= dict()
        
        for number in range(4, maximum+1):
            letterMat['Σ'][str(number)] = 0
        letterMat['Σ']['Σ'] = 0

        pangram = 0
        perfectPangram = 0

        for word in wordList:
            auxLetterList = list(set((word)))
            auxLetterList.sort()
            if auxLetterList == optionalLetters:
                pangram += 1
                if (len(word) == 7):
                    perfectPangram += 1
            if (letterMat.get(word[0].upper()) == None):
                letterMat[word[0].upper()][str(len(word))] = 1
            else:
                if (letterMat[word[0].upper()].get(str(len(word))) == None):
                    letterMat[word[0].upper()][str(len(word))] = 1
                else:
                    letterMat[word[0].upper()][str(len(word))] += 1

            if (beginDict.get(word[:2]) == None):
                beginDict[word[:2]] = 1
            else:
                beginDict[word[:2]] += 1

        finalBingo = True
        for let in optionalLetters:
            sumatory = 0
            bingo = False
            for number in range(4, maximum+1):
                if (letterMat[let.upper()][str(number)] != 0):
                    bingo = True
                sumatory += letterMat[let.upper()][str(number)]
            if not bingo:
                finalBingo = False
            letterMat[let.upper()]['Σ'] = sumatory
        for number in range(4, maximum+1):
            sumatory = 0
            for letter in optionalLetters:

                sumatory+=letterMat[letter.upper()][str(number)]
            letterMat['Σ'][str(number)] = sumatory
        sumatory = 0
        for letter in optionalLetters:
                sumatory+=letterMat[letter.upper()]['Σ']
        letterMat['Σ']['Σ'] = sumatory  

        return Hint(letterMat, beginDict, pangram, perfectPangram, finalBingo, len(wordList))