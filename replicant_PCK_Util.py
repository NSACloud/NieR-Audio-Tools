#Author: NSA Cloud

import os
import io
import struct
import getopt
import sys


#-----General Functions-----#
os.system("color")#Enable console colors
class textColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'     
# read unsigned byte from file
def read_byte(file_object, endian = '<'):
     data = struct.unpack(endian+'B', file_object.read(1))[0]
     return data

 # read signed short from file
def read_short(file_object, endian = '<'):
     data = struct.unpack(endian+'h', file_object.read(2))[0]
     return data
  # read unsigned short from file
def read_ushort(file_object, endian = '<'):
     data = struct.unpack(endian+'H', file_object.read(2))[0]
     return data

 # read unsigned integer from file
def read_uint(file_object, endian = '<'):
     data = struct.unpack(endian+'I', file_object.read(4))[0]
     return data

 # read signed integer from file
def read_int(file_object, endian = '<'):
     data = struct.unpack(endian+'i', file_object.read(4))[0]
     return data

 # read floating point number from file
def read_float(file_object, endian = '<'):
     data = struct.unpack(endian+'f', file_object.read(4))[0]
     return data
 #read null terminated string from file
def read_string(file_object, endian = '<'):
     data =''.join(iter(lambda: file_object.read(1).decode('ascii'), '\x00'))
     return data

# write unsigned byte to file
def write_byte(file_object,input, endian = '<'):
     data = struct.pack(endian+'B', input)
     file_object.write(data)

 # write signed short to file
def write_short(file_object,input, endian = '<'):
     data = struct.pack(endian+'h', input)
     file_object.write(data)
     
 # write unsigned short to file
def write_ushort(file_object,input, endian = '<'):
     data = struct.pack(endian+'H', input)
     file_object.write(data)

 # write unsigned integer to file
def write_uint(file_object,input, endian = '<'):
     data = struct.pack(endian+'I', input)
     file_object.write(data)


 # write signed integer to file
def write_int(file_object,input, endian = '<'):
     data = struct.pack(endian+'i', input)
     file_object.write(data)

 # write floating point number to file
def write_float(file_object,input, endian = '<'):
     data = struct.pack(endian+'f', input)
     file_object.write(data)
 #write null terminated string to file
def write_string(file_object,input):
     input += '\x00'
     data = bytes(input, 'utf-8')
     file_object.write(data)
def getPaddingAmount(currentPos,alignment):
    padding = (currentPos*-1)%alignment
    return padding
def raiseError(error):
     raise Exception(textColors.FAIL + "ERROR: " + error + textColors.ENDC)

def raiseWarning(warning):
     print(textColors.WARNING + "WARNING: " + warning + textColors.ENDC)
def readPCKHeader(file):
    Header = {}
    Header["FileType"] = file.read(4)
     
    if Header["FileType"] != b'AKPK':
         raiseError("File is not a PCK file.")
    Header["wemDataOffset"] = read_uint(file)
    Header["unkn0"] = read_uint(file)
    Header["unkn1"] = read_uint(file)
    Header["unkn2"] = read_uint(file)
    Header["mediaIndexLength"] = read_uint(file)
    Header["unkn3"] = read_uint(file)
    Header["unkn4"] = read_uint(file)
    Header["unkn5"] = read_uint(file)
    Header["unkn6"] = read_uint(file)
    Header["unkn7"] = read_uint(file)
    Header["unkn8"] = read_uint(file)
    Header["unkn9"] = read_uint(file)
    Header["null0"] = file.read(3)
    Header["soundDirs"] = file.read(59)#These directories shouldn't change
    Header["null1"] = file.read(2)
    Header["bnkCount"] = read_uint(file)
    print(Header)
    return Header
def readPCKMediaIndex(file):
    MediaIndex = {}
    MediaIndex["wemCount"] = read_uint(file)
    mediaIndexEntryList = []
    for i in range(0,MediaIndex["wemCount"]):
        entry = {}
        entry["wemID"] = read_uint(file)
        entry["unkn0"] = read_uint(file)
        entry["wemFileSize"] = read_uint(file)
        entry["wemOffset"] = read_uint(file)
        entry["unkn1"] = read_uint(file)
        mediaIndexEntryList.append(entry)
    MediaIndex["mediaIndexEntryList"] = mediaIndexEntryList
    MediaIndex["null"] = file.read(4)
    return MediaIndex
    
