import pytest
import sys
import os


sys.path.append("src")


def main():

    if len(sys.argv) == 1 or sys.argv[1].lower() == "all" and len(sys.argv) == 2:

        pytest.main(["UnitTests/"])

    elif sys.argv[1].lower() == "cov" or sys.argv[1].lower() == "all" and sys.argv[2].lower() == "cov":

        pytest.main(["UnitTests/", "--cov"])

    elif sys.argv[1].lower() == "single":

        counter = 0
        filLis = os.listdir("src/controller") + os.listdir("src/model") + os.listdir("src/view")

        for i in filLis:

            if i == "__pycache__":
                filLis.remove(i)

        for i in filLis:

            counter += 1
            print(f"{counter}. {os.path.splitext(i)[0]}")

        while True:
            try:
                selection = int(input("File to test(1,2,3,etc.): "))
                if(selection > counter):
                    print("Invalid value")
                else:
                    break
            except:
                print("Invalid value")
        
        tempSelect = os.path.splitext(filLis[selection - 1])[0]
        testLis = os.listdir("UnitTests/")

        for i in testLis:

            if i == "__pycache__" or i == "Mocks" or i == "saveFiles":
                pass
            else:
                if tempSelect == os.path.splitext(i)[0].split("_", 1)[-1]:
                    pytest.main(["UnitTests/" + str(i)])
                    return
                
        print("No Tests Made for This Module")
                
    elif sys.argv[1].lower() == "model":

        pytest.main(["UnitTests/", "--cov=src/model"])

    elif sys.argv[1].lower() == "controller":

        pytest.main(["UnitTests/", "--cov=src/controller"])
    
    elif sys.argv[1].lower() == "view":

        pytest.main(["UnitTests/", "--cov=src/view"])
    


            