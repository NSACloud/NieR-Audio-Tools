#Author: NSA Cloud
from .bnk_chunks import readBNKChunk,writeBNKChunk
from .gen_functions import textColors,getByteSection,removeByteSection,insertByteSection,raiseError,createIndexDict,getPaddingAmount
from .name_functions import readWEMNameList
from .gamesupport import getGameSoundNames,checkBNKExtension
import os

def readBNK(filepath, eof = None):
#If the eof isn't provided, assume entire file is a bnk
    print(textColors.OKCYAN + "__________________________________\nBNK import started." + textColors.ENDC)
    print("Opening "+filepath)
    file = open(filepath,"rb")
    print("Reading BNK...")
    BNK = {}
    BNK["FileName"] = str(os.path.basename(filepath))#Get file name
    BNK["FileExtension"] = os.path.splitext(filepath)[1]
    if eof == None:
        BNK["EOF"] = os.fstat(file.fileno()).st_size#Get file size
    else:
        BNK["EOF"] = eof#Use given file size
    BNK["chunkList"] = []
    BNK["chunkIndex"] = []
    while file.tell() != BNK["EOF"]:
        BNK["chunkList"].append(readBNKChunk(file))
        BNK["chunkIndex"].append(BNK["chunkList"][len(BNK["chunkList"])-1]["dwTag"])
    print(textColors.OKGREEN + "__________________________________\nBNK import finished.\n" + textColors.ENDC)
    return BNK


def writeBNK(BNK,exportDir):
    print(textColors.OKCYAN + "__________________________________\nBNK export started." + textColors.ENDC)
    try:
            os.makedirs(exportDir)     
    except:
        pass
    file = open(os.path.join(exportDir,BNK["FileName"]), "wb")
    for chunk in BNK["chunkList"]:
        writeBNKChunk(file,chunk)
    file.close()
    print(textColors.OKGREEN + "__________________________________\nBNK export finished.\n" + textColors.ENDC)
#-----BNK extract functions-----#
def extractWEMs(BNK,outputDir):
    #print (BNK["chunkIndex"])
    if "DIDX" in BNK["chunkIndex"] and "DATA" in BNK["chunkIndex"]:
        try:
            os.makedirs(outputDir)     
        except:
            pass
        chunkMediaIndex = BNK["chunkIndex"].index("DIDX")
        chunkDataIndex = BNK["chunkIndex"].index("DATA")
        print("Project ID: " + str(BNK["chunkList"][0]["dwProjectID"]))
        WEMDict = readWEMNameList(getGameSoundNames(BNK["chunkList"][0]["dwProjectID"]))
        
        print("Extracting WEMs...")
        for index, mediaEntry in enumerate(BNK["chunkList"][chunkMediaIndex]["pLoadedMedia"]):
            #print("Extracting WEM "+str(index))
            if mediaEntry["id"] in WEMDict:
                WEMName = WEMDict[mediaEntry["id"]]+ "-"
            else:
                WEMName = ""
            file = open(os.path.join(outputDir,WEMName+str(mediaEntry["id"])+".wem"), "wb")
            #print("current offset: "+ str(mediaEntry["uOffset"]))
            #print("current size: "+ str(mediaEntry["uSize"]))
            file.write(getByteSection(BNK["chunkList"][chunkDataIndex]["pData"],mediaEntry["uOffset"],mediaEntry["uSize"]))
            file.close()
    else:
        raiseError("BNK " + BNK["FileName"] + " contains no WEMs.")
        
    
#-----BNK export functions-----#
def readNewWEMs(inputDir,pLoadedMedia):#Reads wems if their ID matches ones in bnk
    NewWEMList = []
    for root, dirs, filenames in os.walk(inputDir):
        for fileName in filenames:
            if fileName.endswith(".wem"):
                try:
                    split = (os.path.splitext(fileName)[0]).rsplit('-',1)#Splits WEM ID from file name
                    id = int(split[len(split)-1])#Gets WEM ID if it's the entire name of the file or if it's separated with a hyphen on the end of the filename
                except:
                    id = -1#If the wem name isn't formatted properly, ignore it
                #print("Checking for WEM ID " +str(id))
                for dict_ in [MediaHeader for MediaHeader in pLoadedMedia if MediaHeader["id"] == id]:#Check if wem ID of file is in bnk
                    print ("Reading new WEM: "+os.path.join(root,fileName))
                    file = open(os.path.join(root,fileName),"rb")
                    eof = os.fstat(file.fileno()).st_size
                    NewWEM = {}
                    NewWEM["id"] = id
                    NewWEM["data"] = file.read(eof)
                    file.close()
                    NewWEMList.append(NewWEM)           
    return NewWEMList
    
