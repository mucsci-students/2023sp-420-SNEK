import json
import os
import time
import platform
import subprocess

#main function
def main():
    
    if platform.system() == "Linux" or platform.system() == "Darwin":
        
        if(os.path.exists("spell")):
            os.system("source spell/bin/activate; python -m pytest tests/")
        else:
            os.system("python -m venv spell")
            os.system("source spell/bin/activate; pip install -r requirements.txt; python dbCreator.py; python -m pytest tests/")

    elif platform.system() == "Windows":

        if(os.path.exists("spell")):
            p1 = subprocess.Popen(["powershell.exe", "spell\Scripts\\activate; py -m pytest tests/"])
        else:
            os.system("py -m venv spell")
            p1 = subprocess.Popen(["powershell.exe", "spell\Scripts\\activate; pip install -r requirements.txt; py dbCreator.py; py -m pytest tests/"])
            p1.wait()

    else:
        print("OS not supported")


#execute main
main()