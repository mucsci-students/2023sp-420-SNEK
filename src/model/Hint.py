class Hint:
 
    def __init__(self, letterMatrix:dict[str, dict[str, int]], beginingList:dict[str,int], pangram:int , perfectPangram:int , bingo:bool, numberOfWords:int ):
        self.beginningList = beginingList
        self.letterMatrix = letterMatrix
        self.pangram = pangram
        self.perfectPangram = perfectPangram
        self.bingo = bingo
        self.numberOfWords = numberOfWords
