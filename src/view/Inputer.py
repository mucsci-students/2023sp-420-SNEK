from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import prompt
from prompt_toolkit.application import run_in_terminal, in_terminal
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent


class Inputer:

    class MyCustomCompleter(Completer):

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
            # print(document.cursor_position)
            self.userInput = document.text
            self.options = self.__orderStrings(self.options)
            for possible in self.options:
                yield Completion(possible, start_position=-document.cursor_position)

    def input(self, msg: str = "", possibles=[]):
        ''' Input:
                msg: the message to show before the prompts.
                possibles: the list of possible tab completions.

            Output:
                A string containing the desired (typed) user input.
        '''

        userInput = prompt(msg, completer=self.MyCustomCompleter(possibles))

        return userInput

    def quickInput(self, msg: str = '', options=[]):
        bindings = KeyBindings()

        @bindings.add('<any>')
        def _(event: KeyPressEvent):
            pass

        for l in options:
            @bindings.add(l)
            def _(event: KeyPressEvent):
                f" Say 'hello' when {l} is pressed. "
                event.current_buffer.insert_text(event.data)
                event.app.exit(event.data)

        userInput = prompt(msg, key_bindings=bindings)

        return userInput
