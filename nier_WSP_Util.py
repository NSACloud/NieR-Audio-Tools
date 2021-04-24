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
     
#-----WSP import functions-----#
def readWSP(filepath):
    print(textColors.OKCYAN + "__________________________________\nWSP import started." + textColors.ENDC)
    print("Opening "+filepath)
    file = open(filepath,"rb")
    print("Reading WSP...")
    WSP = {}
    WSP["FileType"] = file.read(4)
     
    if WSP["FileType"] != b'RIFF':
         raiseError("File is not a WSP file.")
    file.seek(0)
    WSP["FileName"] = os.path.basename(filepath)#Get file name
    WSP["EOF"] = os.fstat(file.fileno()).st_size#Get file size
    WSP["WEMList"] = []
    while file.tell() != WSP["EOF"]:
        WSP["WEMList"].append(readWEM(file,WSP["EOF"]))
    print(textColors.OKGREEN + "__________________________________\nWSP import finished.\n" + textColors.ENDC)
    return WSP
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


#-----WSP extract functions-----#
def extractWEMs(WSP,outputDir):   
    for index, wem in enumerate(WSP["WEMList"]):
        print("Extracting WEM "+str(index))
        file = open(outputDir+"\\"+str(index)+".wem", "wb")
        file.write(b"RIFF")
        write_uint(file, WSP["WEMList"][index]["fileSize"])
        file.write(WSP["WEMList"][index]["data"])
        file.write(WSP["WEMList"][index]["padding"])
        file.close()
        
#-----WSP export functions-----#
def readNewWEMs(inputDir,wemCount):#Reads wems to repack into WSP
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
                    raiseError("WEM index exceeds the amount of WEMs in the WSP. \nCheck that you're repacking to the correct file.")
                NewWEMList.append(NewWEM)
        break
    return NewWEMList
    
def repackWSP(WSP, inputDir,exportDir):#Edits the currently imported WSP
    wemCount = len(WSP["WEMList"])
    NewWEMList = readNewWEMs(inputDir,wemCount)
    if NewWEMList == []:
        raiseError("No WEM files were in the repack directory.")
    for WEM in NewWEMList:
        WSP["WEMList"][WEM["Index"]] = WEM#Replace each WEM in the WSP with the ones from the repack directory.
        print("Replacing WEM " + str(WEM["Index"])+ " in WSP") 
    file = open(os.path.join(exportDir,WSP["FileName"]), "wb")
    for index, wem in enumerate(WSP["WEMList"]):    
        file.write(b"RIFF")
        write_uint(file, WSP["WEMList"][index]["fileSize"])
        file.write(WSP["WEMList"][index]["data"])
        file.write(WSP["WEMList"][index]["padding"])
        file.seek(file.tell()+getPaddingAmount(file.tell(),16))#Pad for alignment
    file.close()
#-----WSP file functions-----#
def extractWSPFile(SOURCEFILE,OUTPUTDIR):
    WSP = readWSP(SOURCEFILE)
    print(textColors.OKCYAN + "__________________________________\nExtracting WEMs." + textColors.ENDC)
    extractWEMs(WSP,OUTPUTDIR)
    print(textColors.OKGREEN + "__________________________________\nFinished extracting WEMs to "+ OUTPUTDIR + textColors.ENDC)

def repackWSPFile(SOURCEFILE,INPUTDIR,EXPORTDIR):
    WSP = readWSP(SOURCEFILE)
    print(textColors.OKCYAN + "__________________________________\nRepacking WSP." + textColors.ENDC)
    repackWSP(WSP,INPUTDIR,EXPORTDIR)
    print(textColors.OKGREEN + "__________________________________\nSaved WSP to " +EXPORTDIR + textColors.ENDC)
#-----MAIN-----#

def displayHelp():
    print ("Usage: nier_WSP_Util.py <WSP Path> <OPTIONS>\n")
    print("By default, the WSP provided will be unpacked unless -r is specified.")
    print ("You can also drag a WSP file onto nier_WSP_Util.py to extract it.\n")
    print ("Available options:")
    print("_________________________________")
    print(textColors.OKGREEN +"-e <Extract Directory>"+ textColors.ENDC)
    print("Extract WEMs from the WSP to the directory provided.")
    print("_________________________________")
    print (textColors.OKGREEN +"-r <Repack Directory>"+ textColors.ENDC)
    print("Repack the WSP with WEMs at the directory provided.")
    print(textColors.WARNING + "NOTE: Experimental. Repacking will not work if the WEMs are missing data that the game requires. WEM file sizes might be defined in data\sound\WWiseStreamInfo.wai."+ textColors.ENDC)
    print("_________________________________")
    print (textColors.OKGREEN +"-x <Export Directory>"+ textColors.ENDC)
    print("Export the repacked WSP to the directory provided. The repack directory (-r) option must be used.")
    print("\nWEM files can be played and converted to other formats using foobar2000 with the vgmstream plugin.")
    print("https://www.foobar2000.org/download\nhttps://www.foobar2000.org/components/view/foo_input_vgmstream")
    print("")

print(textColors.BOLD + "__________________________________\nNieR Automata WSP Utility V1" + textColors.ENDC)
print("https://github.com/NSACloud/NieR-Audio-Tools\n")

#Defaults
SOURCEFILE = None#WSP Location
INPUTDIR = None#WSP WEMs to repack
OUTPUTDIR = None#WSP Extract Location
EXPORTDIR = None#WSP Export Location
OPERATION = None

argumentList = sys.argv[2:]

# Options
options = "he:r:x:"
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options)
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1])and os.path.isfile(sys.argv[1]) and sys.argv[1].endswith(".wsp"):#Check that at least a file path has been given  
        #Set default options
        SOURCEFILE = sys.argv[1]
        OUTPUTDIR = os.path.join(os.path.split(SOURCEFILE)[0],os.path.split(os.path.splitext(SOURCEFILE)[0])[1]+"_extract")#sets default wem extract dir
        OPERATION = "unpack"
        # checking each argument
        for currentArgument, currentValue in arguments:
            
            if currentArgument in ("-h"):
                displayHelp()
                 
            elif currentArgument in ("-r"):
                print (("Repacking WSP:(% s)") % (currentValue))
                if os.path.exists(currentValue) and os.path.isdir(currentValue):
                    INPUTDIR = currentValue
                    EXPORTDIR = os.path.join(INPUTDIR,"export")#sets default repacked wsp export dir
                    OPERATION = "repack"
                else:
                    raiseError("Invalid repack path.")
                        
            elif currentArgument in ("-e"):
                OUTPUTDIR = currentValue
            elif currentArgument in ("-x"):
                EXPORTDIR = currentValue
    else:
        displayHelp()
        input("\n"+textColors.FAIL + "ERROR: No WSP file provided. Press enter to exit." + textColors.ENDC)
        exit()
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

if OPERATION == "unpack":
    try:
        os.makedirs(OUTPUTDIR)
    except:
        pass
    extractWSPFile(SOURCEFILE,OUTPUTDIR)
elif OPERATION == "repack":
    try:
        os.makedirs(EXPORTDIR)
    except:
        pass
    repackWSPFile(SOURCEFILE,INPUTDIR,EXPORTDIR)