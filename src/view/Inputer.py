import keyboard
import signal, os


class Inputer:

    def __init__(self):
        self.endOfInput = False
        self.userInput = ""
        self.originalIndex = 0
        self.originals = []
        self.msg = ""
        self.prev = None
        self.specialDouble = '¨`´^'
        self.commandLetters = 'zyc'
        self.commandKeys = ['ctrl', 'shift']
        
    def __distance(self, str1, str2) -> int:
            
        editDist = self.__lev(str1, str2)
        
        return editDist
        
    # Fn that calculates the number of character changes needed between two strings
    def __lev(self, str1, str2):
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

    
    def __orderStrings(self, possiblesList:list[str]):
        if possiblesList == []:
            return possiblesList
        
        self.possibleIndex = -1
        prefixed = [possible for possible in possiblesList if possible.startswith(self.userInput)]
        nonPrefixed = [possible for possible in possiblesList if not possible.startswith(self.userInput)]
        prefixedDistances = [self.__distance(self.userInput, possible) for possible in prefixed]
        nonPrefixedDistances = [self.__distance(self.userInput, possible) for possible in nonPrefixed]
        SortedPrefixed = [possible for _, possible in sorted(zip(prefixedDistances, prefixed))]
        SortedNonPrefixed = [possible for _, possible in sorted(zip(nonPrefixedDistances, nonPrefixed))]
        mostPossibles = SortedPrefixed + SortedNonPrefixed
        return mostPossibles
    
    
    
    # <ctrl>+'z'
    def __ctrl_z(self):
        if self.originalIndex > 0:
            self.originalIndex -= 1
            
        if len(self.originals) > 0:
            self.userInput = self.originals[self.originalIndex]
            self.possibles = self.__orderStrings(self.possibles)

    # <ctrl>+'y'
    def __ctrl_y(self):
        if self.originalIndex < len(self.originals) - 1:
            self.originalIndex += 1
            
        if len(self.originals) > 0:
            self.userInput = self.originals[self.originalIndex]
            self.possibles = self.__orderStrings(self.possibles)

    # <ctrl>+'c'
    def __ctrl_c(self):
        keyboard.press('esc')
        keyboard.stash_state()
        os.kill(os.getpid(), signal.SIGABRT)
        
    # <shift>+<tab>
    def __shift_tab(self):
            
        if self.possibleIndex > 0:
            self.possibleIndex = self.possibleIndex - 1
            
        if len(self.possibles) > 0:
            self.userInput = self.possibles[self.possibleIndex]
            self.__adjustOriginals()

    # <tab>
    def __tab(self):
        
        if self.possibleIndex < len(self.possibles) - 1:
            self.possibleIndex = self.possibleIndex + 1
            
        if len(self.possibles) > 0:
            self.userInput = self.possibles[self.possibleIndex]
            self.__adjustOriginals()
    

    def __on_press(self, key:str):
        
        if key == self.prev and key in self.specialDouble:
            self.userInput += (key + key)
            self.possibles = self.__orderStrings(self.possibles)
            self.__adjustOriginals()

        else:
            if len(key) == 1 and key not in self.specialDouble:
                specialKeyPressed = False
                if key in self.commandLetters:
                    for specialKey in self.commandKeys:
                        specialKeyPressed = specialKeyPressed or keyboard.is_pressed(specialKey)
                if not specialKeyPressed:
                    self.userInput += key
                    self.possibles = self.__orderStrings(self.possibles)
                    self.__adjustOriginals()

            elif key == 'space':
                self.userInput += ' '
                self.possibles = self.__orderStrings(self.possibles)
                self.__adjustOriginals()
            
            # <backspace>
            elif (key == 'backspace'):
                k = len(self.userInput) - 1
                if k > 0:
                    self.userInput = self.userInput[:k]
                else:
                    self.userInput = ""
                self.possibles = self.__orderStrings(self.possibles)
                
                self.__adjustOriginals()

            self.prev = key
            
        self.__showPrompt()

    def __adjustOriginals(self):
        if self.originalIndex == 0:
            self.originals = ['']
            
        elif self.originalIndex < (len(self.originals) - 1):
            self.originals = self.originals[:self.originalIndex]
        
        self.originals += [self.userInput]
        self.originalIndex += 1
        
        
    def __showPrompt(self):
        hidingSpaces = ''.join([' '] * (len(self.originals[self.originalIndex-1]) + 3))
        print("\r" + self.msg + self.userInput, end=hidingSpaces)


    def input(self, msg: str = "", possibles=[]):
        keyboard.unhook_all()
        self.msg = msg
        self.originalIndex = 0
        self.possibleIndex = -1
        self.possibles = possibles
        self.userInput = ""
        self.originals = ['']
        
        self.__showPrompt()
        
        keyboard.add_hotkey('tab', self.__tab)
        keyboard.add_hotkey('shift+tab', self.__shift_tab)
        keyboard.add_hotkey('ctrl+z', self.__ctrl_z)
        keyboard.add_hotkey('ctrl+c', self.__ctrl_c)
        keyboard.add_hotkey('ctrl+y', self.__ctrl_y)
        keyboard.on_press(lambda x: [self.__on_press(x.name), self.__showPrompt()])
        keyboard.on_release(lambda x: self.__showPrompt)
        keyboard.on_release_key('enter', lambda x: keyboard.press('esc'))
        keyboard.wait('enter', suppress=True)
        keyboard.stash_state()
        
        print('\n', end="\r")
        keyboard.unhook_all()
        
        return self.userInput