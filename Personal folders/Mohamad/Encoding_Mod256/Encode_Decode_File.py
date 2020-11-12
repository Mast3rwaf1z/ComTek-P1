from Z256_Inverse_Matrix import Z256_Inverse_Matrix
from Z256_Matrix_Multi import Matrix_Multi
from Z256_Random_Matrix import Z256_Random_Reducible_Matrix
from Packet_Spliting import *
from Matrix_Checks import Check_is_2D_Matrix
from Operations import *
from Z256_Matrix_Operations import *
from Get_Identity_Matrix import Get_I_Matrix


# This function takes an encoding matrix and encodes a column vector of packets.
# Then inserts the encoding row followed by a 0 as a header behind the encoded packet
def Encode_Packets(EncMat, Packet):
    if not Check_is_2D_Matrix(EncMat):               # Check if encoding/decoding matrix is a 2D matrix
        print("Encode_Packets ERROR: First argument is not a 2D matrix")
        return
    if not Check_is_2D_Matrix(Packet):                  # Check if packet vector is a column vector (2D matrx)
        print("Encode_Packets ERROR: Second argument is not a 2D matrix (Column vectors are seen as 2D Matrices)")
        return
    if not len(EncMat) == len(EncMat[0]):         # Check if encoding/decoding matrix is square
        print("Encode_Packets ERROR: First argument is not a square matrix")
        return

    LocPack = Packet[:]
    LocEncMat = EncMat[:]
    ResMatNoHeader = []
    ResMat = []
    ZeroVec = []                                        # Create a zero row vector that has the same length as a row in the packet

    for i in range(len(LocPack[0])):                    # Fill the zero row vector
        ZeroVec.append(0)
    for i in range(len(LocEncMat)):                     # This shows the row of the encoding/decoding matrix we are working with
        y = ZeroVec                                     # Reset y to the 0 row vector
        for j in range(len(LocPack)):                   # This shows the row of the packet vector we are working with
            x = Z256_Const_1D_Mat_Multi(LocPack[j], LocEncMat[i][j])    # Z256 Multiply the the row with its corrosponding constant in the encoding/decoding row
            y = Z256_Matrix_1D_Add(y, x)                # Z256 Add the multiplied packet with the previous multiplied packet (Starts with a zero row vector)
        ResMatNoHeader.append(y)                                # Append the encoded packet into the encoded packet matrix

# The next section inserts the encoding vector before the encoded matrix, and then inserts the value 255 to seperate the two
# This will be used, so the decoding function will search for the first 255 to seperate the encoding vector from the encoded matrix
    for i in range(len(ResMatNoHeader)):
        ResMat.append(ResMatNoHeader[i])                # Append the encoded matrix without the encoding vector (Header)
        for j in range(len(LocEncMat[0]) + 1):
            if j == len(LocEncMat[i]):                  # If all encoding vector elements have been inserted, then insert 255
                ResMat[i].insert(j, 255)
            else:
                ResMat[i].insert(j, LocEncMat[i][j])    # Insert the elements of the encoding vector before the encoded matrix
                #print("Element in " + str(i) + "x" + str(j) + "is: " + str(LocEncMat[i][j]))

    return ResMat                                       # Return the matrix that has the following in each row: [encoding vector, 255, encoded packets]

"""
# This function takes an encoding matrix and encodes a column vector of packets.
# The same function is used to decode, where the decoding matrix is the inverse of the encoding matrix.
def Encode_Decode_Packets(EncDecMat, Packet):
    if not Check_is_2D_Matrix(EncDecMat):               # Check if encoding/decoding matrix is a 2D matrix
        print("Encode_Packets ERROR: First argument is not a 2D matrix")
        return
    if not Check_is_2D_Matrix(Packet):                  # Check if packet vector is a column vector (2D matrx)
        print("Encode_Packets ERROR: Second argument is not a 2D matrix (Column vectors are seen as 2D Matrices)")
        return
    if not len(EncDecMat) == len(EncDecMat[0]):         # Check if encoding/decoding matrix is square
        print("Encode_Packets ERROR: First argument is not a square matrix")
        return

    LocPack = Packet[:]
    LocEncMat = EncDecMat[:]
    ResMat = []
    ZeroVec = []                                        # Create a zero row vector that has the same length as a row in the packet

    for i in range(len(LocPack[0])):                    # Fill the zero row vector
        ZeroVec.append(0)
    for i in range(len(LocEncMat)):                     # This shows the row of the encoding/decoding matrix we are working with
        y = ZeroVec                                     # Reset y to the 0 row vector
        for j in range(len(LocPack)):                   # This shows the row of the packet vector we are working with
            x = Z256_Const_1D_Mat_Multi(LocPack[j], LocEncMat[i][j])    # Z256 Multiply the the row with its corrosponding constant in the encoding/decoding row
            y = Z256_Matrix_1D_Add(y, x)                # Z256 Add the multiplied packet with the previous multiplied packet (Starts with a zero row vector)
        ResMat.append(y)                                # Append the encoded packet into the encoded packet matrix

    return ResMat
"""

File = open("C:\\Users\moham\Desktop\LoPy files\main_to_edit.py","rb+")
ReadFile = File.read()
ListFile = list(ReadFile)
print(ListFile)
print(ReadFile)

Packet = Make_Packet_Matrix(ListFile, 50)
print("Packet")
print(Packet)

for i in range(len(Packet)):
    print(bytes(Packet[i]))

EncodingMatrix = [[235, 124, 14, 2], [244, 135, 48, 167], [134, 52, 155, 254], [178, 94, 212, 1]]

EncodedPacket = Encode_Packets(EncodingMatrix, Packet)
print("EncodedPacket")
print(EncodedPacket)

IdentityMat = Get_I_Matrix(4)

EncodedPacket = Encode_Packets(IdentityMat, Packet)
print("EncodedPacket")
print(EncodedPacket)

for i in range(len(EncodedPacket)):
    print(bytearray(EncodedPacket[i]))

"""
File = open("C:\\Users\moham\Desktop\LoPy files\main.py","rb+")
ReadFile = File.read()
ListFile = list(ReadFile)
print(ListFile)
print(len(ListFile))

Packet = Make_Packet_Matrix(ListFile, 50)
print("Packet")
print(Packet)
RandMat = Z256_Random_Reducible_Matrix(len(Packet))
print("RandMat")
print(RandMat)
EncodedPacket = Encode_Decode_Packets(RandMat, Packet)
print("EncodedPacket")
print(EncodedPacket)
print(len(EncodedPacket))
InvRandMat = Z256_Inverse_Matrix(RandMat)
print("InvRandMat")
print(InvRandMat)
DecodedPacket = Encode_Decode_Packets(InvRandMat, EncodedPacket)
print("DecodedPacket")
print(DecodedPacket)

if Packet == DecodedPacket:
    print("Worked")
else:
    print("Did not work")
"""

"""
Packet = Make_Packet_Matrix(ListFile, 50)
print("Packet")
print(Packet)
RandMat = Z256_Random_Reducible_Matrix(len(Packet))
print("RandMat")
print(RandMat)
EncodedPacket = Matrix_Multi(RandMat, Packet)
print("EncodedPacket")
print(EncodedPacket)
InvRandMat = Z256_Inverse_Matrix(RandMat)
print("InvRandMat")
print(InvRandMat)
DecodedPacket = Matrix_Multi(InvRandMat, EncodedPacket)
print("DecodedPacket")
print(DecodedPacket)

if Packet == DecodedPacket:
    print("Worked")
else:
    print("Did not work")
"""

