from Operations import *
from Configs import *
from Generations_Decode import Generations_Decode
from Generations_Sort import Generations_Sort
from Constants import Full_File_Size_Ran, Generation_File_Size, Generations_Decoded, Full_File_Size, Pivot_Pos, Packets_Needed_To_Decode_Generation

# The function that sorts the packets (Will change name at the end)
def Sort_Packets(Packet, File_Size):
    Loc_Packet = Packet[:]                                                                      # Copy to a local packet (Just in case)
    global Full_File_Size_Ran
    if Full_File_Size_Ran == 0:                                                                 # Don't get the full size more than once (Can't remember why maybe to save power?)
        global Full_File_Size
        for i in range(File_Size):
            Full_File_Size = Full_File_Size + (Loc_Packet[i] * (255**(File_Size - 1 - i)))      # Get full file size out of file size headers
        Gen_Total = Floor_Div_Round_Up(Full_File_Size, Generation_File_Size)                    # Generation file size might not be needed
        Gen_Config(Gen_Total)                                                                   # Run the Generation list initiation function
        Full_File_Size_Ran += 1

    # Get the headers out and set them in a local varaible
    Gen_Num = Loc_Packet[File_Size]
    Gen_Size = Loc_Packet[File_Size + 1]
    Symbol_Size = Loc_Packet[File_Size + 2]

    global Generations_Decoded
    if Generations_Decoded[Gen_Num] == 0:
        print("Corrosponding Generation decoded")
        # Send message that says generation was decoded
        return 2

    # Get the coefficients out of the header and set them in a local list
    Coefficients_Start = File_Size + 3
    Coefficients_End =  File_Size + 3 + Floor_Div_Round_Up(Gen_Size, 8)
    Coefficients = Loc_Packet[Coefficients_Start:Coefficients_End]

    # Increase the number of packets used by one
    Packets_Needed_To_Decode_Generation[Gen_Num] += 1
    # Make the coefficients list into a list of bits
    Coefficients_bits = Bytes_to_Bits(Coefficients)
    for i in range(len(Coefficients_bits) - Gen_Size):
        Coefficients_bits.pop(0)                            # Remove the extra bits at the start

    # Make a local list with the coded symbol
    Symbol_Start = File_Size + 3 + Floor_Div_Round_Up(Gen_Size, 8)
    Symbol = Loc_Packet[Symbol_Start:]
    if Symbol_Size != len(Symbol):                          # Checks if the coded packet is missing anything from the symbol
        print("Packet_Remove_Header ERROR: Size of data in symbol is not same as in header. Packet will not be used")
        return -1
    Pivot_Position_Config(Gen_Num, Gen_Size)                # Run the pivot position list initializing function with this designated generation

    # Create the coded symbol that has to be guassian eliminated
    Coded_Symbol = Coefficients_bits
    for i in range(len(Symbol)):
        Coded_Symbol.append(Symbol[i])

    # Gaussian eliminate packet and add it to generation

    Res = Generations_Decode(Coded_Symbol, Gen_Num, Gen_Size)
    if Res == -1:
        print("Packet discarded")
    if Res == 1:
        print("Packet inserted")
    else:
        print("Unknown result")

    # Check if the generation was fully decoded

    if len(Generations[Gen_Num]) == Gen_Size:
        global Pivot_Pos
        Num_Pivots = Pivot_Pos[Gen_Num][0]
        for i in range(len(Pivot_Pos[Gen_Num]) - 1):
            Num_Pivots = Num_Pivots + Pivot_Pos[Gen_Num][i + 1]
        if Num_Pivots != Gen_Size:
            print("There is a bug, the generation has enough symbols inside, but they do not form a pivot position")
        else:
            print("Packets needed to reduce generation number" + str(Gen_Num) + "is: " + str(Packets_Needed_To_Decode_Generation))
            Generations_Sort(Gen_Num, Gen_Size, Symbol_Size)

        # Here run a function to sort the generation and completely reduce it
