#Author: NSA Cloud

#V3

#Changes in V3:

#Rewritten PCK structure to be faster and more accurate
#BNKs now extract with names
#Repacking is now done via ID instead of index.
#Removed index numbers from WEMs and moved WEM ID to end of file name
#Performance improvements - stream.pck extract time from ~15 seconds to ~4.5 seconds

#NOTE: If you are updating from V1 or V2, you cannot repack with WEMs extracted from those versions.
#Run "update_OLD_WEMNames_replicant.py" on the repack directory to fix the old file names and to be able to use them

#Changes in V2:

#Wwise event IDs are now appended to wems with known events
#Extraction is separated by language folders
#Reduced printing for faster extraction
#Repacking now searches all subdirectories

#This is not intended to be the most efficiently written program. There are many things that could be done better.
#All audio tools will be rewritten and incorporated into a single tool at some point.
import time
start_time = time.time()
import os
import getopt
import sys

from modules.pck import extractPCKFile,repackPCKFile
from modules.gen_functions import textColors,raiseError
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


#-----MAIN-----#

def displayHelp():
    print ("Usage: replicant_PCK_Util.py <PCK Path> <OPTIONS>\n")
    print("By default, the PCK provided will be unpacked unless -r is specified.")
    print ("You can also drag a PCK file onto replicant_PCK_Util.py to extract it.\n")
    print ("Available options:")
    print("_________________________________")
    print(textColors.OKGREEN +"-e <Extract Directory>"+ textColors.ENDC)
    print("Extract WEMs or BNKs from the PCK to the directory provided.")
    print("_________________________________")
    print (textColors.OKGREEN +"-r <Repack Directory>"+ textColors.ENDC)
    print("Repack the PCK with WEMs or BNKs at the directory provided. Reads all subdirectories.")
    print("_________________________________")
    print (textColors.OKGREEN +"-x <Export Directory>"+ textColors.ENDC)
    print("Export the repacked PCK to the directory provided. The repack directory (-r) option must be used.")
    print("\nWEM files can be played and converted to other formats using foobar2000 with the vgmstream plugin.")
    print("https://www.foobar2000.org/download\nhttps://www.foobar2000.org/components/view/foo_input_vgmstream")

print(textColors.BOLD + "__________________________________\nNieR Replicant PCK Utility V3" + textColors.ENDC)
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
    extractPCKFile(SOURCEFILE,OUTPUTDIR)
elif OPERATION == "repack":
    repackPCKFile(SOURCEFILE,INPUTDIR,EXPORTDIR)
print("Execution Time: %.2f seconds" % (time.time() - start_time))