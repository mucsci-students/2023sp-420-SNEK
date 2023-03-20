class Hint:
    letterMatrix = dict()
    beginingList = dict()  
    pangram = 0
    perfectPangram = 0
    bingo =  False
    numberOfWords = 0
    def __init__(self, letterMatrix:dict[str, dict[str, int]], beginingList:dict[str,int], pangram:int , perfectPangram:int , bingo:bool, numberOfWords:int ):
        self.beginingList = beginingList
        self.letterMatrix = letterMatrix
        self.pangram = pangram
        self.perfectPangram = perfectPangram
        self.bingo = bingo
        self.numberOfWords = numberOfWords
