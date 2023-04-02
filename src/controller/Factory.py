from view.BeeUI import BeeUI
from view.TerminalInterface import TerminalInterface


class Factory:
    def produceInterface(self, interFaceOption):

        options = {
            "CLI": TerminalInterface,
            "GUI": BeeUI,
        }

        return options[interFaceOption]()
