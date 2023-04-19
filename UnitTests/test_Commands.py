import sys
sys.path.append('src/model')

import unittest
from Commands import Commands
import os
import sqlite3
import random




class test_Commands(unittest.TestCase):
    
    def test_commandNotFound(self):
    
        self.assertEqual(Commands.getCommandFromName("tortilla"),Commands.UNDEFINED,"command should not exist")

    def test_normalCommands(self):
        self.assertEqual(Commands.getCommandFromName("!help"),Commands.HELP,"command should be help command")
        self.assertEqual(Commands.getCommandFromName("!quit"),Commands.QUIT,"command should be the quit command")
        self.assertEqual(Commands.getCommandFromName("!exit"),Commands.EXIT,"command should be the exit command")
        self.assertEqual(Commands.getCommandFromName("!new word"),Commands.NEW_GAME_WRD,"command should be the new word  command")
        self.assertEqual(Commands.getCommandFromName("!new random"),Commands.NEW_GAME_RND,"command should be the new random  command")
        self.assertEqual(Commands.getCommandFromName("!save"),Commands.SAVE,"command should be the sava  command")
        self.assertEqual(Commands.getCommandFromName("!save secret"),Commands.SAVE_SECRET,"command should be the save secrete command")
        self.assertEqual(Commands.getCommandFromName("!save image"),Commands.SAVE_IMG,"command should be the save image command")
        self.assertEqual(Commands.getCommandFromName("!load"),Commands.LOAD,"command should be the load command")
        self.assertEqual(Commands.getCommandFromName("!shuffle"),Commands.SHUFFLE,"command should be the shuffle command")
        self.assertEqual(Commands.getCommandFromName("!guessed"),Commands.GUESSED_WORDS,"command should be the guessed command")
        self.assertEqual(Commands.getCommandFromName("!rank"),Commands.RANK,"command should be the rank command")
        self.assertEqual(Commands.getCommandFromName("!scores"),Commands.SCORES,"command should be the scores command")
        self.assertEqual(Commands.getCommandFromName("!hints"),Commands.SHOW_HINTS,"command should be the hints command")
        self.assertEqual(Commands.getCommandFromName("!empty"),Commands.CMD_LIKE,"command should be the empty command")

    def test_getCommandList(self):
        expected = ['!exit', '!quit', '!help', '!new word', '!new random', '!save', '!save secret', '!save image', '!load', '!shuffle', '!guessed', '!rank', '!scores', '!hints']
        list = Commands.getCommandNameList()
        self.assertEquals(expected,list,'the command list is incorrect')
    
    def test_isCommand(self):
        self.assertTrue(Commands.isCommandLike("!tortillas"),'the command list is incorrect')
        self.assertFalse(Commands.isCommand("tortillas"),'the command list is incorrect')
        self.assertFalse(Commands.isCommandLike("!help"),'the command list is incorrect')



if __name__ == '__main__':
    unittest.main()