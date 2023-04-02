class Hint:

    def __init__(self, letterMatrix: dict[str, dict[str, int]], beginningList: dict[str, int], pangram: int, perfectPangram: int, bingo: bool, numberOfWords: int):
        self.beginningList = beginningList
        self.letterMatrix = letterMatrix
        self.pangram = pangram
        self.perfectPangram = perfectPangram
        self.bingo = bingo
        self.numberOfWords = numberOfWords
