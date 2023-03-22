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
        filLis = os.listdir("UnitTests/")
        filLis.remove('Mocks')
        for i in filLis:
            if i == "__pycache__" or i == "Mocks" or i == "saveFiles":
                filLis.remove(i)

        for i in filLis:
            printVal = os.path.splitext(i)[0].split("_", 1)[-1]
            counter += 1
            print(f"{counter}. {printVal}")

        while True:

            try:
                selection = input("File to test(1,2,3,etc.): ")
                if selection.lower() == "quit":
                    return
                else:
                    selection = int(selection)
                    if (selection > counter):
                        print("Invalid value")
                    else:
                        break
            except:
                print("Invalid value")
        

        if len(sys.argv) > 2 and sys.argv[2].lower() == "cov":
            pytest.main(["UnitTests/" + filLis[selection - 1], "--cov"])
        else:
            pytest.main(["UnitTests/" + filLis[selection - 1]])

                
    elif sys.argv[1].lower() == "model":

        pytest.main(["UnitTests/", "--cov=src/model"])

    elif sys.argv[1].lower() == "controller":

        pytest.main(["UnitTests/", "--cov=src/controller"])
    
    elif sys.argv[1].lower() == "view":

        pytest.main(["UnitTests/", "--cov=src/view"])
    


            