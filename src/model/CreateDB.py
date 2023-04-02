
##
# this script creates the db after depurating the words, it inserts them
# Run this script only once, if else it will giver error messages for trying to overwrite the DB
##


import requests
import sqlite3
import pandas as pd


letterArray = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

con = sqlite3.connect("spellingBee.db")
cur = con.cursor()
# create the table in the DB
cur.execute("CREATE TABLE word_list ( numLetter INT,letter VARCHAR(10) NOT NULL,differentLetters VARCHAR(45) NOT NULL, word VARCHAR(45) NOT NULL, PRIMARY KEY (word))")

for letter in letterArray:
    resp = requests.get('https://www.wordgamedictionary.com/word-lists/words-that-start-with/letter/' +
                        letter+'/words-that-start-with-'+letter+'.json')

    JSONWord = resp.json()
    # Depuraitng words, first, we delete all the words with less than 4 letters and then, delete all the words with more than 7 different letters
    wordsDF = pd.DataFrame(JSONWord)
    # maske to delete the words with less then 4 letters
    lengthMaks = wordsDF.word.str.len() > 3
    wordsDF = wordsDF[lengthMaks]

    # list of booleans saying if a word has more than 7 differtent letters or not
    numberLettersMask = [len(set(list(word))) < 8 for word in wordsDF.word]
    wordsDF = wordsDF[numberLettersMask]  # apply the list as a mask
    # list of differtent letters in each word
    letterList = [''.join(set(list(word))) for word in wordsDF.word]
    lengthList = [len(word) for word in wordsDF.word]
    # join both list and the letter
    dbList = list(zip(lengthList, [letter] *
                  len(wordsDF), letterList, wordsDF.word))

    con = sqlite3.connect("spellingBee.db")
    cur = con.cursor()
    cur.executemany(
        "INSERT INTO word_list (numLetter,letter,differentLetters , word) VALUES (?, ?, ?, ?);", dbList)
    con.commit()
    con.close()
