Test_Packet = [2, 65, 233, 94, 32, 40, 29, 154, 179, 131, 149, 237, 97, 184, 243, 247, 135, 64, 91, 216, 166, 53, 64, 147, 171, 25, 11, 60, 106, 143, 226, 36, 142, 121, 231, 110, 85, 242, 163, 155, 49, 141, 173, 8, 115, 228, 216, 165, 57, 106]
Test_Packet2 = [2, 65, 233, 114, 19, 40, 5, 16, 146, 33, 242, 75, 250, 250, 94, 233, 84, 29, 143, 33, 82, 196, 112, 23, 8, 125, 224, 56, 63, 230, 145, 140, 123, 53, 158, 8, 146, 157, 89, 62, 245, 246, 228, 11, 225, 227, 81, 85, 230]

File_Size_Arg = 3                                   # Change this according to how many bytes in the header are used to indicate the file size
Generation_File_Size = 32*40                        # This is manually assigned, as I can't care anymore (Can be fixed by sending it from the gateway)
Generations = []                                    # 3D matrix that holds a list of generations, which hold a list of the symbols
Generations_Decoded = []                            # This 1D matrix indicates which generation have been decode, to not send any more coded symbols ot them
Full_File_Size_Ran = 0                              # Is 1 when the variable is assigned, because don't mess with the global variabl grr
Full_File_Size = 0                                  # Had to become a global variable, as it is used in more than one function
Full_File_Data = []                                 # This 2D matrix has all the decoded data from each generation in order. Will be combined in the end to one file
Pivot_Pos = []                                      # A list of generations, which contains the info on pivot positions. 1 = yes pivot, 0 =  no pivot
Pivot_Pos_Ran = []                                  # Is 1 when the pivot position is filled with with pivot variables
Packets_Needed_To_Decode_Generation = []
