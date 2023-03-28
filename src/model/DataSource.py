import numpy as np
import sqlite3
import pandas as pd
import random

from model.Hint import Hint


class DataSource:

      # this is going to be a dicctionary just contianing the words



    def __init__(self,dbName:str=None):
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

    def getHints(self, wordList:list,optionalLetters:list)->Hint:
        letterMat = dict()
        maximum = 0
        beginDict = dict()
        for word in wordList:
            if(maximum < len(word)):
                maximum = len(word)
            
        for letter in optionalLetters:
            letterMat[letter]= dict()
            for number in range(4, maximum+1):
                letterMat[letter][str(number)]= 0
            letterMat[letter]['Σ']= 0

        pangram = 0
        perfectPangram = 0


        print(wordList)

        for word in wordList:
            auxLetterList = list(set((word)))
            auxLetterList.sort()
            if auxLetterList == optionalLetters:
                pangram += 1
                if(len(word) == 7):
                    perfectPangram += 1
            if (letterMat.get(word[0]) == None):
                letterMat[word[0]][str(len(word))] = 1
            else:
                if (letterMat[word[0]].get(str(len(word))) == None):
                    letterMat[word[0]][str(len(word))] = 1
                else:
                    letterMat[word[0]][str(len(word))] += 1

            if (beginDict.get(word[:2]) == None):
                beginDict[word[:2]] = 1
            else:
                beginDict[word[:2]] += 1


        finalBingo = True
        for let in optionalLetters:
            sumatory = 0
            bingo = False
            for number in range(4, maximum+1):
                if(letterMat[let][str(number)] != 0):
                    bingo = True
                sumatory += letterMat[let][str(number)]
            if not bingo:
                finalBingo = False
            letterMat[let]['Σ'] = sumatory

        return Hint(letterMat, beginDict, pangram, perfectPangram , finalBingo, len(wordList))
    
