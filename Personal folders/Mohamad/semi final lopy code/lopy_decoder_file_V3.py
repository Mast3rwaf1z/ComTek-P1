from network import LoRa
import pycom
import socket
import time
import ubinascii
import struct
import sys

Generation_File_Size = 32*40                        # This is manually assigned for now (Can be fixed by sending it from the gateway)
Gen_Num = 0                                         # Hold the generation number that is being worked with
Generations = []                                    # 3D matrix that holds a list of generations, which hold a list of the symbols
Generations_Decoded = []                            # This 1D matrix indicates which generation have been decode, to not send any more coded symbols ot them
Full_File_Size_Ran = 0                              # Is 1 when the variable is assigned, because don't mess with the global variabl grr
Full_File_Size = 0                                  # Had to become a global variable, as it is used in more than one function
Full_File_Data = []                                 # This 2D matrix has all the decoded data from each generation in order. Will be combined in the end to one file
File_Data_List = []                                 # This list contains everything in Full_File_Data but in one list, this is to pop out the extra bits at the end
Pivot_Pos = []                                      # A list of generations, which contains the info on pivot positions. 1 = yes pivot, 0 =  no pivot
Pivot_Pos_Ran = []                                  # Is 1 when the pivot position is filled with with pivot variables
Packets_Needed_To_Decode_Generation = []            # This list contains the number of packets received before a generation was decoded. The positions of the list represent the generation number

# Converts a list of decimal bytes (Bytearray) into a list of zeros and ones
def Bytes_to_Bits(ByteList):                        # Argument(List with bytes)
    LocList = ByteList[:]                           # Copy argument list into a local list
    ResMat = []                                     # Make a list to be filled with the bits
    # Cover the bytes list into a bits list
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
def Floor_Div_Round_Up(x, y):   # Arguments(Number to be floor divided, Number to be floor divided with)
    a = x / y
    b = x // y
    if a != b:                  # If there are decimals then round up
        return b+1
    else:
        return b

# Prints a list with each element on its own line
def Dump_Mat(Matrix):           # Argument(Matrix to be printed)
    for i in Matrix:
        print(i)

# Initiates the global lists
def Gen_Config(Gen_Total):                          # Argument(The number of generations the file will have)
    for i in range(Gen_Total):
        Generations.append([])                      # Fill the list with the generation lists (Initiate generation list)
        Full_File_Data.append([])                   # Fill list with enough place for each generation (Initiate Fill_File_Data list)
        Pivot_Pos.append([])                        # Fill the list with the generation pivot lists (Initiate Pivot_Pos list)
        Pivot_Pos_Ran.append(0)                     # Fill the list with zero states (Initiate Pivot_Pos_Ran list)
        Generations_Decoded.append(0)               # Fill the list with zero states (Initiate Generations_Decoded list)
        Packets_Needed_To_Decode_Generation.append(0)

# Further initiation for global lists that need it
def Pivot_Position_Config(Gen_Num, Gen_Size):
    if Pivot_Pos_Ran[Gen_Num] == 0:                 # If the designated generation list was not filled, the proceed else do nothing
        for i in range(Gen_Size):
            Pivot_Pos[Gen_Num].append(0)            # Set 0s with the number of pivot positions in the generation
        Pivot_Pos_Ran[Gen_Num] = 1                  # Don't run this again for the same generation

        
