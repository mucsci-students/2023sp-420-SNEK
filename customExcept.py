# Game Controller#######################################
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
#######################################################
# State Class###########################################


class SaveNotFound(Exception):
    "Raised when save file is not found, and save type is not overwrite"
    pass


class MasterFileNotFound(Exception):
    "Raised when master save file not found"
    pass


class WrongSaveType(Exception):
    "Raised when save type is not one of the given"
    pass


class OverwriteSave(Exception):
    "Raised when trying to overwrite a save without using an overwrite type"
    pass
######################################################
# Puzzle Class#########################################


class UniqueLetterException(Exception):
    "Raised when the given word does not have 7 unique letters"
    pass


class WordNotFoundException(Exception):
    "Raised when the given word is not found in dictionary"
    pass
######################################################
