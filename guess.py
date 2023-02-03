# Stephen Clugston
# Guess Class to handle the user making a new guess

from puzzle import puzzle

def guess(userGuess):
    
    if userGuess >= 4:
        if userGuess.contains(puzzle.wordPuzzle[0]):
            
            if puzzle.wordsList.contains(userGuess):
            
                if puzzle.wordListSize == 1:
                    # Points correctly incremented to gameState, and message displays saying that the game is complete
                    puzzle.points += 2
                    --puzzle.wordListSize
                    print("Congradulations! All words have been guessed!") 
                    return 1

                # Increments points, removes the word from the possible guesses, and adds the word to found words
                puzzle.points += 2
                --puzzle.wordListSize
                puzzle.wordsList.remove(userGuess)
                puzzle.foundWords.add(userGuess)
            

            if not puzzle.wordsList.contains(userGuess):
                # Output error saying the guess was incorrect
                print("Guessed word was not correct, try again.")
        
        # The guess did not contain the required letter
        print("Guessed word must contain the required letter")

    # The guess was less than 4 letters
    print("Guessed word must be 4 letters or more")


