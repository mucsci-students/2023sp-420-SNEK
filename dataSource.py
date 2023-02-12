import numpy as np
import sqlite3
import pandas as pd
import random



#Contains a list of the words that are going to be the possible guesses for the game
#Contains the total number of letters in the possible words, this will be used to calculate the points

class DataSource:
    numberOfLetters = 0
    wordList = dict()
    def __init__(self, mandatoryLetter, optionalLetters):
        
        con = sqlite3.connect("example3.db")
        cur = con.cursor()
        if len(mandatoryLetter) > 1:#to avoid the user makes an injection
            return
        cur.execute("SELECT word FROM word_list WHERE word like '%"+mandatoryLetter+"%'")
        output = cur.fetchall()
        print(len(output))
        con.commit()

        #just keep the words that contain only the desired letters
        treatmentMat = np.array(output)
        wordSet = set(treatmentMat[:,0])
        boolList = []
        for word in wordSet:
            approved = True
            for letter in word:#
                if(letter not in optionalLetters):
                    approved = False
            boolList.append(approved)
        wordDF = pd.DataFrame(wordSet)
        wordDF = wordDF[boolList] 

        con.close()
        self.wordList = wordDF
        numberLettersList = [len(set(list(word))) for word in self.wordList]
        self.numberOfLetters = sum(numberLettersList)
    
    ##checks if a word is in the db
    def checkWord(searchedWord):
        con = sqlite3.connect("example3.db")
        cur = con.cursor()
        
        cur.execute("SELECT word FROM word_list WHERE word like '"+searchedWord+"'")
        output = cur.fetchall()
        con.commit()
        con.close()
        return len(output) > 0
    
    #Returns a random word valid as a base word for the game
    def getRandomWord(self):
        con = sqlite3.connect("example3.db")
        cur = con.cursor()

        cur.execute(
            "SELECT word,differentLetters FROM word_list WHERE numLetter = 7")
        output = cur.fetchall()
        con.commit()
        numero = random.randint(0, len(output)-1)
        while (len(output[numero][1]) < 7):
            cur.execute(
                "SELECT word,differentLetters FROM word_list WHERE numLetter = 7")
            output = cur.fetchall()
        numero = random.randint(0, len(output)-1)
        con.close()
        return output[numero][0]

    ##returns a dataSource object built with the word and the mandatory letter
    def grabWordsFor(self,word: str, mandatoryLetter: chr) -> None:
        dt = DataSource( mandatoryLetter,list(word))
        self.numberOfLetters = dt.numberOfLetters
        self.wordList = dt.wordList
        
        

