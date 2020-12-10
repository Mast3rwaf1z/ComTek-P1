from File_Splitting import Split_File, Split_Generation
from Random_Matrix import Random_1D_Bit_Matrix
from Encode_Symbol import Encode_Symbol, Send_File_Error

File = open("C:\\Users\moham\Desktop\LoPy files\main to decode.py","rb+")
#File = open("C:\\Users\moham\Desktop\Gimp\Knuckeles.png","rb+")
ReadFile = File.read()
ListFile = list(ReadFile)
FileSize = len(ListFile)

Generations = Split_File(ListFile)

All_Encoded_Packets = []
for i in range(len(Generations)):
    Symbols = Split_Generation(Generations[i])
    for j in range(len(Symbols)):
        Enc_Vec = Random_1D_Bit_Matrix(len(Symbols), 0.5)
        x = Encode_Symbol(Symbols, Enc_Vec, FileSize, i)
        All_Encoded_Packets.append(x)

print(All_Encoded_Packets)
print(len(All_Encoded_Packets))
print(len(All_Encoded_Packets[0]))

def dump_Mat(Mat):
    for i in Mat:
        print(i)

dump_Mat(All_Encoded_Packets)
print(Send_File_Error)
print(len(All_Encoded_Packets[-1]))
print(len(All_Encoded_Packets[0]))
File_Encode = open("C:\\Users\moham\Desktop\LoPy files\Packets\main encoded.py","wb")
File_Encode.close()
File_Encode = open("C:\\Users\moham\Desktop\LoPy files\main encoded.py","ab")
for i in range(len(All_Encoded_Packets)):
    b = bytes(All_Encoded_Packets[i])
    print(b)
    File_Encode.write(b)

