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
    CMD_LIKE = auto()
    UNDEFINED = auto()


    class Constant:
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
            "new word": NEW_GAME_WRD,
            "new random": NEW_GAME_RND,
            "save": SAVE,
            "load": LOAD,
            "shuffle": SHUFFLE,
            "guessed": GUESSED_WORDS,
            "rank": RANK,
            "status": SHOW_STATUS
        })

    @classmethod
    def getCommandFromName(cls, name: str):
        name = name.strip().lower()
        if name.startswith(cls.__CMD_MARK):
            commandWithoutMarker = name[len(cls.__CMD_MARK):]
            commandConstant = Commands(cls.__CMD_DIC.get(commandWithoutMarker, Commands.CMD_LIKE))
        else:
            commandWithoutMarker = name
            commandConstant = Commands(cls.__CMD_DIC.get(commandWithoutMarker, Commands.UNDEFINED))

        return commandConstant

    @classmethod
    def isCommand(cls, cmd: str) -> bool:
        if type(cmd) == str:
            cmdName = cmd.strip().lower()
            cmd = cls.getCommandFromName(cmdName)
            return cmd != Commands.UNDEFINED
        
        else:
            return type(cmd) == Commands
