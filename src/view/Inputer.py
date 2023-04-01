from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import prompt
from prompt_toolkit.application import run_in_terminal, in_terminal
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.filters import Filter
from prompt_toolkit import print_formatted_text, ANSI
from prompt_toolkit.keys import Keys
import os


class Inputer:

    class MyCustomCompleter(Completer):
        ''' Class for completing paths extending the 'Completer' base class.

            Behavior:
                Gives the completer the right strings to complete the input (in order).

            Notes:
                Completes with the nearest option from the given ones, preferring the ones
                that start the same way as the input.
        '''

        def __init__(self, options: list[str] = None):
            self.options = options if options is not None else []
            self.userInput = ''

        # Fn that calculates the number of character changes needed between two strings
        def __lev(self, str1: str, str2: str) -> int:
            ''' Input:
                    two strings to compare (str1 and str2).

                Output:
                    the edit distance between the 2 strings (starting from the front).
            '''
            # if string 1 is empty, return the length of string 2
            if str1 == "":
                return len(str2)

            # if string 2 is empty, return the length of string 1
            if str2 == "":
                return len(str1)

            # if the last character in each strings are equal, set dist = 0
            if str1[0] == str2[0]:
                return self.__lev(str1[1:], str2[1:])

            else:
                # sum of the distance between the levDist for str1 - 1, for str2 - 1, str1 - 1 and str2 - 1
                return min([self.__lev(str1[1:], str2),
                            self.__lev(str1, str2[1:]),
                            self.__lev(str1[1:], str2[1:]) + 1])

        def __orderStrings(self, possiblesList: list[str]):
            ''' Input:
                    two strings to compare (str1 and str2).

                Output:
                    the edit distance between the 2 strings (starting from the front).
            '''
            if possiblesList == []:
                return possiblesList

            prefixed = [
                possible for possible in possiblesList if possible.startswith(self.userInput)]
            nonPrefixed = [
                possible for possible in possiblesList if not possible.startswith(self.userInput)]
            prefixedDistances = [self.__lev(
                self.userInput, possible) for possible in prefixed]
            SortedPrefixed = [possible for _, possible in sorted(
                zip(prefixedDistances, prefixed))]
            SortedNonPrefixed = nonPrefixed
            mostPossibles = SortedPrefixed + SortedNonPrefixed
            return mostPossibles

        def get_completions(self, document, complete_event):
            ''' Input:
                    Defaults for the class to work.

                Output:
                    Yields every possible completion based on the input already given.
            '''
            self.userInput = document.text
            self.options = self.__orderStrings(self.options)
            for possible in self.options:
                yield Completion(possible, start_position=-document.cursor_position)

    class MyCustomPathCompleter(Completer):
        ''' Class for completing paths extending the 'Completer' base class.

            Behavior:
                Gives the completer the right strings to complete the input (in order).

            Notes:
                Completes just the last part of the path (normalized). 
                If no base path is given the current one is chosen.
        '''

        def __init__(self, basedir: str = None):
            self.basedir = basedir

            if self.basedir == "":
                self.basedir = os.getcwd()
            else:
                self.basedir = os.path.normpath(self.basedir)
                self.basedir = os.path.abspath(self.basedir)

                if not os.path.exists(self.basedir):
                    self.basedir = os.getcwd()

        def __calcDirs(self, basedir):
            basedir = os.path.normpath(basedir)
            basedir = os.path.abspath(basedir)
            if os.path.exists(basedir):
                return os.listdir(basedir)
            else:
                return []

        def get_completions(self, document, complete_event):
            ''' Input:
                    Defaults for the class to work.

                Output:
                    Yields every possible completion based on the input already given.
            '''
            self.userInput = document.text
            self.basedir = document.text
            dirs = self.__calcDirs(self.basedir)
            for possible in dirs:
                yield Completion(possible, start_position=0)

    def input(self, msg: str = "", possibles=[]):
        ''' Input:
                msg: the message to show before the prompts.
                possibles: the list of possible tab completions.

            Output:
                A string containing the desired (typed) user input.
        '''

        userInput = prompt(ANSI(msg), completer=self.MyCustomCompleter(
            possibles), complete_while_typing=False)

        return userInput

    def inputPath(self, msg: str = "", basedir=""):
        ''' Input:
                msg: the message to show before the prompts.
                basedir: the base dir from which start the tab completion.

            Output:
                A string containing the desired (typed) user input.
        '''

        userInput = prompt(ANSI(msg), completer=self.MyCustomPathCompleter(
            basedir), complete_while_typing=True)

        return userInput

    def quickInput(self, msg: str = '', options=[]):
        ''' Input:
                msg: the message to show before the prompts.
                options: the valid options for the input.

            Output:
                A string containing the desired (typed) user input, without waiting for an enter.
        '''
        bindings = KeyBindings()

        @bindings.add('<any>')
        def _(event: KeyPressEvent):
            pass

        for l in options:
            @bindings.add(l)
            def _(event: KeyPressEvent):
                event.current_buffer.insert_text(event.data)
                event.app.exit(event.data)

        userInput = prompt(ANSI(msg), completer=self.MyCustomCompleter(
            options), key_bindings=bindings)

        return userInput
