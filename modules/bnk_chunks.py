#Author: NSA Cloud
from .gen_functions import read_uint,read_ushort,read_ubyte,write_uint,write_ushort,write_ubyte,raiseWarning

#TODO: Rewrite this

#Credit to bnnm for mapping BNK structure
#---Read Functions---#

def readBKHD(file):#Bank Header
    print("Reading Bank Header...")
    BKHD = {}
    BKHD["dwTag"] = "BKHD"
    BKHD["dwChunkSize"] = read_uint(file)
    BKHD["dwBankGeneratorVersion"] = read_uint(file)
    BKHD["dwSoundBankID"] = read_uint(file)
    BKHD["dwLanguageID"] = read_uint(file)
    BKHD["bUnused"] = read_ushort(file)
    BKHD["bDeviceAllocated"] = read_ushort(file)
    BKHD["dwProjectID"] = read_uint(file)#NieR Replicant = 6869, NieR Automata = 2317
    BKHD["padding"] = file.read(BKHD["dwChunkSize"]-20)
    return BKHD

def readDIDX(file):#Media Index
    print("Reading Media Index...")
    DIDX = {}
    DIDX["dwTag"] = "DIDX"
    DIDX["dwChunkSize"] = read_uint(file)
    #print("Media Index Size: "+ str(DIDX["dwChunkSize"]))
    DIDX["pLoadedMedia"] = []
    for i in range(0,int(DIDX["dwChunkSize"]/12)):#Media Header size is 12 bytes
        MediaHeader = {}
        MediaHeader["id"] = read_uint(file)
        MediaHeader["uOffset"] = read_uint(file)
        MediaHeader["uSize"] = read_uint(file)
        DIDX["pLoadedMedia"].append(MediaHeader)
    return DIDX
def readDATA(file):#WEM Data
    print("Reading WEM Data...")
    DATA = {}
    DATA["dwTag"] = "DATA"
    DATA["dwChunkSize"] = read_uint(file)
    DATA["pData"] = bytearray(file.read(DATA["dwChunkSize"]))
    return DATA
def readHIRC(file):#Hierarchy
    #TODO - Fully parse HIRC
    print("Reading Hierarchy (Unmapped)...")
    HIRC = {}
    HIRC["dwTag"] = "HIRC"
    HIRC["dwChunkSize"] = read_uint(file)
    HIRC["HIRCDATA"] = file.read(HIRC["dwChunkSize"])#Will remove this once HIRC parsing is done.
    #HIRC["NumReleasableHircItem"] = read_uint(file)
    #HIRC["listLoadedItem"] = []
    return HIRC
def readSTID(file):#String Mappings
    print("Reading String Mappings...")
    STID = {}
    STID["dwTag"] = "STID"
    STID["dwChunkSize"] = read_uint(file)
    STID["uiType"] = read_uint(file)
    STID["uiSize"] = read_uint(file)
    STID["BankIDToFileName"] = []
    for i in range(0,STID["uiSize"]):
        AKBKHashHeader = {}
        AKBKHashHeader["bankID"] = read_uint(file)
        AKBKHashHeader["stringSize"] = read_ubyte(file)
        AKBKHashHeader["FileName"] = file.read(AKBKHashHeader["stringSize"]).decode('utf-8')
        STID["BankIDToFileName"].append(AKBKHashHeader)
    #print(STID["BankIDToFileName"])
    return STID

#def readINIT(file): # PluginChunk #TODO
    #INIT = {}
#def readSTMG(file): #GlobalSettingsChunk #TODO
    #STMG = {}
#def readENVS(file): #EnvSettingsChunk #TODO
    #ENVS = {}
#def readPLAT(file): #CustomPlatformChunk #TODO
    #PLAT = {}
def readUNKN(file):
    UNKN = {}
    file.seek(file.tell()-4)#Since the chunk name is unknown, go back and read it
    UNKN["dwTag"] = file.read(4).decode('utf-8')
    UNKN["dwChunkSize"] = read_uint(file)
    UNKN["unknData"] = file.read(UNKN["dwChunkSize"])
    return UNKN
