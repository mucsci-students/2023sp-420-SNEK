#Imports to manipulate json and file properties
import json
import os

#state class
#from state import X
class state:


    # function for translating from standalone variables to json format
    # also parses json format to standalone variables
    def saveParse(saveName = "tempName", puzzle = [], wordList = [], foundWords = [], status = "Beginner", points = 0, data = []):

        #Instructions for Parser, all arguments are optional
        #If shifting to json, place all standalone variables and no data
        #If shifting to variables, place data (json dictionary) anmd no variables


        retData = []

        if(data == []):
            #Json format
            retData = {

                saveName : 
                [
                    {
                        'puzzle' : puzzle,
                        'wordList' : wordList,
                        'foundWords' : foundWords,
                        'status' : status,
                        'percent' : points 
                    }
                ]
            }

        elif(data != []):
            #loop through all save files
            for i in data:
                #check if key is equal to saveName
                if(list(i)[0] == saveName):
                    #add the values to a new array
                    retData.append(list(i.values()))

            #in the form of [[[{dictionary}]]]
            #return just the dictionary
            return retData[0][0][0]
                

        return retData


