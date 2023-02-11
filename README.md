
## 2023sp-420-SNEK
## Spelling Bee - SNEK

## Description

    -A Spelling Bee game, implemented in Python with an SQLite database


![Screenshot](SNEKTransperent.png)

### Contributers

    -Aitor Cantero Crespo
    -Bogdan Balagurak
    -Josue Perez-Crespo
    -Miguel Armedariz Llanos
    -Nick Hoopes
    -Stephen Clugston

### Neccessary Libraries

    -Used in Datasource and Database
        -requests
        -json
        -numpy
        -sqlite3
        -Pandas
    -Used in Puzzle Class
        -random
    -Used in User Interface
        -abc
    -Used in Commands
        -enum
    -Used in Terminal Interface
        -colorama
        -math
    -Used in State
        -json
        -os
    -Used in Game Controller
        -random
        -string
    -Used in Setup
        -os
        -json
        -time
    

### Instructions for Building and Playing: Notes

    Note 1: The program has a few libraries that need installation for proper function.
            These are colorama, requests, numpy, and pandas

    Note 2: There are two sets of instructions below, one for those who want to use the 
            setup python script and another for those who don't.

    Note 3: if there is not a saveFiles folder present in the working directory, create one for
            the game to store saves into (must be named explicitly "saveFiles")


### Instructions for Building using Setup

    1. Run setup via command line, in the form (python setup.py)

    2. setup.py will prompt the user whether or not they want to 
       automatically install all need libraries listed in Note 1 above.
       If so, the commands for pip installing the libraries will be run.
       Then, shortly after, the database will be setup to work with random
       words.

       Side note: If you do not have the pip installer, well, installed,
       https://pip.pypa.io/en/stable/installation/, could help
    
    3. At this stage, everything should be in-place to run the program and 
       play the game, simply run the main file via the command line or code editor terminal,
       in the form (python main.py)



### Instructions for Building w/o using Setup

    1. Install the four libraries listed in Note 1, either by using pip install
       or manually moving the libraries into the working directory.

       Side note: If you do not have the pip installer, well, installed,
       https://pip.pypa.io/en/stable/installation/, could help

    2. locate and open the launch.ipynb file with your perffered code
       editor.

    3. Within the code editor, locate the first and last cell in the launch.ipynb file, and
       run them (in vscode, the play button in the upper right left corner of the cell).
    
    4. Make sure an "example3.db" was created in the directory.
    
    5. At this stage, everything should be in-place to run the program and 
       play the game, simply run the main file via the command line or code editor terminal,
       in the form (python main.py).

### Instructions for Playing

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

    Side Note: If you forget any of these instructions or commands, the inital
               splash screen of the game has them, and using the help command
               will also bring them up!



### And Remember
    
# ***`No Step On Snek`***

        