# This function sorts a generation by using the pivot position label at the start of each row
def Generations_Sort(Gen_Num, Gen_Size):                        # Arguments(Generation number of the generation to sort, Generation size of the generation to sort)
    Loc_Gen = Generations[Gen_Num][:]                           # Make a local copy of the generation
    Sorted_Gen = []                                             # This list will be used to sore the generation
    for i in range(Gen_Size):                                   # Make enough rows to sort the generation
        Sorted_Gen.append([])

    # Sort the generation

    for i in range(len(Loc_Gen)):                               # Go through the rows of the generation
        Sorting_Pos = Loc_Gen[i][0]                             # Read the pivot position of the row
        for j in range(len(Loc_Gen[i])):                        
            Sorted_Gen[Sorting_Pos].append(Loc_Gen[i][j])       # Copy this row to its right position

    # Check that it has sorted correctly
    # If the generation is fully decoded pop out the pivot position indicator
    # If not remove the rows without any elements

    if len(Loc_Gen) == Gen_Size:                                # If the generation is fully decoded
        for i in range(len(Sorted_Gen)):                        # Go through all rows
            if Sorted_Gen[i][0] == i:                           # If the row is in its right position
                Sorted_Gen[i].pop(0)                            # Pop the pivot position indicator
            else:                                               # If not sorted correctly
                print("There is a bug, the sorting algorithm has failed to sort the generation")
                return -1                                       # Return an error value
        return Sorted_Gen                                       # Return the sorted generation
    else:                                                       # If the generation is not fully decoded
        pop_List = []                                           # This list contains the position of the rows without any elements
        Pivot_List = []                                         # This list contains the position of the rows with elements
        for i in range(len(Sorted_Gen)):                        # Go through all the lists in Sorted Gen
            if len(Sorted_Gen[i]) == 0:                         # If the list is empty
                pop_List.append(i)                              # Put tis position in pop_List
            else:                                               # If list is not empty
                Pivot_List.append(i)                            # Put tis position in Pivot_List
        pop_List.reverse()                                      # Reverse the pop list so it works from the highest value. Otherwise an error would occur due to positions changing after removing an empty list
        for i in pop_List:                                      # Go throught the rows without elements
            Sorted_Gen.pop(i)                                   # And remove these rows
        for i in range(len(Sorted_Gen)):                        # Go through the remaining rows
            if Sorted_Gen[i][0] == Pivot_List[i]:               # Check if they are ordered correctly
                continue
            else:                                               # If not
                print("There is a bug, the sorting algorithm has failed to sort the generation")
                return -1                                       # Return an error value
        return Sorted_Gen                                       # Return the sorted generation

# This function takes a sorted matrix and reduces it to reduced echelon form
def Generations_Complete_Reduce(Gen, Gen_Num, Gen_Size, Symbol_Size):           # Arguments(Generation to reduce, Generation number, Generation size, Symbol size)
    Sorted_Gen = Gen[:]                                                         # Copy the generation into a local generation
    for i in range(len(Sorted_Gen) - 1, 0, -1):                                 # The bottom symbol
        a = Sorted_Gen[i][:]                                                    # Copy the bottom row into a local list to be XoR'ed
        for j in range(i):                                                      # The upper symbols
            if Sorted_Gen[j][i] == 1:                                           # Only XoR if a coefficient is not 0, cause otherwise you don't need to XoR
                b = Sorted_Gen[j][:]                                            # Copy the upper symbol into a local list to be XoR'ed
                Sorted_Gen[j] = bytes([a ^ b for a, b in zip(a, b)])            # XoR the two lists and replace the row of the upper symbol with the XoR'ed row

    # Append all the symbol data into the Full_File_Data list which is used to make the file

    for i in range(Gen_Size):                                                   # Go through all rows in the generation
        for j in range(Symbol_Size):                                            # Go through all the elements in the symbol
            Full_File_Data[Gen_Num].append(Sorted_Gen[i][Gen_Size + j])         # Put the symbol elements in the Full_File_Size list
    Generations_Decoded[Gen_Num] = 1                                            # Declare the generation as decoded
    return 1                                                                    # Return a success value

