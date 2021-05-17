from .gen_functions import textColors,getByteSection,removeByteSection,insertByteSection,raiseError,createIndexDict,getPaddingAmount,read_uint,write_uint,read_unicode_string,write_unicode_string
from .name_functions import readWEMNameList
import os
#-----PCK import functions-----#
def readPCKHeader(file):
    print("Reading PCK Header...")
    Header = {}
    Header["FileType"] = file.read(4)
     
    if Header["FileType"] != b'AKPK':
         raiseError("File is not a PCK file.")
    Header["dataOffset"] = read_uint(file)
    Header["unkn0"] = read_uint(file)#Always seems to be 1
    Header["languageLength"] = read_uint(file)
    Header["bankIndexLength"] = read_uint(file)
    Header["mediaIndexLength"] = read_uint(file)
    Header["unknStructLength"] = read_uint(file)
    return Header
def readPCKLanguages(file):
    print("Reading PCK Languages...")
    Language = {}
    Language["languageCount"] = read_uint(file)
    Language["LangIndexList"] = []
    for i in range(0,Language["languageCount"]):
        LanguageIndexEntry = {}
        LanguageIndexEntry["languageOffset"] = read_uint(file)
        LanguageIndexEntry["languageID"] = read_uint(file)
        Language["LangIndexList"].append(LanguageIndexEntry)
    Language["LangStringList"] = []
    Language["LangIDDict"] = {} #For fast language checking
    for entry in Language["LangIndexList"]:
        string = read_unicode_string(file)
        Language["LangStringList"].append(string)
        Language["LangIDDict"][entry["languageID"]] = string
    #print(Language["LangIDDict"])
    Language["padding"] = file.read(2)
    return Language
def readPCKBNKIndex(file):
    BNKIndex = {}
    BNKIndex["bnkCount"] = read_uint(file)
    if BNKIndex["bnkCount"] != 0:
        print("Reading Bank Index...")
    BNKIndex["BNKIndexList"] = []
    for i in range(0,BNKIndex["bnkCount"]):
        entry = {}
        entry["bnkID"] = read_uint(file)
        entry["unkn1"] = read_uint(file)
        entry["bnkSize"] = read_uint(file)
        entry["bnkOffset"] = read_uint(file)
        entry["langID"] = read_uint(file)
        BNKIndex["BNKIndexList"].append(entry)
    return BNKIndex
def readPCKMediaIndex(file):
    MediaIndex = {}
    MediaIndex["wemCount"] = read_uint(file)
    if MediaIndex["wemCount"] != 0:
        print("Reading Media Index...")
    MediaIndex["mediaIndexEntryList"] = []
    for i in range(0,MediaIndex["wemCount"]):
        entry = {}
        entry["wemID"] = read_uint(file)
        entry["unkn0"] = read_uint(file)
        entry["wemFileSize"] = read_uint(file)
        entry["wemOffset"] = read_uint(file)
        entry["langID"] = read_uint(file)
        MediaIndex["mediaIndexEntryList"].append(entry)
    return MediaIndex

def readUnknStruct(file,structLength):
    UnknStruct = {}
    UnknStruct["unknStructCount"] = read_uint(file)
    if UnknStruct["unknStructCount"] != 0:
        print("Reading Unknown Struct...")
    UnknStruct["unknStructIndexData"] = file.read(structLength-4)
    return UnknStruct
def readData(file,dataOffset):
    print("Reading Data...")
    file.seek(dataOffset+8)#Add 8 to account for header offset
    pData = bytearray(file.read())
    return pData
def readPCK(filepath):
    print(textColors.OKCYAN + "__________________________________\nPCK import started." + textColors.ENDC)
    print("Opening "+filepath)
    file = open(filepath,"rb")
    print("Reading PCK...")
    PCK = {}
    PCK["FileName"] = os.path.basename(filepath)#Get file name
    PCK["Header"] = readPCKHeader(file)
    PCK["Language"] = readPCKLanguages(file)
    PCK["BNKIndex"] = readPCKBNKIndex(file)
    PCK["MediaIndex"] = readPCKMediaIndex(file)
    PCK["UnknStruct"] = readUnknStruct(file,PCK["Header"]["unknStructLength"])
    PCK["Data"] = readData(file,PCK["Header"]["dataOffset"])
    print(textColors.OKGREEN + "__________________________________\nPCK import finished.\n" + textColors.ENDC)
    return PCK


