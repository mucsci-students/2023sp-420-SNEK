"""
showStatus.py
Bogdan Balagurak
 

"""

import main

letters = main.letters

class showStatus:
    def status():
        return 0



    while main.userInput == "status":

        if letters == []:
            print("No status to show, please open a puzzle!") 

        else:    
            print("Here is the status for this puzzle")
            status()
            userInput = input("Enter rearrange again to shuffle again: ")