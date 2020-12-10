from Decoding_Compressed import Sort_Packets, Full_File_Data, Full_File_Size

File_Data_List = []

for i in range(200):
    File_Directory = "C:\\Users\moham\Desktop\LoPy files\Packets\Packet" + str(i) + ".py"
    Packet_Open = open(File_Directory, "rb")
    Packet_Read = Packet_Open.read()
    Packet_List = list(Packet_Read)
    Packet_Open.close()
    Sort_Packets(Packet_List, 3)

#for i in range(Full_File_Size - len(File_Data_List)):
#    File_Data_List.pop(-1)
print(Full_File_Data)

for i in range(len(Full_File_Data)):
    for j in range(len(Full_File_Data[i])):
        File_Data_List.append(Full_File_Data[i][j])
print("Full file size 2")
print(Full_File_Size)
print(len(File_Data_List))
print(Full_File_Size - len(File_Data_List))

File_Decoded = open("C:\\Users\moham\Desktop\LoPy files\Packets\Decoded_File.py", "wb")
File_Decoded.close()
File_Decoded = open("C:\\Users\moham\Desktop\LoPy files\Packets\Decoded_File.py", "ab")
b = bytes(File_Data_List)
print(b)
File_Decoded.write(b)


# Could not get the full file size, so I had to run it in the same file
