
from src.Model.DataSource import *
from src.View.UserInterface import *
from src.Controller.GameController import *
from src.Model.Commands import Commands
from src.View.TerminalInterface import TerminalInterface
from src.Controller.customExcept import InvalidArgumentException
from src.View.BeeUI import *
import sys




DB_FILE_NAME = "spellingBee.db"


def main():
    # If no arguments are given
    dataSource = DataSource()
    if len(sys.argv) == 1:
        myGameController = GameController(dataSource)
        myUserInterface = BeeUI()

        myGameController.setUserInterface(myUserInterface)
        myUserInterface.setController(myGameController)
        myUserInterface.launch() # launch window
    # If first arg given is --cli
    elif sys.argv[1] == '--cli':
        myGameController = GameController(dataSource)
        myUserInterface = TerminalInterface()
        myGameController.setUserInterface(myUserInterface)
        myUserInterface.setController(myGameController)
        myUserInterface.showHelp()

        try:
            myUserInterface.launch()
        except KeyboardInterrupt:
            print()
            exit()
    # Any other case
    else:
        print("Raised when an invalid argument is passed to the main call.\n      Possible args: --cli (Launches in CLI mode).")
        raise InvalidArgumentException

# BeeUI will launch automatically without any arguments
# if the --cli flag is passed behind (py main.py --cli),
# the game will launch in CLI mode.
# otherwise, an InvalidArgumentException will be raised.
if __name__ == "__main__":
    main()