def readBNKChunk(file):#Reads chunk name, decides what to do based on the name.
    type = file.read(4)
    if type == b"BKHD":#Bank Header
        chunk = readBKHD(file);
    elif type == b"DIDX":#Data Index
        chunk =  readDIDX(file);
    elif type == b"DATA":#WEM Data
        chunk =  readDATA(file);
    elif type == b"HIRC":#Hierarchy
        chunk =  readHIRC(file);
    elif type == b"STID":#String Mapping
        chunk =  readSTID(file);
    #elif type == b"INIT":#PluginChunk #TODO
        #chunk =  readINIT(file);
    #elif type == b"STMG":#GlobalSettingsChunk #TODO
        #chunk =  readSTMG(file);
    #elif type == b"ENVS":#EnvSettingsChunk #TODO
        #chunk =  readENVS(file);
    #elif type == b"PLAT":#CustomPlatformChunk #TODO
        #chunk =  readPLAT(file);
    else:
        raiseWarning("Unmapped Chunk Type: " + str(type) )
        chunk = readUNKN(file);
    return chunk

#---Write Functions---#    
def writeBKHD(file,BKHD):#Bank Header
    print("Writing Bank Header...")
    file.write(BKHD["dwTag"].encode('utf-8'))
    write_uint(file,BKHD["dwChunkSize"])
    write_uint(file,BKHD["dwBankGeneratorVersion"])
    write_uint(file,BKHD["dwSoundBankID"])
    write_uint(file,BKHD["dwLanguageID"])
    write_ushort(file,BKHD["bUnused"])
    write_ushort(file,BKHD["bDeviceAllocated"])
    write_uint(file,BKHD["dwProjectID"])
    file.write(BKHD["padding"])

def writeDIDX(file,DIDX):#Media Index
    print("Writing Media Index...")
    file.write(DIDX["dwTag"].encode('utf-8'))
    write_uint(file,DIDX["dwChunkSize"])
    for MediaHeader in DIDX["pLoadedMedia"]:
        write_uint(file,MediaHeader["id"])
        write_uint(file,MediaHeader["uOffset"])
        write_uint(file,MediaHeader["uSize"])
def writeDATA(file,DATA):#WEM Data
    print("Writing WEM Data...")
    file.write(DATA["dwTag"].encode('utf-8'))
    write_uint(file,DATA["dwChunkSize"])
    file.write(DATA["pData"])
def writeHIRC(file,HIRC):#Hierarchy
    #TODO - Fully parse HIRC
    print("Writing Hierarchy...")
    file.write(HIRC["dwTag"].encode('utf-8'))
    write_uint(file,HIRC["dwChunkSize"])
    file.write(HIRC["HIRCDATA"])#Will remove this once HIRC parsing is done.
    #write_uint(file,HIRC["NumReleasableHircItem"])
def writeSTID(file,STID):#String Mappings
    print("Writing String Mappings...")
    file.write(STID["dwTag"].encode('utf-8'))
    write_uint(file,STID["dwChunkSize"])
    write_uint(file,STID["uiType"])
    write_uint(file,STID["uiSize"])
    for AKBKHashHeader in STID["BankIDToFileName"]:
        write_uint(file,AKBKHashHeader["bankID"])
        write_ubyte(file,AKBKHashHeader["stringSize"])
        file.write(AKBKHashHeader["FileName"].encode('utf-8'))

#def writeINIT(file): # PluginChunk #TODO

#def writeSTMG(file): #GlobalSettingsChunk #TODO

#def writeENVS(file): #EnvSettingsChunk #TODO

#def writePLAT(file): #CustomPlatformChunk #TODO

def writeUNKN(UNKN):
    file.write(UNKN["dwTag"].encode('utf-8'))
    write_uint(file,UNKN["dwChunkSize"])
    file.write(UNKN["unknData"])
    
def writeBNKChunk(file,chunk):#Takes chunk, reads name, decides what to write based on the name.
    type = chunk["dwTag"]
    if type == "BKHD":#Bank Header
        writeBKHD(file,chunk);
    elif type == "DIDX":#Data Index
        writeDIDX(file,chunk);
    elif type == "DATA":#WEM Data
        writeDATA(file,chunk);
    elif type == "HIRC":#Hierarchy
        writeHIRC(file,chunk);
    elif type == "STID":#String Mapping
        writeSTID(file,chunk);
    #elif type == "INIT":#PluginChunk #TODO
        #writeINIT(file,chunk);
    #elif type == "STMG":#GlobalSettingsChunk #TODO
        #writeSTMG(file,chunk);
    #elif type == "ENVS":#EnvSettingsChunk #TODO
        #writeENVS(file,chunk);
    #elif type == "PLAT":#CustomPlatformChunk #TODO
        #writePLAT(file,chunk);
    
    else:
        writeUNKN(file,chunk);