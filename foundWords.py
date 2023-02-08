"""
foundWords.py
Bogdan Balagurak
This class takes points and status from the Puzzle.py
file and lets the user know their points
and their rank 

"""

# import required file 
# import Puzzle
import colorama
from colorama import Fore, Back

#Initialize colorama
colorama.init(autoreset=True)

# new variables to use here after
# importing from Puzzle.py
# new_foundWords = Puzzle.foundWords


class foundWords:

    # tests
    new_foundWords = ["afafa","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf",
    "afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf",
    "afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf","afafafaf",]
    userInput = input()

    # 
    def found(new_foundWords):
        
        if not new_foundWords:

            print ("Please open a puzzle to see found words!")

        else:

            print (Back.YELLOW + "Here are the words that you have found so far!")
            print (*new_foundWords)
            print (Back.YELLOW + "----------------------------------------_-----")
       

    # take user input and if it is "found words"
    if userInput == "found words":

        found(new_foundWords)