from State import State
from Puzzle import Puzzle
import os
import json
class stateTest:

    def _init_(self):
        pass
    
    def allSaveNamesTest(self, state):

        test = state.allSaveNames()
        actual = os.listdir("saveFiles")
        retActual = []
        for i in actual:
            retActual.append(os.path.splitext(i)[0])

        assert test == retActual, "Different save name lists"

        return

    def isSavedTest(self, state, saveName):

        testRes = state.isSaved(saveName)
        assert os.path.exists(f"saveFiles/{saveName}.json") == testRes, "Save name was not found"
        
        return

    def saveTest(self, state, saveName, puzzle, wordList, foundWords=[], status="Beginner", points = 0, wordListSize=None, numberOfLetters=0):

        state.save(saveName, "current")
        assert os.path.exists(f"saveFiles/{saveName}.json"), "No file created: Current"

        data = {

                saveName:
                [
                    {
                        'wordPuzzle': puzzle,
                        'wordList': wordList,
                        'foundWords': foundWords,
                        'status': status,
                        'percent': points,
                        'wordListSize': wordListSize,
                        'totalWordLength': numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/{saveName}.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match: Current"

        state.save(saveName + "2", "scratch")
        saveName2 = saveName + "2"
        assert os.path.exists(f"saveFiles/{saveName2}.json"), "No file created: Scratch"

        data = {

                saveName2:
                [
                    {
                        'wordPuzzle': puzzle,
                        'wordList': wordList,
                        'foundWords': [],
                        'status': "Beginner",
                        'percent': 0,
                        'wordListSize': len(wordList),
                        'totalWordLength': numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/{saveName2}.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match: Scratch"
        

    
        state.save(saveName, "overs")
        assert os.path.exists(f"saveFiles/{saveName}.json"), "No file created: Overwrite Scratch"

        data = {

                saveName:
                [
                    {
                        'wordPuzzle': puzzle,
                        'wordList': wordList,
                        'foundWords': [],
                        'status': "Beginner",
                        'percent': 0,
                        'wordListSize': len(wordList),
                        'totalWordLength': numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/{saveName}.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match: Overwrite Scratch"
        
        state.save(saveName + "2", "overc")
        assert os.path.exists(f"saveFiles/{saveName2}.json"), "No file created: Overwrite Current"

        data = {

                saveName2:
                [
                    {
                        'wordPuzzle': puzzle,
                        'wordList': wordList,
                        'foundWords': foundWords,
                        'status': status,
                        'percent': points,
                        'wordListSize': wordListSize,
                        'totalWordLength': numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/{saveName2}.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match: Overwrite Current"
        
        return

    def saveDataTest(self, state, saveName, puzzle, wordList, foundWords=[], status="Beginner", points = 0, wordListSize=None, numberOfLetters=0, typeSave=0):

        state.saveData(saveName, puzzle, wordList, foundWords, status, points, wordListSize=None, numberOfLetters=0, typeSave=0)
        assert os.path.exists(f"saveFiles/{saveName}.json"), "No file created"
        data = {

                saveName:
                [
                    {
                        'wordPuzzle': puzzle,
                        'wordList': wordList,
                        'foundWords': foundWords,
                        'status': status,
                        'percent': points,
                        'wordListSize': wordListSize,
                        'totalWordLength': numberOfLetters
                    }
                ]
            }
        with open(f"saveFiles/{saveName}.json", "r") as f:
                save = json.load(f)
        assert save == [data], "Save files do not match"
        
        return

    def loadTest(self, state, saveName, puzzle):

        actualList = state.load("saveTest3")
        

        assert puzzle.wordPuzzle == actualList[0], "wordPuzzle incorrect"
        assert puzzle.wordsList == actualList[1], "wordsList incorrect"
        assert puzzle.foundWords == actualList[2], "foundWords incorrect"
        assert puzzle.status == actualList[3], "Status incorrect"
        assert puzzle.points == actualList[4], "points incorrect"
        assert puzzle.wordListSize == actualList[5], "wordListSize incorrect"
        assert puzzle.numberOfLetters == actualList[6], "numberOfLetters incorrect"


        return

    def saveParseTest(self, state, puzzleCls, saveName="tempName", puzzle=[], wordList=[], foundWords=[], status="Beginner", points=0, wordListSize=0, numberOfLetters=0, data=[]):
    
        retVal = state.saveParse(saveName, puzzle, wordList, foundWords, status, points, wordListSize, numberOfLetters)

        data = {

                saveName:
                [
                    {
                        'wordPuzzle': puzzle,
                        'wordList': wordList,
                        'foundWords': foundWords,
                        'status': status,
                        'percent': points,
                        'wordListSize': wordListSize,
                        'totalWordLength': numberOfLetters
                    }
                ]
            }
        assert data == retVal, "saveParse not parsing to json correctly"
        
        retVal = state.saveParse(saveName, data = [data])
    
        assert puzzleCls.wordPuzzle == list(retVal.values())[0], "wordPuzzle incorrect"
        assert puzzleCls.wordsList == list(retVal.values())[1], "wordsList incorrect"
        assert puzzleCls.foundWords == list(retVal.values())[2], "foundWords incorrect"
        assert puzzleCls.status == list(retVal.values())[3], "Status incorrect"
        assert puzzleCls.points == list(retVal.values())[4], "points incorrect"
        assert puzzleCls.wordListSize == list(retVal.values())[5], "wordListSize incorrect"
        assert puzzleCls.numberOfLetters == list(retVal.values())[6], "numberOfLetters incorrect"

        

        return


a = stateTest()
b = Puzzle()
c = State(b)

b.wordPuzzle = ["A", "B"]
b.wordsList = ["AB", "BA"]
b.foundWords = ["AB"]
b.numberOfLetters = 15
b.status = "Adept"
b.points = 34
b.wordListSize = len(b.wordsList)

a.allSaveNamesTest(c)
a.saveTest(c, "saveTest", b.wordPuzzle, b.wordsList, b.foundWords, b.status, b.points, len(b.wordsList), b.numberOfLetters)
a.saveDataTest(c, "saveTest3", ["A", "B"], ["AB", "BA"], ["AB"], "Adept", 34, len(b.wordsList), 15, 0)
a.loadTest(c, "saveTest3", b)
a.isSavedTest(c, "saveTest3")
a.saveParseTest(c, b, "saveTest", b.wordPuzzle, b.wordsList, b.foundWords, b.status, b.points, len(b.wordsList), b.numberOfLetters)

if os.path.exists("saveFiles/saveTest.json"):
    os.remove("saveFiles/saveTest.json")
if os.path.exists("saveFiles/saveTest2.json"):
    os.remove("saveFiles/saveTest2.json")
if os.path.exists("saveFiles/saveTest3.json"):
    os.remove("saveFiles/saveTest3.json")
    