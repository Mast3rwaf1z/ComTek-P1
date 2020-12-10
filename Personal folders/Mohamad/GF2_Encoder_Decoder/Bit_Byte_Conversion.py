from Matrix_Checks import Check_is_1D_Matrix
from Random_Matrix import Random_2D_Bit_Matrix

# Converts a list of zeros and ones into a list of decimal bytes (Bytearray)
def Bits_to_Bytes(BitList):                 # Argument(List with bits)
    if not Check_is_1D_Matrix(BitList):
        print("Bit_to_Bytes ERROR: Argument is not a 1D list")
    #if (len(BitList) % 8) != 0:
    #    print("Bit_to_Bytes ERROR: List length is not a multiple of 8")
    LocList = BitList[:]                    # Copy array into a local list
    if (len(BitList) % 8) != 0:             # If array is not a multiple of 8 then set 0s at the start until it is a multiple of 8
        for i in range(8 - (len(BitList) % 8)):
            LocList.insert(0, 0)
    ResMat = []                             # Create matrix to be filled with bytes
    for i in range(len(LocList) // 8):
        ResMat.append((128 * LocList[8 * i]) + (64 * LocList[8 * i + 1]) + (32 * LocList[8 * i + 2]) + (16 * LocList[8 * i + 3]) + (8 * LocList[8 * i + 4]) + (4 * LocList[8 * i + 5]) + (2 * LocList[8 * i + 6]) + (LocList[8 * i + 7]))
    return ResMat


# Converts a list of decimal bytes (Bytearray) into a list of zeros and ones
def Bytes_to_Bits(ByteList):                #Argument(List with bytes)
    if not Check_is_1D_Matrix(ByteList):
        print("Bytes_to_Bits ERROR: Argument is not a 1D list")
    LocList = ByteList[:]
    ResMat = []
    for i in range(len(LocList)):
        x = LocList[i]
        ResMat.append(x // 128)
        if x // 128:
            x = x - 128
        ResMat.append(x // 64)
        if x // 64:
            x = x - 64
        ResMat.append(x // 32)
        if x // 32:
            x = x - 32
        ResMat.append(x // 16)
        if x // 16:
            x = x - 16
        ResMat.append(x // 8)
        if x // 8:
            x = x - 8
        ResMat.append(x // 4)
        if x // 4:
            x = x - 4
        ResMat.append(x // 2)
        if x // 2:
            x = x - 2
        ResMat.append(x)
    return ResMat