# This function takes a coded symbol and performs the decoding algorithm on it
def Generations_Decode(Coded_Symbol, Gen_Num, Gen_Size):                        # Arguments(Coded symbol with coefficients vector, Generation number of the symbol, Generation size of the symbol)
    Loc_Symbol = Coded_Symbol[:]                                                # Copy the list with coefficients and coded symbol into a local list
    Useless_Symbol = 0                                                          # Create the useless symbol indicator
    Position = -1                                                               # Create the position indicator, which indicates the position of the first 1 in the coefficients vector

    # Check the position of the first 1, if there are not 1s then it is useless

    for i in range(Gen_Size):                                                   # Check the elements of the coefficients vector
        if Loc_Symbol[i] == 1:                                                  # If a 1 is found
            Useless_Symbol = 0                                                  # Declare the symbol as useful
            Position = i                                                        # Assign the position of the one
            break                                                               # Stop further checking
        else:                                                                   # If no 1 is found
            Useless_Symbol = 1                                                  # Declare the symbol as useless
    if Useless_Symbol == 1:                                                     # If the symbol is useless
        #print("Packet is empty \n")                                            # Print the reason
        return -1                                                               # Return discarded symbol code

    # Check if this can be used without reducing it (It can make a pivot position without reducing)

    if Pivot_Pos[Gen_Num][Position] == 0:                                       # Check if this generation does not have a pivot position that this symbol can occupy
        Pivot_Pos[Gen_Num][Position] = 1                                        # If not then change the value into 1 (Pivot position available)
        Loc_Symbol.insert(0, Position)                                          # Insert the pivot position indicator at the start of the symbol (Element used in sorting algorithm)
        # The prints bellow are used to visualise what happens with the symbol
        #print("Packet inserted without row operations \n")
        #if len(Generations[Gen_Num]) == 0:
            #print("[]")
        #else:
            #Dump_Mat(Generations[Gen_Num])
        #print("↑")
        #print(Loc_Symbol)
        #print("\n")
        Generations[Gen_Num].append(Loc_Symbol)                                 # Add the symbol to the echelon form generation
        return 1                                                                # Return packet inserted value

    # Sort the generation

    Generations[Gen_Num] = Generations_Sort(Gen_Num, Gen_Size)                  # Else sort the generation to start doing row operations

    # Go and do the reduction using all currently available packets in the generation (You will have to remove the 2 things at the start again)

    #print("-------------------------------------------Doing Row Operations------------------------------------------------")   # This is used to make the terminal more readable
    a = Loc_Symbol[:]                                                           # Copy the local symbol into a list to be XoR'ed
    for i in range(len(Generations[Gen_Num])):                                  # Go through all the symbols in the echelon form generation
        Initial_Pivot_Pos = Generations[Gen_Num][i][0]                          # Get the pivot position of the row we are using to reduce
        if a[Initial_Pivot_Pos] == 1:                                           # If the row can actually reduce the symbol, then proceed with XoR'ing
            b = Generations[Gen_Num][i][:]                                      # Copy the row to use for reducing into a list to be XoR'ed
            b.pop(0)                                                            # Remove the pivot position element
            # The prints bellow are used to visualise what happens with the symbol
            #print("Removing the 1 in position " + str(Initial_Pivot_Pos) + "\n")
            #print(b)
            #print("XoR")
            #print(list(a))
            a = bytes([a ^ b for a, b in zip(a, b)])                            # XoR
            #print("=")
            #print(list(a))
            #print("\n")
        #else:                                                                  # This else is only needed for prints to say that no XoR was performed
            #print("Position " + str(Initial_Pivot_Pos) + " is 0. No need to XoR with")
            #print(Generations[Gen_Num][i][1:])
    a = list(a)                                                                 # When a list is XoR'ed it become a bytes object, so transform the object into a list again
    Loc_Symbol = a[:]                                                           # Make the local symbol into the fully reduced symbol
    #print("---------------------------------------------------Done--------------------------------------------------------")

    # After it is reduced do the same check for the position of 1

    for i in range(Gen_Size):                                                   # Check the elements of the coefficients vector
        if Loc_Symbol[i] == 1:                                                  # If a 1 is found
            Useless_Symbol = 0                                                  # Declare the symbol as useful
            Position = i                                                        # Assign the position of the one
            break                                                               # Stop further checking
        else:                                                                   # If no 1 is found
            Useless_Symbol = 1                                                  # Declare the symbol as useless
    if Useless_Symbol == 1:                                                     # If the symbol is useless
        #print("Packet is dependent \n")                                        # Print the reason
        return -1                                                               # Return discarded symbol code

    # One last check to see if the symbol is useable

    if Pivot_Pos[Gen_Num][Position] == 0:                                       # Check if this generation does not have a pivot position that this symbol can occupy
        Pivot_Pos[Gen_Num][Position] = 1                                        # If not then change the value into 1 (Pivot position available)
        Loc_Symbol.insert(0, Position)                                          # Insert the pivot position indicator at the start of the symbol (Element used in sorting algorithm)
        # The prints bellow are used to visualise what happens with the symbol
        #print("Packet inserted without row operations \n")
        #if len(Generations[Gen_Num]) == 0:
            #print("[]")
        #else:
            #Dump_Mat(Generations[Gen_Num])
        #print("↑")
        #print(Loc_Symbol)
        #print("\n")
        Generations[Gen_Num].append(Loc_Symbol)                                 # Add the symbol to the echelon form generation
        return 1                                                                # Return symbol inserted value
    else:
        print("There is a bug in the system, the thing got reduced and still did not get a unique pivot position. For some reason it still works with this bug.")   # Print the result if this check fails
        #print(Loc_Symbol)                                                      # Print the symbol out
        #print("\n")
        return -1                                                               # Return discarded symbol code


