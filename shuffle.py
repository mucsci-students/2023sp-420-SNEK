"""
shuffle.py
Bogdan Balagurak
This class takes the list of letters of the puzzle and 
shuffles the letters around if the user enters the shuffle command
in the CLI. 

"""

# import required utility and 
# other working file to variables

import random
import main

class shufflePuzzle:

    # create local variable letters from global from
    # main file to use in this class

    letters = main.letters

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

    # first make sure there is a puzzle open and if not,
    # alert user to open a puzzle.
    # once open, take user input from main and if it is "shuffle"
    # then it will let user know that here is a new shuffle
    # it will display the new shuffle d puzzle after completing
    # function and will then ask then to type "shuffle" if
    # they want to shuffle the puzzle again

    while main.userInput == "shuffle":

        if letters == []:
            print("Nothing to shuffle, please open a puzzle!") 

        else:    
            print("Here is the shuffled puzzle")
            shuffle(letters)
            userInput = input("Enter rearrange again to shuffle again: ")
