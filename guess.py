# Stephen Clugston
# Guess Class to handle the user making a new guess

from state import state

def guess(userGuess, gameState):
    
    if userGuess >= 4:

        if gameState.wordList.contains(userGuess) == True:
            
            if gameState.number == 1:
                # Points correctly incremented to gameState
                # Message displays saying that the game is complete
                print("hi") 
        
            # points correctly incremented to gameState
            # remove the word from the words still to guess in gameState, and add it to already guessed words
            print("hi")
    
    
        if gameState.wordList.contains(userGuess) == False:
            # Output error saying the guess was incorrect
            print("Guess was not correct")
    
    print("Word must be 4 letters or more")
    


