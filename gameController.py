# gameController class to handle functionailty of the puzzle
# Stephen Clugston

import random
from puzzle import puzzle
from customExcept import customExcept

class gameController:

    # Class Attributes
    gameOver = False
    
    # Guess function to handle the functionailty of making a guess.
    # Stephen Clugston
    def guess(userGuess):
        if userGuess >= 4:
            
            if userGuess.contains(puzzle.wordPuzzle[0]):
                
                # If this guess is a valid correct guess
                    if not puzzle.foundWords.contains(userGuess) and puzzle.wordsList.contains(userGuess):
                    
                        # If this guess is the last possible guess, increment points, decrement wordListSize and set class variable gameOver to true
                        if puzzle.wordListSize == 1:
                            puzzle.points += userGuess.length()
                            --puzzle.wordListSize
                            gameOver = True
                            return gameOver

                        # If there are still possible guesses, increments points, and add the word to found words
                        puzzle.points += userGuess.length()
                        --puzzle.wordListSize
                        puzzle.foundWords.add(userGuess)
                
                        # If the guessed word was already correctly guessed
                        if puzzle.foundWords.contains(userGuess):
                            raise guessAlreadyMade
                
                        # If the guessed word is not in the array of possible solutions
                        if not puzzle.wordsList.contains(userGuess):
                            # Output error saying the guess was incorrect
                            raise incorrectGuess

            # The guess did not contain the required letter
            raise noReqLetter
        
        # The guess was less than 4 letters
        raise lessThanFourLetters

    

    """
    shuffle function
    Bogdan Balagurak
    this function takes the list of letters of the puzzle and 
    shuffles the letters around if the user enters the shuffle command
    in the CLI. 
    """
    # tests
    #letters = ['a','b','c','d','e','f','g']
    #userInput = input()

    # shuffles letters in list
    # using random.shuffle.
    # first slice list where all but 0 is rearranged
    # 0 is the center letter that is not
    # supposed to be rearranged.
    # after slice, use random shuffle on the
    # new list that was created and then return 
    # element 0 form original list and join the
    # shuffled list to it.
    def shuffle(letters):
        restOfLetters = list(letters[1:])
        random.shuffle(restOfLetters)
        return letters[0] + ''.join(restOfLetters)