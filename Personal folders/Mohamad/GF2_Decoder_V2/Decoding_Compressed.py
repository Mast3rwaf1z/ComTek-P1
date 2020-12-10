from time import sleep

File_Size_Arg = 3
Generation_File_Size = 32*40        # Might not be needed
Generations = []
Generations_Decoded = []
Full_File_Size_Ran = 0
Full_File_Size = 0
Full_File_Data = []
Pivot_Pos = []
Pivot_Pos_Ran = []
Packets_Needed_To_Decode_Generation = []

def Bytes_to_Bits(ByteList):
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

def Floor_Div_Round_Up(x, y):
    a = x / y
    b = x // y
    if a != b:
        return b+1
    else:
        return b

def Gen_Config(Gen_Total):
    for i in range(Gen_Total):
        Generations.append([])
        Full_File_Data.append([])
        Pivot_Pos.append([])
        Pivot_Pos_Ran.append(0)
        Generations_Decoded.append(0)
        Packets_Needed_To_Decode_Generation.append(0)

def Pivot_Position_Config(Gen_Num, Gen_Size):
    if Pivot_Pos_Ran[Gen_Num] == 0:
        for i in range(Gen_Size):
            Pivot_Pos[Gen_Num].append(0)
        Pivot_Pos_Ran[Gen_Num] = 1

def Generations_Sort(Gen_Num, Gen_Size, Symbol_Size):
    Loc_Gen = Generations[Gen_Num][:]
    Sorted_Gen = []
    for i in range(Gen_Size):
        Sorted_Gen.append([])

    for i in range(Gen_Size):
        Sorting_Pos = Loc_Gen[i][0]
        for j in range(len(Loc_Gen[i])):
            Sorted_Gen[Sorting_Pos].append(Loc_Gen[i][j])

    for i in range(Gen_Size):
        if Sorted_Gen[i][0] == i:
            Sorted_Gen[i].pop(0)
        else:
            print("There is a bug, the sorting algorithm has failed to sort the generation")
            return -1

    for i in range(len(Sorted_Gen) - 1, 0, -1):
        a = Sorted_Gen[i][:]
        for j in range(i):
            if Sorted_Gen[j][i] == 1:
                b = Sorted_Gen[j][:]
                Sorted_Gen[j] = bytes([a ^ b for a, b in zip(a, b)])

    for i in range(Gen_Size):
        for j in range(Symbol_Size):
            Full_File_Data[Gen_Num].append(Sorted_Gen[i][Gen_Size + j])
    Generations_Decoded[Gen_Num] = 1
    return 1

def Generations_Decode(Coded_Symbol, Gen_Num, Gen_Size):
    Loc_Symbol = Coded_Symbol[:]
    Useless_Symbol = 0
    Position = -1

    for i in range(Gen_Size):
        if Loc_Symbol[i] == 1:
            Useless_Symbol = 0
            Position = i
            break
        else:
            Useless_Symbol = 1
    if Useless_Symbol == 1:
        return -1

    if Pivot_Pos[Gen_Num][Position] == 0:
        Pivot_Pos[Gen_Num][Position] = 1
        Loc_Symbol.insert(0, Position)
        Generations[Gen_Num].append(Loc_Symbol)
        return 1

    a = Loc_Symbol[:]
    for i in range(len(Generations[Gen_Num])):
        Initial_Pivot_Pos = Generations[Gen_Num][i][0]
        if a[Initial_Pivot_Pos] == 1:
            b = Generations[Gen_Num][i][:]
            b.pop(0)
            a = bytes([a ^ b for a, b in zip(a, b)])
    Loc_Symbol = a[:]
    Loc_Symbol = list(Loc_Symbol)

    for i in range(Gen_Size):
        if Loc_Symbol[i] == 1:
            Useless_Symbol = 0
            Position = i
            break
        else:
            Useless_Symbol = 1
    if Useless_Symbol == 1:
        return -1

    if Pivot_Pos[Gen_Num][Position] == 0:
        Pivot_Pos[Gen_Num][Position] = 1
        #print(Loc_Symbol)
        Loc_Symbol.insert(0, Position)
        Generations[Gen_Num].append(Loc_Symbol)
        return 1
    else:
        print("There is a bug in the system, the thing got reduced and still did not get a unique pivot position")
        return -1

