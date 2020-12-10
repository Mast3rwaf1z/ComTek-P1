from Matrix_Checks import Check_is_1D_Matrix, Check_is_2D_Matrix
from Matrix_Operations import Const_1D_Mat_Multi
from Bit_Byte_Conversion import Bits_to_Bytes

Send_File_Error = 0

# Encodes a generation of symbols according to an encoding vector
# Then puts a header at the start to create an encoded packet
def Encode_Symbol(Vect_Gen, Vect_Enc, File_Size, Generation_Number):        # Arguments(Generation vector (List with symbols), Encoding vector, File size for header, Generation number for header)
    if not Check_is_2D_Matrix(Vect_Gen):
        print("Encode_Symbol ERROR: Generation vector is not a 2D matrix")
        return
    if not Check_is_1D_Matrix(Vect_Enc):
        print("Encode_Symbol ERROR: Encoding vector is not a 1D matrix")
        return
    if not len(Vect_Gen) == len(Vect_Enc):
        print("Encode_Symbol ERROR: Encoding and Generation vectors are not same length")
        return
    # Checks are incomplete. Need to check last two args


    a = []                                                      # First packet to be XoR'ed, it also ends up being the encoded symbol
    Coded_Packet = []                                           # Filled with header and the list a
    Byte_Vect_Enc = Bits_to_Bytes(Vect_Enc)                     # Encoding vector as a byte array

    for i in range(len(Vect_Gen[0])):                           # Fill a with 0s for first XoR to work
        a.append(0)
    for i in range(len(Vect_Enc)):
        b = Const_1D_Mat_Multi(Vect_Gen[i], Vect_Enc[i])        # Second packet to be XoR'ed with a
        a = bytes([a ^ b for a, b in zip(a, b)])                # XoR operation

# Header Format
# [Full file size, #Generation, Generation size, Packet(Symbol) Size, Encoding row vector in bytes]
# Full file size is two bytes. First to be multiplied with 255, second to be added after the multiplication. This makes it able to give sizes up to 63 kilobytes
    File_Size1 = File_Size // (255*255)
    File_Size2 = (File_Size - File_Size1 * (255*255)) // 255
    #if File_Size1 > 255:
        #print("Encode_Symbol ERROR: File size is larger than the supported size of 65,280 bytes")
        #global Send_File_Error
        #Send_File_Error = -1               # Figure out a way to change an error variable
    File_Size3 = File_Size % 256
    Coded_Packet.append(File_Size1)
    Coded_Packet.append(File_Size2)
    Coded_Packet.append(File_Size3)
    Coded_Packet.append(Generation_Number)
    Coded_Packet.append(len(Vect_Gen))
    Coded_Packet.append(len(Vect_Gen[0]))
    for i in range(len(Byte_Vect_Enc)):
        Coded_Packet.append(Byte_Vect_Enc[i])
    for i in range (len(a)):
        Coded_Packet.append(a[i])

    return Coded_Packet

"""
Test_Gen = [[11], [15], [8], [6]]
Test_Enc = [1, 0, 1, 1]
Test_Res = Encode_Symbol(Test_Gen, Test_Enc, 4, 1)
print(Test_Res)                                         # Test successful
"""