#-----PCK extract functions-----#
def extractMedia(PCK,outputDir):#Extracts both WEMs and BNKs. It should be one or the other but both existing at the same time is accounted for just in case.
    dataOffset = PCK["Header"]["dataOffset"] +8#+8 to account for header
    WEMDict = readWEMNameList(os.path.join(os.getcwd(),"SoundNames_replicant.csv"))
    for language in PCK["Language"]["LangStringList"]:
        try:
            os.makedirs(os.path.join(outputDir,language))     
        except:
            pass
    print(textColors.OKCYAN + "__________________________________\nMedia extract started." + textColors.ENDC)       
    if PCK["BNKIndex"]["BNKIndexList"] != []:#Extract bnks if they exist
        
        print("Extracting BNKs...")
        for index, entry in enumerate(PCK["BNKIndex"]["BNKIndexList"]):
            #print("Extracting WEM "+str(index))
            if entry["bnkID"] in WEMDict:
                WEMName = WEMDict[entry["bnkID"]]+ "-"
            else:
                WEMName = ""
            file = open(os.path.join(outputDir,PCK["Language"]["LangIDDict"][entry["langID"]],str(index)+"-" + WEMName + str(entry["bnkID"])+".bnk"), "wb")#Index is included because bnks can share the same ID for different languages
            file.write(getByteSection(PCK["Data"],entry["bnkOffset"] - dataOffset,entry["bnkSize"]))
            file.close()
        
    if PCK["MediaIndex"]["mediaIndexEntryList"] != []:#Extract wems if they exist
        print("Extracting WEMs...")
        for index, entry in enumerate(PCK["MediaIndex"]["mediaIndexEntryList"]):
            #print("Extracting WEM "+str(index))
            if entry["wemID"] in WEMDict:
                WEMName = WEMDict[entry["wemID"]]+ "-"
            else:
                WEMName = ""
            file = open(os.path.join(outputDir,PCK["Language"]["LangIDDict"][entry["langID"]],WEMName + str(entry["wemID"])+".wem"), "wb")
            file.write(getByteSection(PCK["Data"],entry["wemOffset"] - dataOffset,entry["wemFileSize"]))
            file.close()
    print(textColors.OKGREEN + "__________________________________\nFinished extracting media to "+ outputDir + textColors.ENDC)
 
#-----PCK export functions-----#
def readNewWEMs(inputDir,mediaIndexEntryList):#Reads wems if their ID matches ones in pck
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
                for dict_ in [entry for entry in mediaIndexEntryList if entry["wemID"] == id]:#Check if wem ID of file is in bnk
                    print ("Reading new WEM: "+os.path.join(root,fileName))
                    file = open(os.path.join(root,fileName),"rb")
                    eof = os.fstat(file.fileno()).st_size
                    NewWEM = {}
                    NewWEM["id"] = id
                    NewWEM["data"] = file.read(eof)
                    file.close()
                    NewWEMList.append(NewWEM)           
    return NewWEMList

