from Matrix_Checks import Check_is_1D_Matrix, Check_is_2D_Matrix
from Matrix_Operations import Const_1D_Mat_Multi
from Bit_Byte_Conversion import Bits_to_Bytes

# Encodes a generation of symbols according to an encoding vector
# Then puts a header at the start to create an encoded packet
def Encode_Symbol(Vect_Gen, Vect_Enc, File_Size, Generation_Number):        # Arguments(Generation vector (List with symbols), Encoding vector, File size for header, Generation number for header)
    # Do checks and return errors if check fail
    if not Check_is_2D_Matrix(Vect_Gen):
        print("Encode_Symbol ERROR: Generation vector is not a 2D matrix")
        return
    if not Check_is_1D_Matrix(Vect_Enc):
        print("Encode_Symbol ERROR: Encoding vector is not a 1D matrix")
        return
    if not len(Vect_Gen) == len(Vect_Enc):
        print("Encode_Symbol ERROR: Encoding and Generation vectors are not same length")
        return

    a = []                                                                  # First packet to be XoR'ed, it also ends up being the encoded symbol
    Coded_Packet = []                                                       # Packet to be sent. Format: Header|Coefficients vector|Coded symbol
    Byte_Vect_Enc = Bits_to_Bytes(Vect_Enc)                                 # Encoding vector as a byte array

    for i in range(len(Vect_Gen[0])):                                       # Fill a with 0s for first XoR to work
        a.append(0)
    for i in range(len(Vect_Enc)):
        b = Const_1D_Mat_Multi(Vect_Gen[i], Vect_Enc[i])                    # Second packet to be XoR'ed with a
        a = bytes([a ^ b for a, b in zip(a, b)])                            # XoR operation

# Header Format
# [Full file size, #Generation, Generation size, Packet(Symbol) Size, Encoding row vector in bytes]
# Full file size is three bytes. First to be multiplied with 256^2, second to be multiplied with 256, third to be added after the multiplication. This makes it able to give sizes up to 16 megabytes
    File_Size1 = File_Size // (256*256)                                     # Get first file size byte
    File_Size2 = (File_Size - File_Size1 * (256*256)) // 256                # Get second file size byte
    File_Size3 = File_Size % 256                                            # Get third file size byte
    Coded_Packet.append(File_Size1)                                         # Add first file size byte to the coded packet
    Coded_Packet.append(File_Size2)                                         # Add second file size byte to the coded packet
    Coded_Packet.append(File_Size3)                                         # Add third file size byte to the coded packet
    Coded_Packet.append(Generation_Number)                                  # Add generation number to the coded packet
    Coded_Packet.append(len(Vect_Gen))                                      # Add the generation size to the coded packet
    Coded_Packet.append(len(Vect_Gen[0]))                                   # Add the symbol size to the coded packet
    for i in range(len(Byte_Vect_Enc)):                                     # Add the coefficients vector to the coded packet
        Coded_Packet.append(Byte_Vect_Enc[i])
    for i in range (len(a)):                                                # Add the coded symbol to the coded packet
        Coded_Packet.append(a[i])

    return Coded_Packet                                                     # Return the coded packet
