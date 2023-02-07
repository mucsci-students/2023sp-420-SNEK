# gameController class to handle functionailty of the puzzle
# Stephen Clugston

import random
from puzzle import puzzle
from exceptions import exceptions

class gameController:

    # Class Variables
    gameOver = False
    

# search found words for the word first, then search in the wordsList for a correct guess

    # Guess function to handle the functionailty of making a guess.
    # Stephen Clugston
    def guess(userGuess):
        if userGuess >= 4:
        
            if userGuess.contains(puzzle.wordPuzzle[0]):
            
                if puzzle.wordsList.contains(userGuess):
            
                    # If this guess is the last possible guess, increment points, decrement wordListSize and set class variable gameOver to true
                    if puzzle.wordListSize == 0:
                        puzzle.points += userGuess.length()
                        --puzzle.wordListSize
                        print("Congradulations! All words have been guessed!") 

                    # If there are still possible guesses, increments points, remove the word from the possible guesses, and add the word to found words
                    puzzle.points += userGuess.length()
                    --puzzle.wordListSize
                    puzzle.wordsList.remove(userGuess)
                    puzzle.foundWords.add(userGuess)
            
                # If the guessed word is not in the array of possible solutions
                if not puzzle.wordsList.contains(userGuess):
                    # Output error saying the guess was incorrect
                    print("Guessed word was not correct, try again.")
        
                # The guess did not contain the required letter
                print("Guessed word must contain the required letter")

            # The guess was less than 4 letters
            print("Guessed word must be 4 letters or more")


    # Guess function to handle the functionailty of making a guess.
    # Stephen Clugston
    def newGuess(userGuess):
        if userGuess >= 4:
            if userGuess.contains(puzzle.wordPuzzle[0]):
                
                # If this guess is a valid correct guess
                if not puzzle.foundWords.contains(userGuess) and puzzle.wordsList.contains(userGuess):
                    
                    # If this guess is the last possible guess, increment points, decrement wordListSize and set class variable gameOver to true
                    if puzzle.wordListSize == 0:
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
                    return guessAlreadyMade(Exception)
                
                # If the guessed word is not in the array of possible solutions
                if not puzzle.wordsList.contains(userGuess):
                    # Output error saying the guess was incorrect
                    incorrectGuess(Exception)

            # The guess did not contain the required letter
            return noReqLetter(Exception)
        
        # The guess was less than 4 letters
        return lessThanFourLetters(Exception)

    

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

    





class incorrectGuess(Exception):
    "Raised when the guess is valid but not correct"
    pass

class noReqLetter(Exception):
    "Raised when the guess does not contain the required letter"
    pass

class lessThanFourLetters(Exception):
    "Raised when the guess is less than 4 letters long"
    pass

class guessAlreadyMade(Exception):
    "Raised when the guess was already correctly guessed previously"
    pass