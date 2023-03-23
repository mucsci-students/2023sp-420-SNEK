from pynput import keyboard, mouse
import pygetwindow as gw
import os
import signal

class Imputer:

    def __init__(self):
        activeWindow = gw.getActiveWindow()
        self.myWindow = '' if not hasattr(activeWindow, 'title') else activeWindow.title
        self.shift = False
        self.control = False
        self.other = False
        self.endOfInput = False
        self.backspace = False
        self.userInput = ""
        self.originalIndex = 0
        self.keyboardListener = None
        self.originals = []
        
    def __distance(self, originalStr, possibleStr):
        return 1
    
    def __orderStrings(self, possibles):
        distances = [self.__distance(self.userInput, possible) for possible in self.possibles]
        possibles = [possible for _, possible in sorted(zip(distances, possibles))]
        return possibles
    
    
    def on_click(self, x, y, button, pressed):
        activeWindow = gw.getActiveWindow()
        newWindow = '' if not hasattr(activeWindow, 'title') else activeWindow.title
        
        if newWindow != self.myWindow:
            self.keyboardListener.stop()
        elif not self.keyboardListener.is_alive():
            self.keyboardListener = self.__createKeyboardListener()
            self.keyboardListener.start()

    def on_release(self, key: keyboard.Key):
        if (key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r):
            self.shift = False

        elif (key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r or key == keyboard.Key.ctrl):
            self.control = False

        elif key == keyboard.Key.backspace:
            self.backspace = False

        elif key != keyboard.Key.tab:
            self.other = False
        
        self.__showPrompt()

    def on_press(self, key: keyboard.Key):
        
        if hasattr(key, "char"):
            keyChar = key.char
        else:
            keyChar = None
            
        # <ctrl> [either normal, right or left]
        if ((key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r or key == keyboard.Key.ctrl)
            and not self.other and not self.backspace):
            self.control = True
            
        # <ctrl>+'c'
        elif keyChar == 'c' and self.control and not self.other and not self.shift:
            self.endOfInput = True
            self.keyboardListener.stop()
            self.mouseListener.stop()
            os.kill(os.getpid(), signal.SIGABRT)
            
        # <backspace>
        elif (key == keyboard.Key.backspace and not self.other and not self.shift):
            self.backspace = True
            k = len(self.userInput) - 1
            if k > 0:
                self.userInput = self.userInput[:k]
            else:
                self.userInput = ""
            self.possibles = self.__orderStrings(self.possibles)
            
            self.__adjustOriginals()

        # <shift> [either normal, right or left]
        elif ((key == keyboard.Key.shift or key == keyboard.Key.shift_l or key == keyboard.Key.shift_r)
               and not self.other and not self.control and not self.backspace):
            self.shift = True
            
        # <ctrl>+'z'
        elif (keyChar == 'z' and not self.shift
                and self.control and not self.other and not self.backspace):
            if self.originalIndex > 0:
                self.originalIndex -= 1
                
            if len(self.originals) > 0:
                self.userInput = self.originals[self.originalIndex]
                self.possibles = self.__orderStrings(self.possibles)

        # <ctrl>+'y'
        elif (keyChar == 'y' and not self.shift
                and self.control and not self.other and not self.backspace):
            if self.originalIndex < len(self.originals) - 1:
                self.originalIndex += 1
                
            if len(self.originals) > 0:
                self.userInput = self.originals[self.originalIndex]
                self.possibles = self.__orderStrings(self.possibles)

        # <shift>+<tab>
        elif self.shift and key == keyboard.Key.tab and not self.other and not self.backspace:
            if self.possibleIndex > 0:
                self.possibleIndex = self.possibleIndex - 1
                
            if len(self.possibles) > 0:
                self.userInput = self.possibles[self.possibleIndex]
                self.possibles = self.__orderStrings(self.possibles)
            
            self.__adjustOriginals()

        # <shift>+1 (= !)
        elif self.shift and keyChar == '1' and not self.other and not self.backspace:
            self.userInput += '!'
            self.possibles = self.__orderStrings(self.possibles)
            self.__adjustOriginals()

        # <tab>
        elif key == keyboard.Key.tab and not self.other and not self.shift and not self.backspace:
            if self.possibleIndex < len(self.possibles) - 1:
                self.possibleIndex = self.possibleIndex + 1
                
            if len(self.possibles) > 0:
                self.userInput = self.possibles[self.possibleIndex]
                self.possibles = self.__orderStrings(self.possibles)
            
            self.__adjustOriginals()

        # <enter>
        elif key == keyboard.Key.enter and not self.other and not self.shift and not self.backspace:
            self.endOfInput = True
            self.keyboardListener.stop()
            self.mouseListener.stop()

        # <space>
        elif key == keyboard.Key.space and not self.other and not self.shift and not self.backspace:
            self.userInput += ' '
            self.possibles = self.__orderStrings(self.possibles)
            self.__adjustOriginals()

        # any key that is not either of the above combinations 
        else:
            self.other = True
            if keyChar != None:
                self.userInput += keyChar
                self.possibles = self.__orderStrings(self.possibles)
                self.__adjustOriginals()
                
        self.__showPrompt()

    def __adjustOriginals(self):
        if self.originalIndex == 0:
            self.originals = ['']
        elif self.originalIndex < (len(self.originals) - 1):
            self.originals = self.originals[:self.originalIndex]
        
        self.originals += [self.userInput]
        self.originalIndex += 1
        
        
    def __showPrompt(self):
        hidingSpaces = ''.join([' '] * (len(self.originals[self.originalIndex-1]) + 2))
        print("\r>> " + self.userInput, end=hidingSpaces)
        
    def __createKeyboardListener(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
            suppress=True)
        
        return listener

    def on_press_option(self, key: keyboard.Key):
        
        if hasattr(key, "char"):
            self.userInput = key.char
            self.optionListener.stop()

    def inputSingleLetter(self):
        self.optionListener = keyboard.Listener(
            on_press=self.on_press_option,
            suppress=True)
        self.optionListener.start()
        self.optionListener.join()
        
        return self.userInput

    def input(self, possibles=[]):
        self.originalIndex = 0
        self.possibles = possibles
        self.possibleIndex = -1
        self.userInput = ""
        self.originals = ['']
        
        self.mouseListener = mouse.Listener(on_click=self.on_click)
        self.mouseListener.start()

        self.keyboardListener = self.__createKeyboardListener()
        
        self.__showPrompt()
        
        self.keyboardListener.start()
        self.mouseListener.join()
        print('\n', end="\r")

        return self.userInput
    

i = Imputer()
m = i.input(["a", "b", "c"])
print('.'+m+'.')