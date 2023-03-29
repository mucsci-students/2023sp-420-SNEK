from enum import Enum, auto


class Commands(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return count + 1

    EXIT = auto()
    HELP = auto()
    NEW_GAME_WRD = auto()
    NEW_GAME_RND = auto()
    SAVE = auto()
    LOAD = auto()
    SHUFFLE = auto()
    GUESSED_WORDS = auto()
    RANK = auto()
    SHOW_STATUS = auto()
    UNDEFINED = auto()


    class Constant:  # use Constant(object) if in Python 2
        def __init__(self, value):
            self.value = value

        def __get__(self, *args):
            return self.value

        def __repr__(self):
            return '%s(%r)' % (self.__class__.__name__, self.value)

    __CMD_MARK = Constant("!")
    __CMD_DIC = Constant(
        {
            "exit": EXIT,
            "help": HELP,
            "new wrd": NEW_GAME_WRD,
            "new rnd": NEW_GAME_RND,
            "save": SAVE,
            "load": LOAD,
            "shuffle": SHUFFLE,
            "guessed": GUESSED_WORDS,
            "rank": RANK,
            "status": SHOW_STATUS
        })

    @ classmethod
    def getCommandFromName(cls, name: str):
        name = name.strip().lower()
        if name.startswith(cls.__CMD_MARK):
            commandWithoutMarker = name[len(cls.__CMD_MARK):]
        else:
            commandWithoutMarker = name

        commandConstant = Commands(cls.__CMD_DIC.get(commandWithoutMarker, Commands.UNDEFINED))

        return commandConstant
    
    @classmethod
    def getCommandNameList(cls):
        commandNameList = [cls.__CMD_MARK + cmdName for cmdName in list(cls.__CMD_DIC.keys())]
        return commandNameList

    @ classmethod
    def isCommand(cls, name) -> bool:
        if type(name) == str:
            name = name.strip().lower()

            return (name.startswith(cls.__CMD_MARK) and
                    name[len(cls.__CMD_MARK):] in cls.__CMD_DIC.keys())
        else:
            return True