def readNewBNKs(inputDir,BNKIndexList,PCKLangIDDict):#Reads BNKs to repack into PCK
    NewBNKList = []
    BNKLangDict ={
        684519430:"english(us)",
        4224429355:"japanese(jp)",
        393239870:"sfx"
        }
    for root, dirs, filenames in os.walk(inputDir):
        for fileName in filenames:
            if fileName.endswith(".bnk"):
                print("Checking " + fileName + " for matching BNK entry...")
                file = open(os.path.join(root,fileName),"rb")
                NewBNK = {}
                file.seek(12)#Read only bnk ID and lang ID, if it matches entry in PCK, read the entire file
                NewBNK["id"] = read_uint(file)
                NewBNK["dwLanguageID"] = read_uint(file)#Reads language id to have something to compare against since bnks for each language have the same ID    
                #print("BNK ID: " + str(NewBNK["id"]))
                #print("BNK Language: " + BNKLangDict[NewBNK["dwLanguageID"]])
                NewBNK["index"] = next((i for i, entry in enumerate(BNKIndexList) if entry["bnkID"] == NewBNK["id"] and PCKLangIDDict[entry["langID"]] == BNKLangDict[NewBNK["dwLanguageID"]]), None)#Check that language and id of bnk match entry in PCK
                if NewBNK["index"] != None:
                    print ("Entry found, reading BNK...")
                    eof = os.fstat(file.fileno()).st_size
                    file.seek(0)
                    NewBNK["data"] = file.read(eof)
                    
                    
                    NewBNKList.append(NewBNK)
                file.close()
    return NewBNKList  
def updateWEMIndexOffsets(mediaIndexEntryList,offset,difference):
    for entry in mediaIndexEntryList:
        if entry["wemOffset"] > offset:
            entry["wemOffset"] += difference
    
def updateBNKIndexOffsets(BNKIndexList,offset,difference):
    for entry in BNKIndexList:
        if entry["bnkOffset"] > offset:
            entry["bnkOffset"] += difference
 

def writePCKHeader(file,Header):
    print("Writing PCK Header...")
    file.write(Header["FileType"])
    write_uint(file,Header["dataOffset"])
    write_uint(file,Header["unkn0"])
    write_uint(file,Header["languageLength"])
    write_uint(file,Header["bankIndexLength"])
    write_uint(file,Header["mediaIndexLength"])
    write_uint(file,Header["unknStructLength"])
def writePCKLanguages(file,Language):
    print("Writing PCK Languages...")
    write_uint(file,Language["languageCount"])
    for entry in Language["LangIndexList"]:
        write_uint(file,entry["languageOffset"])
        write_uint(file,entry["languageID"])
    for entry in Language["LangStringList"]:
        write_unicode_string(file,entry)
    file.write(Language["padding"])
def writePCKBNKIndex(file,BNKIndex):
    write_uint(file,BNKIndex["bnkCount"])
    if BNKIndex["bnkCount"] != 0:
        print("Writing Bank Index...")
    for entry in BNKIndex["BNKIndexList"]:
        write_uint(file,entry["bnkID"])
        write_uint(file,entry["unkn1"])
        write_uint(file,entry["bnkSize"])
        write_uint(file,entry["bnkOffset"])
        write_uint(file,entry["langID"])
def writePCKMediaIndex(file,MediaIndex):
    write_uint(file,MediaIndex["wemCount"])
    if MediaIndex["wemCount"] != 0:
        print("Writing Media Index...")
    for entry in MediaIndex["mediaIndexEntryList"]:
        write_uint(file,entry["wemID"])
        write_uint(file,entry["unkn0"])
        write_uint(file,entry["wemFileSize"])
        write_uint(file,entry["wemOffset"])
        write_uint(file,entry["langID"])

def writeUnknStruct(file,UnknStruct):
    write_uint(file,UnknStruct["unknStructCount"])
    if UnknStruct["unknStructCount"] != 0:
        print("Writing Unknown Struct...")
    file.write(UnknStruct["unknStructIndexData"])
def writeData(file,Data):
    print("Writing Data...")
    file.write(Data)
    
    
