import os
from .gen_functions import raiseWarning
#This file determines the path to use for sound names depending on the bnk projectID.
def getGameSoundNames(projectID):#dwProjectID in bnk
    csvDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))#Gets directory of gamesupport.py and moves to the parent directory
    soundPathDictionary = {
    6869:os.path.join(csvDir,"SoundNames_replicant.csv"),#NieR Replicant
    2317:os.path.join(csvDir,"SoundNames_automata.csv"),#NieR Automata
    1114:os.path.join(csvDir,"SoundNames_MHWorld.csv"),#Monster Hunter World
    3485:os.path.join(csvDir,"SoundNames_MHRise.csv"),#Monster Hunter Rise
    
    }
    
    return soundPathDictionary.get(projectID,os.path.join(csvDir,"SoundNames_unknown.csv"))
def checkBNKExtension(extension):
    supportedExtensions = [".bnk",".nbnk",".2",".nsw",".en",".ja",".fc"]
    if extension.lower() in supportedExtensions:
        return True
    else:
        raiseWarning("Unknown file extension: "+ extension)
        return False