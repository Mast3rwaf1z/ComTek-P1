from network import LoRa
import pycom
import socket
import time
import ubinascii
import struct
import sys

File_Size_Arg = 3                                   # Change this according to how many bytes in the header are used to indicate the file size
Generation_File_Size = 32*40                        # This is manually assigned, as I can't care anymore (Can be fixed by sending it from the gateway)
Generations = []                                    # 3D matrix that holds a list of generations, which hold a list of the symbols
Generations_Decoded = []                            # This 1D matrix indicates which generation have been decode, to not send any more coded symbols ot them
Full_File_Size_Ran = 0                              # Is 1 when the variable is assigned, because don't mess with the global variabl grr
Full_File_Size = 0                                  # Had to become a global variable, as it is used in more than one function
Full_File_Data = []                                 # This 2D matrix has all the decoded data from each generation in order. Will be combined in the end to one file
File_Data_List = []                                 # This list contains everything in Full_File_Data but in one list, this is to pop out the extra bits at the end
Pivot_Pos = []                                      # A list of generations, which contains the info on pivot positions. 1 = yes pivot, 0 =  no pivot
Pivot_Pos_Ran = []                                  # Is 1 when the pivot position is filled with with pivot variables
Packets_Needed_To_Decode_Generation = []
File_Name = "Insert file name here.py"

# Converts a list of decimal bytes (Bytearray) into a list of zeros and ones
def Bytes_to_Bits(ByteList):                #Argument(List with bytes)
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

# This function need to be adjusted beforehand, now it only works for generation size 32, symbol size 40
# A way to make it work is to send some info in an initial packet. If there is time it will be explored
def Gen_Config(Gen_Total):
    for i in range(Gen_Total):
        Generations.append([])                      # Fill the list with the generation lists (Initiate generation list)
        Full_File_Data.append([])                   # Fill list with enough place for each generation (Initiate Fill_File_Data list)
        Pivot_Pos.append([])                        # Fill the list with the generation pivot lists (Initiate Pivot_Pos list)
        Pivot_Pos_Ran.append(0)                     # Fill the list with zero states (Initiate Pivot_Pos_Ran list)
        Generations_Decoded.append(0)               # Fill the list with zero states (Initiate Generations_Decoded list)
        Packets_Needed_To_Decode_Generation.append(0)


def Pivot_Position_Config(Gen_Num, Gen_Size):
    if Pivot_Pos_Ran[Gen_Num] == 0:                 # If the designated generation list was not filled, the proceed else do nothing
        for i in range(Gen_Size):
            Pivot_Pos[Gen_Num].append(0)            # Set 0s with the number of pivot positions in the generation
        Pivot_Pos_Ran[Gen_Num] = 1                  # Don't run this again for the same generation

def Generations_Sort(Gen_Num, Gen_Size, Symbol_Size):
    Loc_Gen = Generations[Gen_Num][:]
    Sorted_Gen = []
    for i in range(Gen_Size):
        Sorted_Gen.append([])

    # Sort the generation

    for i in range(Gen_Size):
        Sorting_Pos = Loc_Gen[i][0]
        for j in range(len(Loc_Gen[i])):
            Sorted_Gen[Sorting_Pos].append(Loc_Gen[i][j])

    # Check that it has sorted correctly, if yes pop out the pivot position indicator

    for i in range(Gen_Size):
        if Sorted_Gen[i][0] == i:
            Sorted_Gen[i].pop(0)
        else:
            print("There is a bug, the sorting algorithm has failed to sort the generation")
            return -1

    # Reduce to reduced echelon form

    for i in range(len(Sorted_Gen) - 1, 0, -1):                                # The bottom symbol
        a = Sorted_Gen[i][:]
        for j in range(i):                                                      # The upper symbols
            if Sorted_Gen[j][i] == 1:
                b = Sorted_Gen[j][:]
                Sorted_Gen[j] = bytes([a ^ b for a, b in zip(a, b)])

    # Append all the symbol data into the Full_File_Data list

    for i in range(Gen_Size):
        for j in range(Symbol_Size):
            Full_File_Data[Gen_Num].append(Sorted_Gen[i][Gen_Size + j])
    Generations_Decoded[Gen_Num] = 1
    return 1

