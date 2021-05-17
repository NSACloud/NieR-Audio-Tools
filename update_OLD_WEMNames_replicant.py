#For updating old Replicant PCK Util V1 and V2 wem names to new format
#Old format names start with index and WEM ID, new format ends with WEM ID
import sys
import os
from modules.name_functions import readWEMNameList
from modules.gen_functions import textColors,raiseWarning
def updateOldWEMNames(folderpath,csvpath):
    WEMDict = readWEMNameList(csvpath)
    print("Updating old WEM names to new format...")
    for root, dirs, files in os.walk(folderpath):
        for file in files:
            if os.path.splitext(file)[1] =='.wem':
                #print("Checking "+file)
                split = (os.path.splitext(file)[0]).split('-',2)#Splits WEM index and WEM ID from file name
               
                if len(split) >= 2:
                    #print (str(split[0]))
                    #print (str(split[1]))
                    if split[0].isdigit() and split[1].isdigit():#Check if split file name is integers
                        index = int(split[0])
                        id = int(split [1])
                        #print("index "+ str(index) + " id "+str(id))
                        if index < 25000 and id > 999:#Checks that digit counts are within a normal range, not foolproof but works well enough
                            if id in WEMDict:
                                print("Renaming "+file)
                                try:
                                    os.rename(os.path.join(root,file),os.path.join(root,WEMDict[id]+"-"+str(id)+".wem"))
                                except:
                                    raiseWarning("Failed to rename " + file + ", skipping.")
                            else:
                                try:
                                    os.rename(os.path.join(root,file),os.path.join(root,str(id)+".wem"))
                                except:
                                    raiseWarning("Failed to rename " + file + ", skipping.")
    print("Finished updating old WEM names.")
    
#MAIN
if len(sys.argv) > 1:
    folderpath = sys.argv[1]
else:
    print("No path provided, enter a folder path containing old format wem names.")
    folderpath = str(input("Enter path:"))
folderpath = folderpath.strip('"')
if os.path.isfile(folderpath):
    folderpath = os.path.split(folderpath)[0]#Removes file from path
if os.path.isdir(folderpath) and os.path.exists(folderpath):
    print("\nThe path provided is: " + textColors.OKGREEN + folderpath + textColors.ENDC )
    print("All subdirectories will be checked for old format wem names. "+ textColors.WARNING + "Is this path correct? (yes/no)" + textColors.ENDC)
    result = str(input()).lower()
    if result == "yes" or result == "y":
        updateOldWEMNames(folderpath,"SoundNames_replicant.csv")
    else:
        print("Exiting.")
else:
    print("Invalid folder path.")