def Sort_Packets(Packet, File_Size):
    Loc_Packet = Packet[:]
    global Full_File_Size_Ran
    if Full_File_Size_Ran == 0:
        global Full_File_Size
        for i in range(File_Size):
            Full_File_Size = Full_File_Size + (Loc_Packet[i] * (255**(File_Size - 1 - i)))
        print(Full_File_Size_Ran)
        Gen_Total = Floor_Div_Round_Up(Full_File_Size, Generation_File_Size)                        # Generatin file size might not be needed, if the thing sends packets from the first generation first, which is the plan currently
        Gen_Config(Gen_Total)
        Full_File_Size_Ran += 1
        #print("Full file size 1")
        #print(Full_File_Size)

    Gen_Num = Loc_Packet[File_Size]
    Gen_Size = Loc_Packet[File_Size + 1]
    Symbol_Size = Loc_Packet[File_Size + 2]

    global Generations_Decoded
    if Generations_Decoded[Gen_Num] == 1:
        print("Generation " + str(Gen_Num) +  " Decoded")
        # Send back a special message to say generation is decoded and to go into the next generation
        return 2

    print("Generation number: " + str(Gen_Num) + " Packet number: " + str(Packets_Needed_To_Decode_Generation[Gen_Num]))

    Coefficients_Start = File_Size + 3
    Coefficients_End =  File_Size + 3 + Floor_Div_Round_Up(Gen_Size, 8)
    Coefficients = Loc_Packet[Coefficients_Start:Coefficients_End]

    Packets_Needed_To_Decode_Generation[Gen_Num] += 1

    Coefficients_bits = Bytes_to_Bits(Coefficients)
    for i in range(len(Coefficients_bits) - Gen_Size):
        Coefficients_bits.pop(0)

    Symbol_Start = File_Size + 3 + Floor_Div_Round_Up(Gen_Size, 8)
    Symbol = Loc_Packet[Symbol_Start:]
    if Symbol_Size != len(Symbol):
        print("Packet_Remove_Header ERROR: Size of data in symbol is not same as in header. Packet will not be used")
        return -1
    Pivot_Position_Config(Gen_Num, Gen_Size)

    Coded_Symbol = Coefficients_bits
    for i in range(len(Symbol)):
        Coded_Symbol.append(Symbol[i])

    Res = Generations_Decode(Coded_Symbol, Gen_Num, Gen_Size)
    if Res == -1:
        print("Packet discarded")
    if Res == 1:
        #print("Packet inserted")
        x = 1
    else:
        print("Unknown result")

    if len(Generations[Gen_Num]) == Gen_Size:
        #sleep(0.4)
        global Pivot_Pos
        Num_Pivots = Pivot_Pos[Gen_Num][0]
        for i in range(len(Pivot_Pos[Gen_Num]) - 1):
            Num_Pivots = Num_Pivots + Pivot_Pos[Gen_Num][i + 1]
        if Num_Pivots != Gen_Size:
            print("There is a bug, the generation has enough symbols inside, but they do not form a pivot position")
        else:
            print("Packets needed to reduce generation number " + str(Gen_Num) + " is: " + str(Packets_Needed_To_Decode_Generation[Gen_Num]))
            Res = Generations_Sort(Gen_Num, Gen_Size, Symbol_Size)
            if Res == 1:
                print("Sorting Generation " + str(Gen_Num) + " Succeeded")
            elif Res == -1:
                print("Sorting Generation " + str(Gen_Num) + " failed")
            else:
                print("Unknown error code from generations sorting function. Error code is: " + str(Res))

"""
File_Data_List = []

for i in range(200):
    File_Directory = "C:\\Users\moham\Desktop\LoPy files\Packets\Packet" + str(i) + ".py"
    Packet_Open = open(File_Directory, "rb")
    Packet_Read = Packet_Open.read()
    Packet_List = list(Packet_Read)
    Packet_Open.close()
    Sort_Packets(Packet_List, 3)

print(Full_File_Data)

for i in range(len(Full_File_Data)):
    for j in range(len(Full_File_Data[i])):
        File_Data_List.append(Full_File_Data[i][j])
print("Full file size 2")
print(Full_File_Size)
print(len(File_Data_List))
print(len(File_Data_List) - Full_File_Size)

for i in range(len(File_Data_List) - Full_File_Size):
    File_Data_List.pop(-1)

print("Full file size 2")
print(Full_File_Size)
print(len(File_Data_List))
print(len(File_Data_List) - Full_File_Size)

File_Decoded = open("C:\\Users\moham\Desktop\LoPy files\Packets\Decoded_File.py", "wb")
File_Decoded.close()
File_Decoded = open("C:\\Users\moham\Desktop\LoPy files\Packets\Decoded_File.py", "ab")
b = bytes(File_Data_List)
print(b)
File_Decoded.write(b)

#Use this section later as it is the last building block to finish the program in the lopy
"""

File_Data_List = []

for i in range(3668):
    File_Directory = "C:\\Users\moham\Desktop\LoPy files\Packets Knuckles\Packet" + str(i) + ".bin"
    print("Reading file number: " + str(i))
    Packet_Open = open(File_Directory, "rb")
    Packet_Read = Packet_Open.read()
    Packet_List = list(Packet_Read)
    print(Packet_List)
    Packet_Open.close()
    Sort_Packets(Packet_List, 3)

print(Full_File_Data)

for i in range(len(Full_File_Data)):
    for j in range(len(Full_File_Data[i])):
        File_Data_List.append(Full_File_Data[i][j])
print("Full file size 2")
print(Full_File_Size)
print(len(File_Data_List))
print(len(File_Data_List) - Full_File_Size)
if (len(File_Data_List) - Full_File_Size) > 0:
    for i in range(len(File_Data_List) - Full_File_Size):
        File_Data_List.pop(-1)

print("Full file size 2")
print(Full_File_Size)
print(len(File_Data_List))
print(len(File_Data_List) - Full_File_Size)

File_Decoded = open("C:\\Users\moham\Desktop\LoPy files\Packets Knuckles\Decoded_File.png", "wb")
File_Decoded.close()
File_Decoded = open("C:\\Users\moham\Desktop\LoPy files\Packets Knuckles\Decoded_File.png", "ab")
b = bytes(File_Data_List)
print(b)
File_Decoded.write(b)
