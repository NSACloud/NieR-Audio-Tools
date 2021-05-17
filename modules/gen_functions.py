#V1
#-----General Functions-----#
import os
import struct

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
def read_ubyte(file_object, endian = '<'):
     data = struct.unpack(endian+'B', file_object.read(1))[0]
     return data
# read signed byte from file
def read_byte(file_object, endian = '<'):
     data = struct.unpack(endian+'b', file_object.read(1))[0]
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
def read_string(file_object):
     data =''.join(iter(lambda: file_object.read(1).decode('ascii'), '\x00'))
     return data
def read_unicode_string(file_object):#Reads unicode string from file into utf-8 string
    data =(''.join(iter(lambda: file_object.read(2).decode('utf-8'), '\x00\x00'))).replace('\x00', '')#TODO Fix this
    return data
# write unsigned byte to file
def write_ubyte(file_object,input, endian = '<'):
     data = struct.pack(endian+'B', input)
     file_object.write(data)
# write signed byte to file
def write_byte(file_object,input, endian = '<'):
     data = struct.pack(endian+'b', input)
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
def write_unicode_string(file_object,input):#Writes utf-8 string as utf-16
     data = input.encode('UTF-16LE') + b'\x00\x00'#Little endian utf16
     file_object.write(data)#::2 because
def getPaddingAmount(currentPos,alignment):
    padding = (currentPos*-1)%alignment
    return padding
def raiseError(error,errorCode = 999):
     print(textColors.FAIL + "ERROR: " + error + textColors.ENDC)
     exit(errorCode)

def raiseWarning(warning):
     print(textColors.WARNING + "WARNING: " + warning + textColors.ENDC)

def getByteSection(byteArray,offset,size):
    data = byteArray[offset:(offset+size)]
    return data
def removeByteSection(byteArray,offset,size):#removes specified amount of bytes from byte array at offset
    del byteArray[offset:(offset+size)]#Deletes directly from the array passed to it
def insertByteSection(byteArray,offset,input):#inserts bytes into bytearray at offset
    byteArray[offset:offset] = input

def createIndexDict(name_dict, id_key):#Creates dictionary of names and their index
    index_dict = dict((p[id_key], i) for i, p in enumerate(name_dict)) #index_dict.get(id, None) returns index of that id
    return index_dict
