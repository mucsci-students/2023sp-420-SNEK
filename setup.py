import json
import os
import time

def runIpynb():
    print(".")
    with open('launch.ipynb') as f:
        nb_content = json.load(f)

        for cell in nb_content['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(line for line in cell['source'] if not line.startswith('%'))
                exec(source, globals(), locals())

def pipInstall():
    os.system("pip install requests")
    os.system("pip install colorama")
    os.system("pip install numpy")
    os.system("pip install pandas")
    return


def main():

    insVal = input("Would you like to install all libraries automatically using pip?\n Libraries include: rquests, numpy, pandas, colorama\n [Y/N]: ")

    if(insVal.lower() == "y"):
        pipInstall()
    else:
        pass
    print("Setting up random database.", end = "")
    print(".", end = "")
    runIpynb()
    time.sleep(3)
    print("Done!")


main()