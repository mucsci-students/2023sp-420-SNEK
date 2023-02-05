"""
shuffle.py
Bogdan Balagurak
This class takes the list of letters of the puzzle and 
shuffles the letters around if the user enters the shuffle command
in the CLI. 

"""

# import required utility and 
import random

class shufflePuzzle:

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
    
    # take user input and if it is "shuffle"
    # then it will let user know that here is a new shuffle
    # it will display the new shuffled puzzle after completing
    # function and will then ask then to type "shuffle" if
    # they want to shuffle the puzzle again
    if userInput == "shuffle":
        print("Here is the shuffled puzzle")
        #shuffle(letters)
        print (shuffle(letters))
        print("Enter shuffle again to shuffle more: ")