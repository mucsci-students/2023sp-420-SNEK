"""
status.py
Bogdan Balagurak
This class takes points and status from the Puzzle.py
file and lets the user know their points
and their rank 

"""

# import required file 
import Puzzle

# new variables to use here after
# importing from Puzzle.py
new_status = Puzzle.status
new_points = Puzzle.points

class showStatus:

    # tests
    # points = [350]
    # userInput = input()
    # status = "temp"

    # statusCheck definitions checks first if a puzzle is 
    # open and lets the user know to open one
    # to see their rank if they havent already
    # then it uses an any function to compare user 
    # points and assigns the proper status and lets
    # the user know hoe many points they have
    def statusCheck(points, status):
        
        if status == "":

            print ("Please open a puzzle to see rank!")

        elif status != "":

            print("Here are your stats for this puzzle")

            if any(x in points for x in range(0, 150)):

                print("You are a Novice")
                status = "Novice"
                print (str(*points) + " Points") 

            if any(x in points for x in range(150, 250)):

                print("You are a getting better!")
                print("You are an Intermediate")
                status = "Intermediate"
                print (str(*points) + " Points")

            if any(x in points for x in range(250, 350)):

                print("Wow, look at you!")
                print("You are Advanced")
                status = "Advanced"
                print (str(*points) + " Points")
            
            if any(x in points for x in range(350, 450)):

                print("Bruh, you crazy!")
                print("You are a Master")
                status = "Master"
                print (str(*points) + " Points")

        return status

    # take user input and if it is "status"
    # then it will let user know their points
    # and level that they are currently at
    # if userInput == "status":

    #    statusCheck(points,status)