def replaceWEM(MediaHeader,pData,WEM):
    #print(MediaHeader)
    newWEMSize = len(WEM["data"])
    newWEMPadding = getPaddingAmount(newWEMSize,16)
    removeByteSection(pData,MediaHeader["uOffset"],MediaHeader["uSize"]+getPaddingAmount(MediaHeader["uSize"],16))#Removes wem at offset, including it's padding
    insertByteSection(pData,MediaHeader["uOffset"],WEM["data"].ljust((newWEMSize + newWEMPadding), b'\0'))#Inserts padded wem at offset
def updateWEMIndexOffsets(pLoadedMediaSection,sizeDifference):
    for MediaHeader in pLoadedMediaSection:
        MediaHeader["uOffset"] += sizeDifference

def replaceBNKWEMs(BNK, inputDir,exportDir):#Edits the currently imported BNK
    if "DIDX" in BNK["chunkIndex"] and "DATA" in BNK["chunkIndex"]:
        chunkMediaIndex = BNK["chunkIndex"].index("DIDX")
        chunkDataIndex = BNK["chunkIndex"].index("DATA")
        
        NewWEMList = readNewWEMs(inputDir,BNK["chunkList"][chunkMediaIndex]["pLoadedMedia"])#Passes list of wems in bnk
        if NewWEMList == []:
            raiseError("No replacement WEM files were found in the repack directory.")
        wemIDDict = createIndexDict(BNK["chunkList"][chunkMediaIndex]["pLoadedMedia"], "id")
        for WEM in NewWEMList:   
            print("Replacing WEM " + str(WEM["id"])+ " in BNK")
            wemIndex = wemIDDict.get(WEM["id"])
            oldDataSize = len(BNK["chunkList"][chunkDataIndex]["pData"])
            replaceWEM(BNK["chunkList"][chunkMediaIndex]["pLoadedMedia"][wemIndex],BNK["chunkList"][chunkDataIndex]["pData"],WEM)#Passes MediaHeader entry for specific wem
            newDataSize = len(BNK["chunkList"][chunkDataIndex]["pData"])
            sizeDifference = newDataSize - oldDataSize
            print ("WEM "+ str(WEM["id"])+" size difference: "+str(sizeDifference))
            BNK["chunkList"][chunkMediaIndex]["pLoadedMedia"][wemIndex]["uSize"] = len(WEM["data"])#Updates current WEM's size, not including padding 
            updateWEMIndexOffsets(BNK["chunkList"][chunkMediaIndex]["pLoadedMedia"][wemIndex+1::],sizeDifference)#Updates offsets of all entries after current wem
        BNK["chunkList"][chunkDataIndex]["dwChunkSize"] = len(BNK["chunkList"][chunkDataIndex]["pData"])
            
    else:
        raiseError("BNK " + BNK["FileName"] + " contains no WEMs. Cannot repack.")
#-----BNK file functions-----#
def extractBNKFile(SOURCEFILE,OUTPUTDIR):
    BNK = readBNK(SOURCEFILE)
    print(textColors.OKCYAN + "__________________________________\nWEM extract started." + textColors.ENDC)
    extractWEMs(BNK,OUTPUTDIR)
    print(textColors.OKGREEN + "__________________________________\nFinished extracting WEMs to "+ OUTPUTDIR + textColors.ENDC)

def repackBNKFile(SOURCEFILE,INPUTDIR,EXPORTDIR):
    BNK = readBNK(SOURCEFILE)
    print(textColors.OKCYAN + "__________________________________\nBNK repack started." + textColors.ENDC)
    replaceBNKWEMs(BNK,INPUTDIR,EXPORTDIR)
    print(textColors.OKGREEN + "__________________________________\nFinished repacking BNK." + textColors.ENDC)
    writeBNK(BNK,EXPORTDIR)
    print(textColors.OKGREEN + "__________________________________\nSaved BNK to " +EXPORTDIR + textColors.ENDC)