def readPCKBNKIndex(file,bnkCount):
    bnkIndex = {}
    bnkIndexList = []
    for i in range(0,bnkCount):
        entry = {}
        entry["unkn0"] = read_uint(file)
        entry["unkn1"] = read_uint(file)
        entry["bnkSize"] = read_uint(file)
        entry["bnkOffset"] = read_uint(file)
        entry["unkn4"] = read_uint(file)
        bnkIndexList.append(entry)
    bnkIndex["bnkIndexList"]= bnkIndexList
    bnkIndex["null"] = file.read(8)
    return bnkIndex
#-----PCK import functions-----#
def readPCK(filepath):
    print(textColors.OKCYAN + "__________________________________\nPCK import started." + textColors.ENDC)
    print("Opening "+filepath)
    file = open(filepath,"rb")
    print("Reading PCK...")
    PCK = {}
    PCK["FileName"] = os.path.basename(filepath)#Get file name
    PCK["EOF"] = os.fstat(file.fileno()).st_size#Get file size
    PCK["MediaIndex"] = None#Set default value in the case that PCK doesn't have media index
    PCK["WEMList"] = None#Set default value in the case that PCK doesn't have media index
    PCK["BNKList"] = None#Set default value in the case that PCK doesn't have bnk index
    PCK["Header"] = readPCKHeader(file)
    if PCK["Header"]["bnkCount"] != 0:
        PCK["BNKList"] = []
        PCK["BNKIndex"] = readPCKBNKIndex(file, PCK["Header"]["bnkCount"])
        for i in range(0,PCK["Header"]["bnkCount"]):
            file.seek(PCK["BNKIndex"]["bnkIndexList"][i]["bnkOffset"])
            PCK["BNKList"].append(readBNK(file,PCK["BNKIndex"]["bnkIndexList"][i]["bnkSize"]))
    else:
        PCK["MediaIndex"] = readPCKMediaIndex(file)
        PCK["WEMList"] = []
        for i in range(0,PCK["MediaIndex"]["wemCount"]):
            PCK["WEMList"].append(readWEM(file,PCK["EOF"]))
    print(textColors.OKGREEN + "__________________________________\nPCK import finished.\n" + textColors.ENDC)
    return PCK
def readBNK(file,eof):
    BNK = {}
    BNK["FileType"] = file.read(4)
    if BNK["FileType"] != b'BKHD':
        raiseError("Failed during reading BNK.")
    file.seek(file.tell()-4)
    BNK["data"] = file.read(eof)#Might change this to fully parse bnk at some point
    return BNK
def readWEM(file,eof):#Returns WEM as a dictionary
    print("Current Pos: "+ str(file.tell()))
    print("Reading WEM...")
    WEM = {}
    
    WEM["FileType"] = file.read(4)
    if WEM["FileType"] != b'RIFF':
        raiseError("Failed during reading WEM.")
   
    WEM["fileSize"] = read_uint(file)
    WEM["data"] = file.read(WEM["fileSize"])
    WEM["padding"] = file.read(getWEMPadding(file,eof))
    return WEM

def getWEMPadding(file, eof):
    print("Reading WEM padding...")
    if file.tell() == eof:
            return 0;
    startPos = file.tell()
    paddingSize = 0
    while read_byte(file) == 0:
        paddingSize += 1
        if file.tell() == eof:
            break;
    file.seek(startPos)
    print("Padding Amount: " + str(paddingSize))
    return paddingSize       


#-----PCK extract functions-----#
def extractWEMs(PCK,outputDir):   
    for index, wem in enumerate(PCK["WEMList"]):
        print("Extracting WEM "+str(index))
        file = open(outputDir+"\\"+str(index)+"-"+str(PCK["MediaIndex"]["mediaIndexEntryList"][index]["wemID"])+".wem", "wb")
        file.write(b"RIFF")
        write_uint(file, PCK["WEMList"][index]["fileSize"])
        file.write(PCK["WEMList"][index]["data"])
        file.write(PCK["WEMList"][index]["padding"])
        file.close()

