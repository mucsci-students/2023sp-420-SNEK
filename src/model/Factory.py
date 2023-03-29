from src.view.BeeUI import BeeUI
from src.view.TerminalInterface import TerminalInterface


class Factory:
    def __init__(interFaceOption):
    
        options = {
            "CLI": TerminalInterface,
            "GUI": BeeUI,

        }
        return options[interFaceOption]()