import numpy as np
import sqlite3
import pandas as pd

class DataSource:
    numberOfLetters = 0
    wordList = dict()##this is going to be a dicctionary just contianing the words
    def __init__(self, mandatoryLetter, optionalLetters):
        con = sqlite3.connect("example2.db")
        cur = con.cursor()

        cur.execute("SELECT word FROM word_list WHERE word like '%"+mandatoryLetter+"%'")
        output = cur.fetchall()
        print(len(output))
        #for row in output:
        #   print(row[0])
        con.commit()

        treatmentMat = np.array(output)
        letterSet = set(treatmentMat[:,0])
        
        treatmentMat = np.array(output)
        letterSet = set(treatmentMat[:,0])
        boolList = []
        for word in letterSet:
            approved = True
            for letter in word:
                if(letter not in optionalLetters):
                    approved = False
            boolList.append(approved)
        wordDF = pd.DataFrame(letterSet)
        wordDF = wordDF[boolList]

        # for letter in optionalLetters:
        #     cur.execute("SELECT word FROM word_list WHERE word like '%"+letter+"%'")
        #     output = cur.fetchall()
        #     con.commit()
        #     treatmentMat = np.array(output) 
        #     auxSet = set(treatmentMat[:,0])
        #     letterSet = letterSet.union(auxSet)
        con.close()
        self.wordList = letterSet
        numberLettersList = [len(set(list(word))) for word in self.wordList]
        self.numberOfLetters = sum(numberLettersList)
    

    def checkWord(searchedWord):
        con = sqlite3.connect("example2.db")
        cur = con.cursor()
        
        cur.execute("SELECT word FROM word_list WHERE word like '"+searchedWord+"'")
        output = cur.fetchall()
        con.commit()
        con.close()
        return len(output) > 0
    def grabWordsFor(word, mandatoryLetter):
        return DataSource( mandatoryLetter,list(word))
    