def extractBNKs(PCK,outputDir):   
    for index, wem in enumerate(PCK["BNKList"]):
        print("Extracting BNK "+str(index))
        file = open(outputDir+"\\"+str(index)+".bnk", "wb")
        file.write(PCK["BNKList"][index]["data"])
        file.close()        
#-----PCK export functions-----#
def readNewWEMs(inputDir,wemCount):#Reads wems to repack into PCK
    NewWEMList = []
    for root, dirs, filenames in os.walk(inputDir):
        for fileName in filenames:
            if fileName.endswith(".wem"):           
                print ("Reading new WEM: "+os.path.join(root,fileName))
                file = open(os.path.join(root,fileName),"rb")
                eof = os.fstat(file.fileno()).st_size
                NewWEM = readWEM(file,eof)            
                file.close()
                NewWEM["Index"] = int((os.path.splitext(fileName)[0]).split('-')[0])#Splits index from WEM ID and extension
                if NewWEM["Index"] > wemCount:
                    raiseError("WEM index exceeds the amount of WEMs in the PCK. \nCheck that you're repacking to the correct file.")
                NewWEMList.append(NewWEM)
        break
    return NewWEMList

def readNewBNKs(inputDir,bnkCount):#Reads wems to repack into PCK
    NewBNKList = []
    for root, dirs, filenames in os.walk(inputDir):
        for fileName in filenames:
            if fileName.endswith(".bnk"):           
                print ("Reading new BNK: "+os.path.join(root,fileName))
                file = open(os.path.join(root,fileName),"rb")
                eof = os.fstat(file.fileno()).st_size
                NewBNK = readBNK(file,eof)            
                file.close()
                NewBNK["Index"] = int((os.path.splitext(fileName)[0]).split('-')[0])#Splits index from BNK ID and extension
                NewBNK["fileSize"] = eof
                if NewBNK["Index"] > bnkCount:
                    raiseError("BNK index exceeds the amount of BNKs in the PCK. \nCheck that you're repacking to the correct file.")
                NewBNKList.append(NewBNK)
        break
    return NewBNKList  
def updateWEMIndexOffsets(mediaIndexEntryList,offset,difference):
    for entry in mediaIndexEntryList:
        if entry["wemOffset"] > offset:
            entry["wemOffset"] += difference
    return mediaIndexEntryList    
def updateBNKIndexOffsets(bnkIndexList,offset,difference):
    for entry in bnkIndexList:
        if entry["bnkOffset"] > offset:
            entry["bnkOffset"] += difference
    return bnkIndexList
def writePCKHeader(file,PCKHEADER):
    file.write(b"AKPK")
    write_uint(file,PCKHEADER["wemDataOffset"])
    write_uint(file,PCKHEADER["unkn0"])
    write_uint(file,PCKHEADER["unkn1"])
    write_uint(file,PCKHEADER["unkn2"])
    write_uint(file,PCKHEADER["mediaIndexLength"])
    write_uint(file,PCKHEADER["unkn3"])
    write_uint(file,PCKHEADER["unkn4"])
    write_uint(file,PCKHEADER["unkn5"])
    write_uint(file,PCKHEADER["unkn6"])
    write_uint(file,PCKHEADER["unkn7"])
    write_uint(file,PCKHEADER["unkn8"])
    write_uint(file,PCKHEADER["unkn9"])
    file.write(PCKHEADER["null0"])
    file.write(PCKHEADER["soundDirs"])
    file.write(PCKHEADER["null1"])
    write_uint(file,PCKHEADER["bnkCount"])
