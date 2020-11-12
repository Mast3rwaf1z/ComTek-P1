from Matrix_Checks import Check_is_1D_Matrix

# Splits the list of bytes into a vector with packets of one byte each
def Make_Packet_Vector(Packet):                     # Argument(Byte list)
    if not Check_is_1D_Matrix(Packet):              # Check if the input is of correct type
        print("Make_Packet_Vector ERROR: Argument entered is not a list")
        return
    LocalPack = Packet[:]
    ResPack = []
    for i in range(len(Packet)):
        ResPack.append([])                          # Make a row in Result packet
        ResPack[i].append(LocalPack[i])             # Fill each row with one byte
    return ResPack

# Splits the list of bytes into a matrix, where each row is a packet of the sized specified
def Make_Packet_Matrix(Packet, Num):                # Arguments(Byte list, Size of each packet in bytes)
    if not Check_is_1D_Matrix(Packet):              # Check if first argument is of correct type (List with numbers in)
        print("Make_Packet_Matrix ERROR: First argument entered is not a list")
        return
    if not isinstance(Num, int):                    # Check if second argument is of correct type (Integer)
        print("Make_Packet_Matrix ERROR: Second argument entered is not an integer")
        return
    LocalPack = Packet[:]
    ResPack = []
    x = Num - (len(LocalPack) % Num)                # Find out how many empty bytes there will be (If a file of 188 byte is devided into 50 byte a packer, 12 bytes will be empty)
    y = 1                                           # A number that is used to see if we have encoded the entire byte list, so we insert zeros after
    if x == Num:                                    # If there are no empty bytes needed
        for i in range(len(LocalPack) // Num):      # Move and create a new row
            ResPack.append([])
            for j in range(Num):                    # Fill the new row with the bytes according to the size given
                ResPack[i].append(LocalPack[i * Num + j])
    else:
        for i in range((len(LocalPack) // Num) + 1):# If we need zeros, then the number of rows is one more than the floor division
            ResPack.append([])                      # Move and create a new row
            for j in range(Num):
                if y == len(LocalPack):             # If we have filled all the bytes in, then fill the rest of the row with zeros
                    ResPack[i].append(0)
                else:                               # Else fill the row with the bytes
                    ResPack[i].append(LocalPack[i * Num + j])
                    y += 1                          # Add one to the byte counter
    return ResPack
