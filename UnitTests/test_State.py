
import os
import json
import pytest
import unittest
from State import State
from Puzzle import Puzzle



#some functions have random letters in front so that they go before other functions during
#execution of test
class test_State(unittest.TestCase):
    
    #test that allSaveNames actually returns accurate list
    def test_allSaveNames(self):
        test = c.allSaveNames()
        actual = os.listdir("saveFiles")
        retActual = []
        for i in actual:
            retActual.append(os.path.splitext(i)[0])
        self.assertTrue(test == retActual)

        return

    
    #test Save with different types (current, scratch, overcurrent, overscratch)
    def test_bSave(self):

        
        c.save("saveTest", "current")
        assert os.path.exists(f"saveFiles/saveTest.json"), "No file created: Current"

        data = {

                "saveTest":
                [
                    {
                        'wordPuzzle': b.wordPuzzle,
                        'wordList': b.wordsList,
                        'foundWords': b.foundWords,
                        'status': b.status,
                        'percent': b.points,
                        'wordListSize': b.wordListSize,
                        'totalWordLength': b.numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/saveTest.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match: Current"

        c.save("saveTest2", "scratch")
        saveName2 = "saveTest2"
        assert os.path.exists(f"saveFiles/{saveName2}.json"), "No file created: Scratch"

        data = {

                saveName2:
                [
                    {
                        'wordPuzzle': b.wordPuzzle,
                        'wordList': b.wordsList,
                        'foundWords': [],
                        'status': "Beginner",
                        'percent': 0,
                        'wordListSize': len(b.wordsList),
                        'totalWordLength': b.numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/saveTest2.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match: Scratch"
        

    
        c.save("saveTest", "overs")
        assert os.path.exists(f"saveFiles/saveTest.json"), "No file created: Overwrite Scratch"

        data = {

                "saveTest":
                [
                    {
                        'wordPuzzle': b.wordPuzzle,
                        'wordList': b.wordsList,
                        'foundWords': [],
                        'status': "Beginner",
                        'percent': 0,
                        'wordListSize': len(b.wordsList),
                        'totalWordLength': b.numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/saveTest.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match: Overwrite Scratch"
        
        c.save("saveTest2", "overc")
        assert os.path.exists(f"saveFiles/saveTest2.json"), "No file created: Overwrite Current"

        data = {

                saveName2:
                [
                    {
                        'wordPuzzle': b.wordPuzzle,
                        'wordList': b.wordsList,
                        'foundWords': b.foundWords,
                        'status': b.status,
                        'percent': b.points,
                        'wordListSize': b.wordListSize,
                        'totalWordLength': b.numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/{saveName2}.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match: Overwrite Current"
        
        return

    #test the raw save data function
    def test_cSaveData(self):
        
        c.saveData("saveTest3", b.wordPuzzle, b.wordsList, b.foundWords, b.status, b.points, wordListSize=None, numberOfLetters=0, typeSave=0)
        assert os.path.exists(f"saveFiles/saveTest3.json"), "No file created"
        data = {

                "saveTest3":
                [
                    {
                        'wordPuzzle': b.wordPuzzle,
                        'wordList': b.wordsList,
                        'foundWords': b.foundWords,
                        'status': b.status,
                        'percent': b.points,
                        'wordListSize': b.wordListSize,
                        'totalWordLength': b.numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/saveTest3.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match"
        
        return

    #test loading by asserting that the puzzle class matches with loaded values
    def test_dLoad(self):
        
        actualList = c.load("saveTest3")
        

        assert b.wordPuzzle == actualList[0], "wordPuzzle incorrect"
        assert b.wordsList == actualList[1], "wordsList incorrect"
        assert b.foundWords == actualList[2], "foundWords incorrect"
        assert b.status == actualList[3], "Status incorrect"
        assert b.points == actualList[4], "points incorrect"
        assert b.wordListSize == actualList[5], "wordListSize incorrect"
        assert b.numberOfLetters == actualList[6], "numberOfLetters incorrect"


        return


    #test the parser so that it is outputting correctly parsed json and variables
    def test_eSaveParse(self):
        
        retVal = c.saveParse("saveTest", b.wordPuzzle, b.wordsList, b.foundWords, b.status, b.points, b.wordListSize, b.numberOfLetters)

        data = {

                "saveTest":
                [
                    {
                        'wordPuzzle': b.wordPuzzle,
                        'wordList': b.wordsList,
                        'foundWords': b.foundWords,
                        'status': b.status,
                        'percent': b.points,
                        'wordListSize': b.wordListSize,
                        'totalWordLength': b.numberOfLetters
                    }
                ]
            }
        assert data == retVal, "saveParse not parsing to json correctly"
        
        retVal = c.saveParse("saveTest", data = [data])
    
        assert b.wordPuzzle == list(retVal.values())[0], "wordPuzzle incorrect"
        assert b.wordsList == list(retVal.values())[1], "wordsList incorrect"
        assert b.foundWords == list(retVal.values())[2], "foundWords incorrect"
        assert b.status == list(retVal.values())[3], "Status incorrect"
        assert b.points == list(retVal.values())[4], "points incorrect"
        assert b.wordListSize == list(retVal.values())[5], "wordListSize incorrect"
        assert b.numberOfLetters == list(retVal.values())[6], "numberOfLetters incorrect"

        

        return
    
    #test if the isSaved function returns the correct value
    def test_zIsSaved(self):
        
        testRes = c.isSaved("saveTest")
        self.assertTrue(os.path.exists(f"saveFiles/saveTest.json") == testRes)
        
        return

    #teardown class to remove test save files that are created during the tests
    @classmethod
    def tearDownClass(self):
        if os.path.exists("saveFiles/saveTest.json"):
            os.remove("saveFiles/saveTest.json")
        if os.path.exists("saveFiles/saveTest2.json"):
            os.remove("saveFiles/saveTest2.json")
        if os.path.exists("saveFiles/saveTest3.json"):
            os.remove("saveFiles/saveTest3.json")
        if os.path.exists("tests/pycache"):
            os.remove("tests/pycache")


#initialization of various classes
a = test_State()
b = Puzzle()
c = State(b)

#initiazliation of puzzle class
b.wordPuzzle = ["A", "B"]
b.wordsList = ["AB", "BA"]
b.foundWords = ["AB"]
b.numberOfLetters = 15
b.status = "Adept"
b.points = 34
b.wordListSize = len(b.wordsList)

    

if __name__ == '__main__':
    unittest.main(exit = False)



    