# The function reads the header of the coded packet, then sends the coded symbols to the decoding function
# It also runs the function to reduce the generation into reduced echelon form
# This can be seen as the main function, that integrates all the functions above
def Sort_Packets(Packet, File_Size = 3):                                                        # Arguments(Packet to work with, Number of bytes in file size header(Optional))
    Loc_Packet = Packet[:]                                                                      # Copy the packet to a local list
    global Full_File_Size_Ran
    if Full_File_Size_Ran == 0:                                                                 # Don't get the full size more than once in or amount of generations more than once
        global Full_File_Size
        for i in range(File_Size):
            Full_File_Size = Full_File_Size + (Loc_Packet[i] * (256**(File_Size - 1 - i)))      # Get full file size out of file size headers
        Gen_Total = Floor_Div_Round_Up(Full_File_Size, Generation_File_Size)                    # Get the amount of generations from the header of the first packet
        Gen_Config(Gen_Total)                                                                   # Run the Generation list initiation function
        Full_File_Size_Ran += 1                                                                 # Change this value so this block of code does not run again

    # Get the headers out and set them in a local varaible
    Gen_Num = Loc_Packet[File_Size]
    Gen_Size = Loc_Packet[File_Size + 1]
    Symbol_Size = Loc_Packet[File_Size + 2]

    # Check if the generation has already been decoded, if so don't send the coded symbol through the decoding algorithm
    global Generations_Decoded
    if Generations_Decoded[Gen_Num] == 1:
        print("Generation already decoded. Packet discarded")                                   # Print feedback
        return 2                                                                                # 2 as a result tells the program to move into checking if all generations were decoded and making the file

    # Get the coefficients out of the header and set them in a local list
    Coefficients_Start = File_Size + 3                                                          # Set where the coefficients start in the packet
    Coefficients_End =  File_Size + 3 + Floor_Div_Round_Up(Gen_Size, 8)                         # Set where the coefficients end in the packet
    Coefficients = Loc_Packet[Coefficients_Start:Coefficients_End]                              # Get the coefficients vector out

    # Increase the number of packets used by one
    Packets_Needed_To_Decode_Generation[Gen_Num] += 1                                           # This is used to give feedback on the number of packets used to decode the generation

    # Make the coefficients list into a list of bits
    Coefficients_bits = Bytes_to_Bits(Coefficients)
    for i in range(len(Coefficients_bits) - Gen_Size):
        Coefficients_bits.pop(0)                                                                # Remove the extra bits at the start

    # Make a local list with the coded symbol
    Symbol_Start = File_Size + 3 + Floor_Div_Round_Up(Gen_Size, 8)                              # Set where the symbols start in the packet
    Symbol = Loc_Packet[Symbol_Start:]                                                          # Get the coded symbol out
    if Symbol_Size != len(Symbol):                                                              # Checks if the coded packet is missing anything from the symbol
        print("Packet_Remove_Header ERROR: Size of data in symbol is not same as in header. Packet will not be used")
        return -1                                                                               # Return a fail code
    Pivot_Position_Config(Gen_Num, Gen_Size)                                                    # Run the pivot position list initializing function with this designated generation

    # Create the coded symbol that has to be guassian eliminated (Coefficients vector + coded symbol)
    Coded_Symbol = Coefficients_bits
    for i in range(len(Symbol)):
        Coded_Symbol.append(Symbol[i])

    # Gaussian eliminate packet and add it to generation

    #print("Decoding algorithm start:\n")
    Res = Generations_Decode(Coded_Symbol, Gen_Num, Gen_Size)
    if Res == -1:                                                                               # If symbol was discraded
        print("Decoding algorithm end.\nResult: Packet discarded \n")
    elif Res == 1:                                                                              # If symbol was inserted
        print("Decoding algorithm end.\nResult: Packet inserted \n")
    else:
        print("Decoding algorithm end.\nResult: Unknown result \n")

    # Check if the generation was fully decoded

    if len(Generations[Gen_Num]) == Gen_Size:
        global Pivot_Pos
        Num_Pivots = Pivot_Pos[Gen_Num][0]                                                      # This variable contains the number of pivot positions that the echelon form generation has, which should be equal to the generation size
        for i in range(len(Pivot_Pos[Gen_Num]) - 1):                                            # This loop adds the number of pivot positions to Num_Pivots
            Num_Pivots = Num_Pivots + Pivot_Pos[Gen_Num][i + 1]                                 
        if Num_Pivots != Gen_Size:                                                              # If the generation failed in becoming echelon form then send feedback
            print("There is a bug, the generation has enough symbols inside, but they do not form a pivot position \n")
        else:                                                                                   # Else send feedback on the amount of packets needed to reduce the generation and reduce the generation into reduced echelon form
            print("Number of packets needed to reduce generation number " + str(Gen_Num) + " is: " + str(Packets_Needed_To_Decode_Generation[Gen_Num]) + "\n")
            Sorted_Generation = Generations_Sort(Gen_Num, Gen_Size)                             # Sort the generation before reducing it to reduced echelon form
            if Sorted_Generation == -1:                                                         # If the sorting failed then send feedback that it failed
                print("Sorting Generation " + str(Gen_Num) + " failed \n")
            else:                                                                               # Else send feedback that the sorting succeeded
                print("Sorting Generation " + str(Gen_Num) + " Succeeded \n")
                Res = Generations_Complete_Reduce(Sorted_Generation, Gen_Num, Gen_Size, Symbol_Size)    # Reduce the generation into reduced echelon form
                if Res == 1:                                                                    # If it returns a success then send feedback that it succeeded
                    print("Generation reduced to reduced echelon form and uncoded symbols appended to Full_File_Data \n")
                    return 2                                                                    # 2 as a result tells the program to move into checking if all generations were decoded and making the file
                else:                                                                           # Else send feedback with the different value it returned
                    print("The Generations_Complete_Reduce function returned an unexpected value. The value is: " + str(Res) + "\n")




# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('c46d071ad49b09ce5d776f2981349ba0')

# Initialise LoRa in LORAWAN Class C mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, device_class=LoRa.CLASS_C)

# Restoring previous lora sessions
lora.nvram_restore()

# Join the network
if not lora.has_joined():
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)
    timeOut = 0
    while not lora.has_joined():
        timeOut += 1
        time.sleep(1)
        print('Not yet joined...')
        if timeOut == 20:
            sys.exit()

print("Connected.")

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the LoRaWAN data rate to DR 0 = SF12BW125
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

Test_Int = 69
pkg = struct.pack('i', Test_Int)

#Send the package
try:
    s.send(pkg)
except OSError as e:
    if e.args[0] == 11:
        print("error sending")

# make the socket non-blocking (because if there's no data received it will block forever...)


s.setblocking(False)


# ------------------------------------------------Error Messages---------------------------------------------------
# Error_Message3 = File name error (Does not contain the .)
# --------------------------------------------------Not in use-----------------------------------------------------

# Try and receive a message from the server and check if it is telling the sensor to go into update mode
# This can be explored later to make a proper functional system, it is not needed for testing

#Received_Message = s.recv(64)
#Received_Message_List = list(Recieved_Message)
#if bytes(Received_Message_List[0:12]) == b'Update_Start':
#   File_Name_List = Received_Message_List
#   File_Name_Error_Sent = 0
#   if File_Name_List_count(.) > 0:
#       Update_Status = 1
#   else:
#       while File_Name_Error_Sent == 0:
#           try:
#               pkg = struct.pack("b", b'Error_Message3')
#               s.send(pkg)
#               File_Name_Sent_Error = 1
#           except OSError as e:
#               if e.args[0] == 11:
#                   print("error sending")
#else:
#   Update_Status = 0

