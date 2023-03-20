class Hint:
    letterMatrix = dict()
    beginingList = dict()  
    pangram = 0
    perfectPangram = 0
    bingo =  False
    def __init__(self, letterMatrix:dict[str, dict[str, int]], beginingList:dict[str,int], pangram:int , perfectPangram:int , bingo:bool ):
        self.beginingList = beginingList
        self.letterMatrix = letterMatrix
        self.pangram = pangram
        self.perfectPangram = perfectPangram
        self.bingo = bingo
