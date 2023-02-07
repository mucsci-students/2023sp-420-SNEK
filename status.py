"""
shuffle.py
Bogdan Balagurak
This class takes the list of letters of the puzzle and 
shuffles the letters around if the user enters the shuffle command
in the CLI. 

"""

# import required file 
# import state

class showStatus:

    # tests
    points = [350]
    userInput = input()
    status = "temp"

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

    # take user input and if it is "shuffle"
    # then it will let user know that here is a new shuffle
    # it will display the new shuffled puzzle after completing
    # function and will then ask then to type "shuffle" if
    # they want to shuffle the puzzle again
    if userInput == "status":

        statusCheck(points,status)