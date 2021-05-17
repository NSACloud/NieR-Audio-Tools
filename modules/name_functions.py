import os
import csv
from .gen_functions import raiseWarning
def readWEMNameList(filepath):
    WEMDict = {}
    try:
        if os.path.exists(filepath)and os.path.isfile(filepath) and filepath.endswith(".csv"):
            print("Reading " + filepath + "...")
            with open(filepath) as csvfile:
                csvread = csv.reader(csvfile)
                next(csvread)#skip header line of csv
                for i, row in enumerate (csvread):
                    wemID = int(row[0])
                    wemName = row[1]
                    WEMDict.update({wemID:wemName})
        else:
            raiseWarning(filepath + " not found. WEMs will not use their internal names.")
    except:
        raiseWarning("Failed to read " + filepath)
    return WEMDict
def updateWEMNames(folderpath,csvpath):
    WEMDict = readWEMNameList(csvpath)
    print("Updating WEM names...")
    for root, dirs, files in os.walk(folderpath):
        for file in files:
            if os.path.splitext(file)[1] =='.wem':
                #print("Checking "+file)
                split = (os.path.splitext(file)[0]).rsplit('-',1)#Splits WEM ID from file name
                if len(split) == 2:
                    id = -1#Ignore wem if name is not formatted correctly
                    if split[1].isdigit():
                        id = int(split[1])
                else:#Handles the case of there being no name attached to the wem
                    if split[0].isdigit():
                        id = int(split[0])
                if id in WEMDict:
                    print("Renaming "+file)
                    try:
                        os.rename(os.path.join(root,file),os.path.join(root,WEMDict[id]+"-"+str(id)+".wem"))
                    except:
                        raiseWarning("Failed to rename " + file + ", skipping.")                        
    print("Finished updating WEM names.")