Update_Status = 1                                                   # Set the update status to on. Make this variable 0 if you don't want the lopy to update. Comment it if you want to use the system right above it
print("Update status is: " + str(Update_Status))                    # Print the update status out
# If update mode is on then go into a file receiving loop

while Update_Status == 1:
    Packet_Byte = s.recv(64)                                        # Receive the packet in byte for
    if Packet_Byte == b'':                                          # If packet is empty try and receive a new packet
        continue
    else:
        Packet = list(Packet_Byte)                                  # Put packet in list
        print("Packet received:")                                   # Print that the packet was received
        print(Packet)                                               # Print the packet that was received
        print("\n")
        Res = Sort_Packets(Packet)                                  # Send the packet throught the decoding algorithm

    if Res == 2:                                                    # If the generation has been decoded
        print("Generation " + str(Gen_Num) + " decoded")            # Print which generation was decoded

        # Send message telling it to move to the next generation
        # Uncomment this part once we find out how to receive messages on the computer

        #pkg = struct.pack('Iib', generationDone = 1)
        #try:
        #    s.send(pkg)
        #except OSError as e:
        #    if e.args[0] == 11:
        #        print("error sending")
        #time.sleep(1)
    else:                                                           # If generation is not done start from the start of the while loop
        continue

    Sum_Gen_Decoded = 0                                             # This variable has the number of generations that were decoded
    for i in range(len(Generations)):                               # Put all the number of generations together
        Sum_Gen_Decoded += Generations_Decoded[i]
    if Sum_Gen_Decoded == len(Generations):                         # If all generations are decoded (Sum of elements in the list is equal to its length) Then start with making the file
        print("All generations are decoded")                        # Print that all the generations were decoded
            
        # Make file using the file name and send that the file has been decoded
        
        File_Name = "Update.py"                                     # File name assigned manually for now
        File_Open = open(File_Name, "wb")                           # Open file in write mode to completely wipe the file if it already exists
        
        # Write the data from the decoded symbols into one full list and remove the extra zeros
        
        for i in range(len(Full_File_Data)):
            for j in range(len(Full_File_Data[i])):
                File_Data_List.append(Full_File_Data[i][j])
        if len(File_Data_List) >= Full_File_Size:                   # Check if the list of data is larger or equal to the file size from the header
            for i in range(len(File_Data_List) - Full_File_Size):
                File_Data_List.pop(-1)
        else:                                                       # If not, then there was an error with the decoder
            print("Algorithm says all generations decoded, but the file is not complete")
        
        File_Open.write(bytes(File_Data_List))                      # Write everything in the file
        File_Open.close()                                           # Close the file to save it

        # Try and send the Update Done message for 30 seconds, once every second. This is used to stop the computer from sending packets
        # Uncomment this part once we find out how to receive messages on the computer

        #for i in range(30):
        #    pkg = struct.pack('b', b'Update_Done')
        #    try:
        #        s.send(pkg)
        #    except OSError as e:
        #        if e.args[0] == 11:
        #            print("error sending")
        #    time.sleep(1)
        Update_Status = 0                                           # Set the update status to off


print("Update status is: " + str(Update_Status))                    # Print the update status out
#execfile(File_Name)                        # Dangerous. It is possible to brick the LoPy by running the sent file. Only used for showcasing

# This program has been tested. The amount of prints have crashed the LoPy. Therefore the prints have been commented
