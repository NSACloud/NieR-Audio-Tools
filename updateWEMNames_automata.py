import sys
import os
from modules.name_functions import updateWEMNames
from modules.gen_functions import textColors
GAME = "NieR Automata"
CSVPATH = "SoundNames_automata.csv"
#MAIN
if len(sys.argv) > 1:
    folderpath = sys.argv[1]
else:
    print("No path provided, enter a folder path containing " + GAME + " WEMs.")
    folderpath = str(input("Enter path:"))
folderpath = folderpath.strip('"')
if os.path.isfile(folderpath):
    folderpath = os.path.split(folderpath)[0]#Removes file from path
if os.path.isdir(folderpath) and os.path.exists(folderpath):
    print("\nThe path provided is: " + textColors.OKGREEN + folderpath + textColors.ENDC )
    print("All subdirectories will be checked for " + GAME + " WEMs. "+ textColors.WARNING + "Is this path correct? (yes/no)" + textColors.ENDC)
    result = str(input()).lower()
    if result == "yes" or result == "y":
        updateWEMNames(folderpath,CSVPATH)
    else:
        print("Exiting.")
else:
    print("Invalid folder path.")