def Generations_Decode(Coded_Symbol, Gen_Num, Gen_Size):
    Loc_Symbol = Coded_Symbol[:]
    Useless_Symbol = 0
    Position = -1

    # Check the position of the first 1, if there are not 1s then it is useless

    for i in range(Gen_Size):
        if Loc_Symbol[i] == 1:
            Useless_Symbol = 0
            Position = i
            break
        else:
            Useless_Symbol = 1
    if Useless_Symbol == 1:
        return -1

    # Check if this can be used without reducing it (It can make a pivot position without reducing)

    if Pivot_Pos[Gen_Num][Position] == 0:
        Pivot_Pos[Gen_Num][Position] = 1
        Loc_Symbol.insert(0, Position)
        #Loc_Symbol.insert(0, Gen_Size)                         # Might not be needed, if we supply this to the sorting thing directly
        Generations[Gen_Num].append(Loc_Symbol)
        return 1

    # Go and do the reduction using all currently available packets in the generation (You will have to remove the 2 things at the start again)

    a = Loc_Symbol[:]
    for i in range(len(Generations[Gen_Num])):
        Initial_Pivot_Pos = Generations[Gen_Num][i][0]          # Might not be needed, if we supply this to the sorting thing directly (Switched from 1 to 0)
        if a[Initial_Pivot_Pos] == 1:
            b = Generations[Gen_Num][i][:]
            b.pop(0)
            #b.pop(0)                                           # Might not be needed, if we supply this to the sorting thing directly
            a = bytes([a ^ b for a, b in zip(a, b)])
    a = list(a)
    Loc_Symbol = a[:]

    # After it is reduced do the same check for the position of 1

    for i in range(Gen_Size):
        if Loc_Symbol[i] == 1:
            Useless_Symbol = 0
            Position = i
            break
        else:
            Useless_Symbol = 1
    if Useless_Symbol == 1:
        return -1

    # One last check that can be deleted later

    if Pivot_Pos[Gen_Num][Position] == 0:
        Pivot_Pos[Gen_Num][Position] = 1
        Loc_Symbol.insert(0, Position)
        #Loc_Symbol.insert(0, Gen_Size)                          # Might not be needed, if we supply this to the sorting thing directly
        Generations[Gen_Num].append(Loc_Symbol)
        return 1
    else:
        print("There is a bug in the system, the thing got reduced and still did not get a unique pivot position. For some reason it still works with this bug.")
        return -1


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

    # The thing bellow is useless. It is already part of the main function.
    #global Generations_Decoded
    #if Generations_Decoded[Gen_Num] == 1:
    #    print("Generation " + str(Gen_Num) +  " Decoded")
        # Send back a special message to say generation is decoded and to go into the next generation
    #    return 2

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
            Res = Generations_Sort(Gen_Num, Gen_Size, Symbol_Size)
            if Res == 1:
                print("Sorting Generation " + str(Gen_Num) + " Succeeded")
            elif Res == -1:
                print("Sorting Generation " + str(Gen_Num) + " failed")
            else:
                print("Unknown error code from generations sorting function. Error code is: " + str(Res))



# create an OTAA authentication parameters
dev_eui = ubinascii.unhexlify('be3f661454d53eae')           # possibly the wrong value but the uplink transmissions work without it
app_eui = ubinascii.unhexlify('0000000000000000')
#app_key = ubinascii.unhexlify('ffea46d69b39a495b4b16d69390c9b17')
#app_key = ubinascii.unhexlify('cd4005ab70fa0a1e940cf29f7204b0e3')
app_key = ubinascii.unhexlify('c46d071ad49b09ce5d776f2981349ba0')

# Initialise LoRa in LORAWAN mode.
#lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, device_class=LoRa.CLASS_C)
# Restoring previous lora sessions
lora.nvram_restore()

# Join the network
if not lora.has_joined():
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)
    # lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=0)
    timeOut = 0
    while not lora.has_joined():
        timeOut += 1
        time.sleep(1)
        print('Not yet joined...')
        if timeOut == 20:
            sys.exit()

print("Connected!")

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the LoRaWAN data rate to DR 0 = SF12BW125
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

battery = 93
fullness = 47
temperature = 26

pkg = struct.pack('Iib',battery,fullness,temperature)
# pkg = struct.pack('iii', 1, 2, 3)

#Send the package
try:
    s.send(pkg)
except OSError as e:
    if e.args[0] == 11:
        print("error sending")

# make the socket non-blocking (because if there's no data received it will block forever...)


s.setblocking(False)


# ------------------------------------------------Error Messages---------------------------------------------------
# Error_Message0
# Error_Message1
# Error_Message2
# Error_Message3 = File name error (Does not contain the .)


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

Update_Status = 1                               # Make this variable 0 if you don't want the lopy to update. Comment it if you want to use the system right above it
Gen_Num = 0                                     # Shows the generation that the sensor is recieving from

