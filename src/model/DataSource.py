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

    def checkWord(self, searchedWord)->bool:
        ''' Inputs:
                searchedWord: the word to check in the db.

            Output:
                if the word is in the db
        '''
        con = sqlite3.connect(self.dbName)
        cur = con.cursor()

        cur.execute(
            "SELECT word FROM word_list WHERE word like '"+searchedWord+"'")
        output = cur.fetchall()
        con.commit()
        con.close()
        return len(output) > 0

    def getRandomWord(self):
        ''' 
            Output:
                a random word from the db that can be used as the base word for the puzzle.
        '''
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
        ''' Inputs:
                word: the base word for the puzzle.
                mandatoryLetter: the required letter for the puzzle

            Output:
                the list of the words that are possible gusses for the puzzle.
        '''
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


    def hasHighScores(self, requiredLetters:list)->bool:
        ''' Inputs:
                requiredLetters: a list of the letters of the puzzle with the required letter at postion 0.

            Output:
                boolean value if that puzzle has registered scores
        '''
        con = sqlite3.connect(self.dbName)
        cur = con.cursor()
        mandatoryLetter = requiredLetters[0]
        restOfLetters = requiredLetters[1:]
        restOfLetters.sort()
        puzzleName = ''.join(mandatoryLetter)+''.join(restOfLetters)
        cur.execute(
            "SELECT* FROM high_scores WHERE puzzleName like '"+puzzleName+"'")
        output = cur.fetchall()
        con.commit()
        con.close()
        return len(output) != 0

    def getHighScores(self, requiredLetters:list):
        ''' Inputs:
                requiredLetters: a list of the letters of the puzzle with the required letter at postion 0.

            Output:
                a np.array with the top 10 scores.
        '''

        con = sqlite3.connect(self.dbName)
        cur = con.cursor()
        scores = dict()
        mandatoryLetter = requiredLetters[0]
        restOfLetters = requiredLetters[1:]
        restOfLetters.sort()
        puzzleName = ''.join(mandatoryLetter)+''.join(restOfLetters)
        if(self.hasHighScores(requiredLetters)):
            cur.execute("SELECT* FROM '"+puzzleName+"' ORDER BY points DESC, playerName DESC ")
            output = cur.fetchall()
            con.commit()
            dataTreatment = np.array(output)
            if(len(dataTreatment) >= 10):
                length = 10
            else:
                length = len(dataTreatment)
           
            scores = dataTreatment[:length]
        con.close()
        return scores;

    def getMinimumHighScore(self, requiredLetters:list):
        ''' Inputs:
                requiredLetters: a list of the letters of the puzzle with the required letter at postion 0.

            Output:
                the minimum score in the top 10 scores, if there are less than, 10 will be 0
        '''
        scores = self.getHighScores(requiredLetters);
        min = 0;
        if(len(scores) == 10):
            min = int(scores[9][1])
        return min


    def setHighScore(self, requiredLetters:list,name:str,points:int):
        ''' Inputs:
                requiredLetters: a list of the letters of the puzzle with the required letter at postion 0.
                name: the name of the player
                points: the points of the player

            Output:
                boolean value if that puzzle has registered scores
        '''
        mandatoryLetter = requiredLetters[0]
        restOfLetters = requiredLetters[1:]
        restOfLetters.sort()
        puzzleName = ''.join(mandatoryLetter)+''.join(restOfLetters)
        con = sqlite3.connect(self.dbName)
        cur = con.cursor()
        if(not self.hasHighScores(requiredLetters)):
            
            cur.execute("CREATE TABLE "+puzzleName+" (playerName VARCHAR(50) NOT NULL, points INT NOT NULL);")
            cur.execute(
                    "INSERT INTO high_scores VALUES ('"+puzzleName+"');")
            con.commit()
        cur.execute("INSERT INTO "+puzzleName+" VALUES ('"+name+"','"+str(points)+"');")
        con.commit()
        con.close()
        
        
    def getHints(self, inputWordList:list,inputOptionalLetters:list)->Hint:
         
        ''' Inputs:
                inputWordList: a list of the words of the puzzle.
                inputOptionalLetters: a list of the letters of the puzzle with the required letter at postion 0.

            Output:
                hint object with all the data for the hints
        '''
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