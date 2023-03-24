import random


class Puzzle:
    '''
    Model for the puzzle of the game.

    Static params:
        MIN_WRD_LEN:        Minimum length of the guessed words
        __MIN_POINTS:       Minimum points you can get from a guessed word
        __PANGRAM_BONUS:    Bonus points for pangram
        __PANGRAM_BONUS:    Bonus points for pangram
        __RANK_NAMES_LIST:  The list of names of the rankings, ordered (from small to big)

    Params:
        puzzleLetters:      The word split into an array of characters
        wordList:           Words relative to the puzzle
        guessedWords:       Already guessed words
        currentRank:        Current rank (beginner etc..)
        currentPoints:      Current number of points for the puzzle
        maxPoints:          Total number of points of given game
        rankingsAndPoints:  A dictionary containing the rank names and their thresholds.
    '''
    # Class variables that do not change from game to game:

    MIN_WRD_LEN: int = 4         # Minimum length of the guessed words
    __MIN_POINTS: int = 1        # Minimum points you can get from a guessed word
    __PANGRAM_BONUS: int = 7     # Bonus points for pangram
    # The list of names of the rankings, ordered (from small to big)
    __RANK_NAMES_LIST: list[str] = ["Beginner", "Good Start", "Moving Up", "Good",
                                    "Solid", "Nice", "Great", "Amazing", "Genius"]

    def __init__(self, puzzleLetters: list[str], WordList: list[str], guessedWords: list[str] = None, maxPoints: int = 0, currentPoints: int = 0) -> None:
        ''' Inputs:
                WordList: list of allowed words of the game.
                puzzleLetters: list of letters of the game (the first one being the required one).
        '''
        # Class variables add hoc for this particular game:

        # The word split into an array of characters
        self.puzzleLetters: list[str] = puzzleLetters
        # Words relative to the puzzle
        self.wordList: list[str] = WordList
        # Already guessed words
        if guessedWords == None:
            guessedWords = []
        self.guessedWords: list[str] = guessedWords
        # Current number of points for the puzzle
        self.currentPoints: int = currentPoints
        # Total number of points of given game
        self.maxPoints: int = maxPoints if maxPoints != 0 else self.__calcMaxPoints(WordList, puzzleLetters)
        # A dictionary containing the rank names and their thresholds.
        self.rankingsAndPoints: dict[str,
                                     int] = self.__rankDict(self.maxPoints)
        # Current rank (beginner etc..)
        self.currentRank: str = self.__calcCurrentRank()

    # Static method to calculate the maximum points of a game.
    @classmethod
    def __calcMaxPoints(cls, WordList: list[str], puzzleLetters: list[str]) -> int:
        ''' Inputs:
                WordList: list of allowed words of the game.
                puzzleLetters: list of letters of the game.

            Output:
                sum: the total maximum of points
        '''
        sum:int = 0
        for word in WordList:
            sum = sum + cls.__pointsOf(word, puzzleLetters)
        return sum

    # Static method to calculate the points of a word.
    @classmethod
    def __pointsOf(cls, word: str, puzzleLetters: list[str]) -> int:
        ''' Precondition:
                    All words are correct and their lengths are more than __MIN_WRD_LEN

            Inputs:
                word: the word of which points are being calculated.
                puzzleLetters: list of letters of the game.

            Output:
                the points a word is worth.
        '''
        if len(word) == cls.MIN_WRD_LEN:
            return cls.__MIN_POINTS
        elif set(word) == set(puzzleLetters):
            return len(word) + cls.__PANGRAM_BONUS
        else:
            return len(word)

    # Static method to calculate the points of a word.
    @classmethod
    def __rankDict(cls, maxPoints: int) -> dict[str, int]:
        ''' Inputs:
                maxPoints: the maximum points of a given game.

            Output:
                a dictionary containing the rank names and their thresholds.
        '''
        n = len(cls.__RANK_NAMES_LIST)
        if maxPoints < (n - 1):
            return None

        rankingFunction: function = lambda x: (maxPoints/((n-1)**2)) * x**2

        pointList = [round(rankingFunction(i)) for i in range(n)]

        rankDict = dict(zip(cls.__RANK_NAMES_LIST, pointList))
        return rankDict

    def getMaxPoints(self) -> int:
        ''' Output:
                the maximum points of this given game.
        '''
        return self.maxPoints

    def getRanks(self) -> dict[str, int]:
        ''' Output:
                the dictionary containing the rank names and their thresholds.
        '''
        return self.rankingsAndPoints

    def getCurrentRank(self) -> str:
        ''' Output:
                the name of the current rank of the player.
        '''
        return self.currentRank

    def getRankingsAndPoints(self) -> dict[str, int]:
        ''' Output:
                a dictionary containing the rank names and their thresholds.
        '''
        return self.rankingsAndPoints

    # Actually calculates the current rank
    def __calcCurrentRank(self) -> str:
        ''' Output:
                the name of the current rank of the player.
        '''
        if (self.currentPoints == 0):
            return self.__RANK_NAMES_LIST[0]
        
        i: int = 0
        for i in range(len(self.__RANK_NAMES_LIST)):
            if(self.currentPoints < self.rankingsAndPoints[self.__RANK_NAMES_LIST[i]]):
                break
            
        return self.__RANK_NAMES_LIST[i-1]

    def addGuessWord(self, word: str) -> None:
        ''' Precondition:
                "word" is a string contained in "wordList".

            Inputs:
                word: the word that was guessed.

            Postcondition:
                the points, rank and guessed words get updated accordingly.
        '''
        self.guessedWords.append(word)
        self.currentPoints += self.__pointsOf(word, self.puzzleLetters)
        self.currentRank = self.__calcCurrentRank()

    def getGuessedWords(self) -> list[str]:
        ''' Output:
                a list of the words the player correctly guessed.
        '''
        return self.guessedWords

    def getCurrentPoints(self) -> int:
        ''' Output:
                the points the player achieved.
        '''
        return self.currentPoints

    def getWordList(self) -> list[str]:
        ''' Output:
                the list of correct words allowed in the game.
        '''
        return self.wordList

    def getPuzzleLetters(self) -> list[str]:
        ''' Output:
                the list of letters that make up the game.
        '''
        return self.puzzleLetters

    def shuffle(self):
        ''' Postcondition:
                the list of letters that make up the game gets shuffled, except for the first one.
        '''
        restOfLetters = list(self.puzzleLetters[1:])
        random.shuffle(restOfLetters)
        letters = [self.puzzleLetters[0]] + restOfLetters
        self.puzzleLetters = letters
