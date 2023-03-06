
## 2023sp-420-SNEK
## Spelling Bee - SNEK

## Description

    -A Spelling Bee game, implemented in Python with an SQLite database


![Screenshot](img/SNEKTransperent.png)

### Contributers

    -Aitor Cantero Crespo
    -Bogdan Balagurak
    -Josue Perez-Crespo
    -Miguel Armedariz Llanos
    -Nick Hoopes
    -Stephen Clugston

### Neccessary Libraries

    Libraries not pre-packaged with Python
    that need installation.

        -colorama
        -requests
        -numpy
        -pandas
        -pytest

### Python Version

    Tested on Python 3.10.9 and Python 3.11.1


### Instructions for Building using Setup

    0. when using windows, execution policy for scripts must be changed
       from default to allow scripts to run like the activate script for the
       virtual environment. This is done by using the command 
       (Set-ExecutionPolicy -ExecutionPolicy RemoteSigned)

    1. Run setup via command line, in the form (python setup.py (Mac/Linux)) (py setup.py (Windows))

    2. setup.py will create a viurutal environment, instatiate databases,
       and intall any required non-base modules/packages into the environment

    3. Entering Virutal Environment
            Linux/Mac
                -use the command line command (source spell/bin/activate)
            Windows
                -use the command line command (spell/Scripts/activate) (powershell)
                -use the command line command (spell\Scripts\activate) (CMD)
                

    4. You should see the virtual environment name (spell) next to the command line 
       path in windows or username in linux/mac, from here you can start the program
       with 
       (python main.py (Mac/Linux) py main.py (Windows) for GUI on start)
       (python main.py --cli (Mac/Linux) py main.py --cli (Windows) for CLI on start)
    
    5. To exit the virtual environment simply type (deactivate) into the command line


### CLI Instructions

    How to play:
    You are given a word puzzle with a bunch of letters
    and a required letter.  The Required letter is in the
    center of the honeycomb.  Every word that you guess
    requires that the center letter be used, otherwise you
    will not receive credit for the guess.  The word that
    you guess also needs to be a valid word in the
    Scrabble dictionary.  Every puzzle has a corresponding
    pangram that it is generated from.  The pangram will
    include every letter in the honeycomb.

    Commands:
    Call commands with a preceeding '!'. Commands may be
    called at anytime.

            -!new rnd - Generate a new random puzzle
            -!new wrd - Genereate a new puzzle with a user given
                        word.  Console will prompt for the word after
                        command is given.
            -!status - Display you status for the current puzzle.
            -!save - Bring up the prompts for saving your current game.
            -!load - Bring up the prompts for loading a saved game.
            -!shuffle - Shuffle the shown puzzle honeycomb randomly, changing
                        the order of the letter randomly other than the 
                        required center letter.  You can use this to
                        help you find other words.
            -!guessed - Shows all the already correctly guessed words.
            -!help - Prints out the help menu.
            -!exit - Exits the game. Will prompt to save.'''
   
### GUI Instructions

![Screenshot](img/spellBeeInstruct.PNG)

### Running Tests

    Command to run pytest (Be sure to be in environment before using)
        Run All:
            - (pytest UnitTests/)
        Run Specific:
            - (pytest UnitTests/TestFileName)




### And Remember
    
#  ***`No Step On Snek`*** 

        