def repackPCK(PCK, inputDir,exportDir):#Edits the currently imported PCK
    if PCK["Header"]["bnkCount"] != 0:
        NewBNKList = readNewBNKs(inputDir,PCK["Header"]["bnkCount"])
        if NewBNKList == []:
            raiseError("No BNK files were in the repack directory.")
        for BNK in NewBNKList:
            print("Replacing BNK " + str(BNK["Index"])+ " in PCK")
            PCK["BNKList"][BNK["Index"]] = BNK#Replace each BNK in the PCK with the ones from the repack directory.
            size_difference = BNK["fileSize"] - PCK["BNKIndex"]["bnkIndexList"][BNK["Index"]]["bnkSize"]
            print ("BNK "+ str(BNK["Index"])+" size difference: "+str(size_difference))
            PCK["BNKIndex"]["bnkIndexList"][BNK["Index"]]["bnkSize"] = BNK["fileSize"]
            PCK["BNKIndex"]["bnkIndexList"] = updateBNKIndexOffsets(PCK["BNKIndex"]["bnkIndexList"],PCK["BNKIndex"]["bnkIndexList"][BNK["Index"]]["bnkOffset"],size_difference)
        file = open(os.path.join(exportDir,PCK["FileName"]), "wb")
        writePCKHeader(file,PCK["Header"])
        for entry in PCK["BNKIndex"]["bnkIndexList"]:
            write_uint(file,entry["unkn0"])
            write_uint(file,entry["unkn1"])
            write_uint(file,entry["bnkSize"])
            write_uint(file,entry["bnkOffset"])
            write_uint(file,entry["unkn4"])
        file.write(PCK["BNKIndex"]["null"])
        for index, entry in enumerate(PCK["BNKIndex"]["bnkIndexList"]):    
            file.seek(entry["bnkOffset"])
            file.write(PCK["BNKList"][index]["data"])
        file.close()
    else:
        NewWEMList = readNewWEMs(inputDir,PCK["MediaIndex"]["wemCount"])
        if NewWEMList == []:
            raiseError("No WEM files were in the repack directory.")
        for WEM in NewWEMList:
            print("Replacing WEM " + str(WEM["Index"])+ " in PCK")
            PCK["WEMList"][WEM["Index"]] = WEM#Replace each WEM in the PCK with the ones from the repack directory.
            size_difference = WEM["fileSize"] - PCK["MediaIndex"]["mediaIndexEntryList"][WEM["Index"]]["wemFileSize"]+8#+8 to account for wem header
            print ("WEM "+ str(WEM["Index"])+" size difference: "+str(size_difference))#NOTE: Uses WEM's reported size
            PCK["MediaIndex"]["mediaIndexEntryList"][WEM["Index"]]["wemFileSize"] = WEM["fileSize"]+8
            PCK["MediaIndex"]["mediaIndexEntryList"] = updateWEMIndexOffsets(PCK["MediaIndex"]["mediaIndexEntryList"],PCK["MediaIndex"]["mediaIndexEntryList"][WEM["Index"]]["wemOffset"],size_difference)
            
        file = open(os.path.join(exportDir,PCK["FileName"]), "wb")
        writePCKHeader(file,PCK["Header"])
        write_uint(file,PCK["MediaIndex"]["wemCount"])
        for entry in PCK["MediaIndex"]["mediaIndexEntryList"]:
            write_uint(file,entry["wemID"])
            write_uint(file,entry["unkn0"])
            write_uint(file,entry["wemFileSize"])
            write_uint(file,entry["wemOffset"])
            write_uint(file,entry["unkn1"])
        file.write(PCK["MediaIndex"]["null"])
        for index, entry in enumerate(PCK["MediaIndex"]["mediaIndexEntryList"]):    
            file.seek(entry["wemOffset"])
            file.write(b"RIFF")           
            write_uint(file,PCK["WEMList"][index]["fileSize"])
            file.write(PCK["WEMList"][index]["data"])
        file.close()
#-----PCK file functions-----#
def extractPCKFile(SOURCEFILE,OUTPUTDIR):
    PCK = readPCK(SOURCEFILE)
    if PCK["Header"]["bnkCount"] != 0:
        print(textColors.OKCYAN + "__________________________________\nExtracting BNKs." + textColors.ENDC)
        extractBNKs(PCK,OUTPUTDIR)
        print(textColors.OKGREEN + "__________________________________\nFinished extracting BNKs to "+ OUTPUTDIR + textColors.ENDC)
        
    else:
        print(textColors.OKCYAN + "__________________________________\nExtracting WEMs." + textColors.ENDC)
        extractWEMs(PCK,OUTPUTDIR)
        print(textColors.OKGREEN + "__________________________________\nFinished extracting WEMs to "+ OUTPUTDIR + textColors.ENDC)