def repackPCK(PCK, inputDir):#Edits the currently imported PCK
    dataOffset = PCK["Header"]["dataOffset"] + 8
    if PCK["BNKIndex"]["BNKIndexList"] != []:
        NewBNKList = readNewBNKs(inputDir,PCK["BNKIndex"]["BNKIndexList"],PCK["Language"]["LangIDDict"])#Replaces via index since BNKs for different languages have the same ID
        if NewBNKList == []:
            raiseError("No replacement BNK files were in the repack directory.")
        
        for newBNK in NewBNKList:
            
            print("Replacing BNK " + str(newBNK["index"])+ " in PCK")
            currentEntry = PCK["BNKIndex"]["BNKIndexList"][newBNK["index"]]
            oldDataSize = len(PCK["Data"])
            removeByteSection(PCK["Data"],currentEntry["bnkOffset"]-dataOffset,currentEntry["bnkSize"])#Removes wem at offset
            insertByteSection(PCK["Data"],currentEntry["bnkOffset"]-dataOffset,newBNK["data"])#Inserts wem at offset
            newDataSize = len(PCK["Data"])
            sizeDifference = newDataSize - oldDataSize
            print ("BNK "+ str(newBNK["id"])+" size difference: "+str(sizeDifference))
            currentEntry["bnkSize"] = len(newBNK["data"])
            updateBNKIndexOffsets(PCK["BNKIndex"]["BNKIndexList"],currentEntry["bnkOffset"],sizeDifference)#Updates offsets by checking each entry, offsets can be out of order so can't blindly increase
    
    if PCK["MediaIndex"]["mediaIndexEntryList"] != []:
        NewWEMList = readNewWEMs(inputDir,PCK["MediaIndex"]["mediaIndexEntryList"])#Passes list of wems in PCK
        if NewWEMList == []:
            raiseError("No replacement WEM files were found in the repack directory.")
        wemIDDict = createIndexDict(PCK["MediaIndex"]["mediaIndexEntryList"], "wemID")
        for WEM in NewWEMList:   
            print("Replacing WEM " + str(WEM["id"])+ " in PCK")
            wemIndex = wemIDDict.get(WEM["id"])
            entry = PCK["MediaIndex"]["mediaIndexEntryList"][wemIndex]
            oldDataSize = len(PCK["Data"])
            #print("Removing "+str(entry["wemFileSize"])+" at: "+str(entry["wemOffset"]-dataOffset) +" Inserting "+ str(len(WEM["data"])))
            removeByteSection(PCK["Data"],entry["wemOffset"]-dataOffset,entry["wemFileSize"])#Removes wem at offset
            insertByteSection(PCK["Data"],entry["wemOffset"]-dataOffset,WEM["data"])#Inserts wem at offset
            newDataSize = len(PCK["Data"])
            sizeDifference = newDataSize - oldDataSize
            print ("WEM "+ str(WEM["id"])+" size difference: "+str(sizeDifference))
            entry["wemFileSize"] = len(WEM["data"])
            updateWEMIndexOffsets(PCK["MediaIndex"]["mediaIndexEntryList"],entry["wemOffset"],sizeDifference)#Updates offsets by checking each entry, offsets can be out of order so can't blindly increase
            
def writePCK(PCK,exportDir):
    print(textColors.OKCYAN + "__________________________________\nPCK export started." + textColors.ENDC)
    try:
            os.makedirs(exportDir)     
    except:
        pass
    file = open(os.path.join(exportDir,PCK["FileName"]), "wb")
    writePCKHeader(file,PCK["Header"])
    writePCKLanguages(file,PCK["Language"])
    writePCKBNKIndex(file,PCK["BNKIndex"])
    writePCKMediaIndex(file,PCK["MediaIndex"])
    writeUnknStruct(file,PCK["UnknStruct"])
    print("Writing Data...")
    file.write(PCK["Data"])
    file.close()
    print(textColors.OKGREEN + "__________________________________\nPCK export finished.\n" + textColors.ENDC)
    
#-----PCK file functions-----#
def extractPCKFile(SOURCEFILE,OUTPUTDIR):
    PCK = readPCK(SOURCEFILE)
    extractMedia(PCK,OUTPUTDIR)
    
def repackPCKFile(SOURCEFILE,INPUTDIR,EXPORTDIR):
    PCK = readPCK(SOURCEFILE)
    print(textColors.OKCYAN + "__________________________________\nRepacking PCK." + textColors.ENDC)
    repackPCK(PCK,INPUTDIR)
    writePCK(PCK,EXPORTDIR)
    print(textColors.OKGREEN + "__________________________________\nSaved PCK to " +EXPORTDIR + textColors.ENDC)