# If update mode is on then go into a file receiving loop
while Update_Status == 1:
    Packet_Byte = s.recv(64)                    # Receive the packet in byte for
    if Packet_Byte == b'':                      # If packet is empty try and receive a new packet
        #print(Packet_Byte)
        continue
    else:
        Packet = list(Packet_Byte)              # Put packet in list
        print("Packet received")
        print(Packet)
        Sort_Packets(Packet, File_Size_Arg)

    print("Is the generation decoded? " + str(Generations_Decoded[Gen_Num]))
    if Generations_Decoded[Gen_Num] == 1:       # If the generation has been decoded send that info to the source so it stops sending packets from this generation and start with a new generation
        print("Generation" + str(Gen_Num) + " decoded")
        # Send message telling it to move to the next generation
        pkg = b'Generation_Done'
        #pkg = struct.pack('b', b'Generation_Done')                 # This is used to turn numbers into bytes, therefore it is useless to use it on bytes
        try:
            s.send(pkg)
        except OSError as e:
            if e.args[0] == 11:
                print("error sending")
        #time.sleep(1)
    else:                                       # If generation is not done start from the start of the while loop
        continue

    Sum_Gen_Decoded = 0
    for i in range(len(Generations)):           # Put all the number of generations together
        Sum_Gen_Decoded += Generations_Decoded[i]
    if Sum_Gen_Decoded == len(Generations):     # If all generations are decoded (Sum of elements in the list is equal to its length) The start with making the file
        # Make file using the file name and send that the file has been decoded

        print("All generations are decoded")
        File_Name = "Update.py"                 # File name assigned manually for now, as the code to receive from the server is not completed

        File_Open = open(File_Name, "wb")       # Open file in write mode to completely wipe the file if it already exists
        #File_Open.close()
        #File_Open = open(File_Name, "ab")       # Open the now empty file in append mode to put the data in it. Might not be needed
        # Append the data from the generation into one full list and remove the extra zeros
        for i in range(len(Full_File_Data)):
            for j in range(len(Full_File_Data[i])):
                File_Data_List.append(Full_File_Data[i][j])
        if len(File_Data_List) >= Full_File_Size:
            for i in range(len(File_Data_List) - Full_File_Size):
                File_Data_List.pop(-1)
        else:
            print("Algorithm says all generations decoded, but the file is not complete")
        print(bytes(File_Data_List))
        File_Open.write(bytes(File_Data_List))  # Write everything in the file
        File_Open.close()
        # The part bellow is not so good, the lopy waits for the computer to send a message, but the computer does not know if the lopy received it
        # Therefore the lopy might get stuck in update mode if we let the computer send only a certain amount of the message before stopping
        # Therefore it is a better idea to let the lopy send a certain amount of the message instead, the computer getting stuck is a better alternative
        """
        Update_Done = 0
        while Update_Done == 0:                 # This part is for if the message that the last packet has been decoded fails to send
            pkg = struct.pack('b', b'Update_Done')
            try:
                s.send(pkg)
            except OSError as e:
                if e.args[0] == 11:
                    print("error sending")
            Received_Message = s.recv(64)
            if Received_Message == b'Update_Done':
               Update_Done = 1
            else:
               Update_Done = 0
        Update_Status = 0
        """

        # Try and send the Update Done message for 30 seconds, once every second. This is used to stop the computer from sending packets
        for i in range(30):
            pkg = b'Update_Done'
        #    pkg = struct.pack('b', b'Update_Done')
            try:
                s.send(pkg)
            except OSError as e:
                if e.args[0] == 11:
                    print("error sending")
            time.sleep(0.2)
        Update_Status = 0
# Uncomment section under if the new update file is empty
"""
File_read = open(File_Name, "rb")
File_Read = File_read.read()
print("File read")
print(File_Read)
File_Read.close()
File_Write_Attempts = 0

while File_Read == b'' and File_Write_Attempts < 10:
    File_Open = open(File_Name, "ab")       # Open the now empty file in append mode to put the data in it. Might not be needed
    File_Open.write(bytes(File_Data_List))
    File_Open.close()
    File_read = open(File_Name, "rb")
    File_Read = File_read.read()
    print("File read again")
    print(File_Read)
    File_Write_Attempts += 1
if File_Write_Attempts > 9:
    print("Could not write anything in file. File will be empty")
else:
    print("File has stuff in it")
"""

#execfile(File_Name)                        # Dangerous. It is possible to brick the LoPy by running the sent file. Only used for showcasing
