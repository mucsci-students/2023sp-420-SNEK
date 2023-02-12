import json
import os
import time

#runs the launch depurator for generating the database
def runIpynb():
    #flavor text
    print(".")

    #open the ipynb like a json file
    with open('launch.ipynb') as f:
        nb_content = json.load(f)

        #loop through and execute all cells
        for cell in nb_content['cells']:
            #check if cell is code
            if cell['cell_type'] == 'code':
                source = ''.join(line for line in cell['source'] if not line.startswith('%'))
                #execute cells
                exec(source, globals(), locals())

#send commands to line to install libraries
def pipInstall():
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install numpy")
    os.system("pip install pandas")
    return

#main function
def main():
    #check for input for if they want to manually install or not
    insVal = input("Would you like to install all libraries automatically using pip?\n Libraries include: rquests, numpy, pandas, colorama\n [Y/N]: ")
    #if y run pip install
    if(insVal.lower() == "y"):
        pipInstall()
    else:
        pass

    #flavor text
    print("Setting up random database.", end = "")
    print(".", end = "")

    #run the launch ipynb
    runIpynb()
    time.sleep(3)
    print("Done!")

#execute main
main()