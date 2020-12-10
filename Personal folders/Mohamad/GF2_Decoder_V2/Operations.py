# Converts a list of decimal bytes (Bytearray) into a list of zeros and ones
def Bytes_to_Bits(ByteList):                #Argument(List with bytes)
    #if not Check_is_1D_Matrix(ByteList):
    #    print("Bytes_to_Bits ERROR: Argument is not a 1D list")
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

# Floor division usually rounds down. This function makes it round up instead
def Floor_Div_Round_Up(x, y):
    a = x / y
    b = x // y
    if a != b:                  # If there are decimals then round up
        return b+1
    else:
        return b
