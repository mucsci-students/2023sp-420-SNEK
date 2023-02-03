"""
shuffle.py
Bogdan Balagurak
This class takes the list of letters of the puzzle and 
shuffles the letters around if the user enters the shuffle command
in the CLI. 

"""

# import required file 
#import state

class showStatus:

    # tests
    points = [152]
    userInput = input()
    status = "152"

    # shuffles letters in list
    # using random.shuffle.
    # first slice list where all but 0 is rearranged
    # 0 is the center letter that is not
    # supposed to be rearranged.
    # after slice, use random shuffle on the
    # new list that was created and then return 
    # element 0 form original list and join the
    # shuffled list to it.
    def statusCheck(points, status):
        if status == "":

            print ("Please open a puzzle to see rank!")

        elif status != "":

            print("Here are your stats for this puzzle")

            if any(x in points for x in range(50, 150)):
                print("You are a Beginner")
                status = "Beginner"
                print (str(*points) + " Points") 

            if any(x in points for x in range(151, 250)):
                print("You are a Getting better")
                status = "Novice"
                print (str(*points) + " Points")
                
        return status

    # take user input and if it is "shuffle"
    # then it will let user know that here is a new shuffle
    # it will display the new shuffled puzzle after completing
    # function and will then ask then to type "shuffle" if
    # they want to shuffle the puzzle again
    if userInput == "status":

        statusCheck(points,status)