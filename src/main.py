
import sys


from model.DataSource import *
from model.Factory import Factory
from view.UserInterface import *
from controller.GameController import *
from view.TerminalInterface import TerminalInterface
from controller.customExcept import InvalidArgumentException
from view.BeeUI import *




DB_FILE_NAME = "spellingBee.db"


def main():
    if(os.path.exists("spellingBee.db")):
        pass
    else:
        with open("./model/CreateDB.py") as f:
            exec(f.read())

    # If no arguments are given
    dataSource = DataSource("spellingBee.db")
    myFactory = Factory()
    if len(sys.argv) == 1:
        myGameController = GameController(dataSource)
        myUserInterface = myFactory.produceInterface("GUI")

        myGameController.setUserInterface(myUserInterface)
        myUserInterface.setController(myGameController)
        myUserInterface.launch() # launch window
    # If first arg given is --cli
    elif sys.argv[1] == '--cli':
        myGameController = GameController(dataSource)
        myUserInterface = myFactory.produceInterface("CLI")
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