def repackPCKFile(SOURCEFILE,INPUTDIR,EXPORTDIR):
    PCK = readPCK(SOURCEFILE)
    print(textColors.OKCYAN + "__________________________________\nRepacking PCK." + textColors.ENDC)
    repackPCK(PCK,INPUTDIR,EXPORTDIR)
    print(textColors.OKGREEN + "__________________________________\nSaved PCK to " +EXPORTDIR + textColors.ENDC)
#-----MAIN-----#

def displayHelp():
    print ("Usage: nier_PCK_Util.py <PCK Path> <OPTIONS>\n")
    print("By default, the PCK provided will be unpacked unless -r is specified.")
    print ("You can also drag a PCK file onto nier_PCK_Util.py to extract it.\n")
    print ("Available options:")
    print("_________________________________")
    print(textColors.OKGREEN +"-e <Extract Directory>"+ textColors.ENDC)
    print("Extract WEMs or BNKs from the PCK to the directory provided.")
    print("_________________________________")
    print (textColors.OKGREEN +"-r <Repack Directory>"+ textColors.ENDC)
    print("Repack the PCK with WEMs or BNKs at the directory provided.")
    print(textColors.WARNING + "NOTE: Experimental. Repacking will not work if the WEMs are missing data that the game requires."+ textColors.ENDC)
    print("_________________________________")
    print (textColors.OKGREEN +"-x <Export Directory>"+ textColors.ENDC)
    print("Export the repacked PCK to the directory provided. The repack directory (-r) option must be used.")
    print("\nWEM files can be played and converted to other formats using foobar2000 with the vgmstream plugin.")
    print("https://www.foobar2000.org/download\nhttps://www.foobar2000.org/components/view/foo_input_vgmstream")

print(textColors.BOLD + "__________________________________\nNieR Replicant PCK Utility V1" + textColors.ENDC)
print("https://github.com/NSACloud/NieR-Audio-Tools\n")

#Defaults
SOURCEFILE = None#PCK Location
INPUTDIR = None#PCK WEMs to repack
OUTPUTDIR = None#PCK Extract Location
EXPORTDIR = None#PCK Export Location
OPERATION = None

argumentList = sys.argv[2:]

# Options
options = "he:r:x:"
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options)
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1])and os.path.isfile(sys.argv[1]) and sys.argv[1].endswith(".pck"):#Check that at least a file path has been given  
        #Set default options
        SOURCEFILE = sys.argv[1]
        OUTPUTDIR = os.path.join(os.path.split(SOURCEFILE)[0],os.path.split(os.path.splitext(SOURCEFILE)[0])[1]+"_extract")#sets default wem extract dir
        OPERATION = "unpack"
        # checking each argument
        for currentArgument, currentValue in arguments:
            
            if currentArgument in ("-h"):
                displayHelp()
                 
            elif currentArgument in ("-r"):
                print (("Repacking PCK:(% s)") % (currentValue))
                if os.path.exists(currentValue) and os.path.isdir(currentValue):
                    INPUTDIR = currentValue
                    EXPORTDIR = os.path.join(INPUTDIR,"export")#sets default repacked PCK export dir
                    OPERATION = "repack"
                else:
                    raiseError("Invalid repack path.")
                        
            elif currentArgument in ("-e"):
                OUTPUTDIR = currentValue
            elif currentArgument in ("-x"):
                EXPORTDIR = currentValue
    else:
        displayHelp()
        input("\n"+textColors.FAIL + "ERROR: No PCK file provided. Press enter to exit." + textColors.ENDC)
        exit()
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

if OPERATION == "unpack":
    try:
        os.makedirs(OUTPUTDIR)
    except:
        pass
    extractPCKFile(SOURCEFILE,OUTPUTDIR)
elif OPERATION == "repack":
    try:
        os.makedirs(EXPORTDIR)
    except:
        pass
    repackPCKFile(SOURCEFILE,INPUTDIR,EXPORTDIR)