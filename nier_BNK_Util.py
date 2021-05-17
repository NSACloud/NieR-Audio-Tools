#Author: NSA Cloud

#This is not intended to be the most efficiently written program. There are many things that could be done better.
#All audio tools will be rewritten and incorporated into a single tool at some point.
import os
import io
import getopt
import sys

from modules.bnk import extractBNKFile,repackBNKFile
from modules.gen_functions import textColors,raiseError
from modules.gamesupport import checkBNKExtension

#-----MAIN-----#

def displayHelp():
    print ("Usage: nier_BNK_Util.py <BNK Path> <OPTIONS>\n")
    print("By default, the BNK provided will be unpacked unless -r is specified.")
    print ("You can also drag a BNK file onto nier_BNK_Util.py to extract it.\n")
    print ("Compatible with NieR Replicant, NieR Automata and probably any other games that use BNK.\n")
    print ("Available options:")
    print("_________________________________")
    print(textColors.OKGREEN +"-e <Extract Directory>"+ textColors.ENDC)
    print("Extract WEMs from the BNK to the directory provided.")
    print("_________________________________")
    print (textColors.OKGREEN +"-r <Repack Directory>"+ textColors.ENDC)
    print("Repack the BNK with WEMs at the directory provided. Reads all subdirectories.")
    print("_________________________________")
    print (textColors.OKGREEN +"-x <Export Directory>"+ textColors.ENDC)
    print("Export the repacked BNK to the directory provided. The repack directory (-r) option must be used.")
    print("\nWEM files can be played and converted to other formats using foobar2000 with the vgmstream plugin.")
    print("https://www.foobar2000.org/download\nhttps://www.foobar2000.org/components/view/foo_input_vgmstream")

print(textColors.BOLD + "__________________________________\nNieR BNK Utility V1" + textColors.ENDC)
print("https://github.com/NSACloud/NieR-Audio-Tools\n")

#Defaults
SOURCEFILE = None#BNK Location
INPUTDIR = None#BNK WEMs to repack
OUTPUTDIR = None#BNK Extract Location
EXPORTDIR = None#BNK Export Location
OPERATION = None

argumentList = sys.argv[2:]

# Options
options = "he:r:x:"
try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options)
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1])and os.path.isfile(sys.argv[1]) and checkBNKExtension(os.path.splitext(sys.argv[1])[1]):#Check that at least a file path has been given  
        #Set default options
        SOURCEFILE = sys.argv[1]
        OUTPUTDIR = os.path.join(os.path.split(SOURCEFILE)[0],os.path.split(os.path.splitext(SOURCEFILE)[0])[1]+"_extract")#sets default wem extract dir
        OPERATION = "unpack"
        # checking each argument
        for currentArgument, currentValue in arguments:
            
            if currentArgument in ("-h"):
                displayHelp()
                 
            elif currentArgument in ("-r"):
                print (("Repacking BNK:(% s)") % (currentValue))
                if os.path.exists(currentValue) and os.path.isdir(currentValue):
                    INPUTDIR = currentValue
                    EXPORTDIR = os.path.join(INPUTDIR,"export")#sets default repacked BNK export dir
                    OPERATION = "repack"
                else:
                    raiseError("Invalid repack path.")
                        
            elif currentArgument in ("-e"):
                OUTPUTDIR = currentValue
            elif currentArgument in ("-x"):
                EXPORTDIR = currentValue
    else:
        displayHelp()
        input("\n"+textColors.FAIL + "ERROR: No BNK file provided. Press enter to exit." + textColors.ENDC)
        exit()
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))


    
if OPERATION == "unpack":
    extractBNKFile(SOURCEFILE,OUTPUTDIR)
elif OPERATION == "repack":
    repackBNKFile(SOURCEFILE,INPUTDIR,EXPORTDIR)