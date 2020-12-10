# This file should use the encoding function to take a file and split it into encoded packets with extra redundant packets (For now 100 packets per generation)

from File_Splitting import Split_File, Split_Generation
from Random_Matrix import Random_1D_Bit_Matrix
from Encode_Symbol import Encode_Symbol, Send_File_Error

#File = open("C:\\Users\moham\Desktop\LoPy files\main to decode.py","rb+")
File = open("C:\\Users\moham\Desktop\Gimp\Knuckeles.png","rb+")
ReadFile = File.read()
ListFile = list(ReadFile)
FileSize = len(ListFile)

Generations = Split_File(ListFile)

for i in range(len(Generations)):
    Symbols = Split_Generation(Generations[i])
    print(Symbols)
    Packets_Per_Gen = 100
    for j in range(Packets_Per_Gen):
        File_Directory = "C:\\Users\moham\Desktop\LoPy files\Packets Knuckles\Packet" + str(i * Packets_Per_Gen + j) + ".bin"
        File_Encode = open(File_Directory, "wb")
        File_Encode.close()
        File_Encode = open(File_Directory,"ab")
        Enc_Vec = Random_1D_Bit_Matrix(len(Symbols), 0.1)
        x = Encode_Symbol(Symbols, Enc_Vec, FileSize, i)
        b = bytes(x)
        print(b)
        File_Encode.write(b)
        File_Encode.close()

"""
for i in range(len(Generations)):
    Symbols = Split_Generation(Generations[i])
    print(Symbols)
    Packets_Per_Gen = len(Symbols)
    for j in range(Packets_Per_Gen):
        File_Directory = "C:\\Users\moham\Desktop\LoPy files\Packets Knuckles\Packet" + str(i * 32 + j) + ".bin"
        File_Encode = open(File_Directory, "wb")
        File_Encode.close()
        File_Encode = open(File_Directory,"ab")
        Enc_Vec = []
        for k in range(Packets_Per_Gen):
            if j == k:
                Enc_Vec.append(1)
            else:
                Enc_Vec.append(0)
        x = Encode_Symbol(Symbols, Enc_Vec, FileSize, i)
        b = bytes(x)
        print("Generation: " + str(i) + " Packet: " + str(j) +" Encoded")
        print("Packet name: Packet" + str(i * 32 + j) + ".bin")
        print(b)
        File_Encode.write(b)
        File_Encode.close()
"""
