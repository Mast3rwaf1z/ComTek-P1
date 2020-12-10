from Matrix_Checks import Check_is_1D_Matrix

# Floor division usually rounds down. This function makes it round up instead
def Floor_Div_Round_Up(x, y):
    a = x / y
    b = x // y
    if a != b:                  # If there are decimals then round up
        return b+1
    else:
        return b

# Function to split a file into Generations
# Output is a 2d matrix with each generation in a list
def Split_File(File, Gen_Size = 32, Symbol_Size = 40):      # Arguments(File to split, Generation size, Symbol size)
    if not Check_is_1D_Matrix(File):                        # Check if file is a bytearray
        print("Split_File ERROR: File is not a bytearray or a list")
        return
    File_Size = len(File)                                   # Get the size of the file in bytes
    No_of_Generation = Floor_Div_Round_Up(File_Size, Gen_Size*Symbol_Size)  # Get the number of generations the file needs to be split into
    Generations = []                                        # Make empty matrix to fill with the generations
    for i in range(No_of_Generation):
        Generations.append([])
        for j in range(Gen_Size*Symbol_Size):
            if i == No_of_Generation-1:                     # If it is the last generation
                if j >= (File_Size - Gen_Size*Symbol_Size*(No_of_Generation - 1)):  # If we have already appended the entire file
                    if len(Generations[i]) % Symbol_Size == 0:                      # If we have enough zeros to make a symbol
                        break
                    else:
                        Generations[i].append(0)                                    # Fill with zeros
                else:
                    Generations[i].append(File[i*Gen_Size*Symbol_Size + j])         # Append normally until file is all appended
            else:
                Generations[i].append(File[i*Gen_Size*Symbol_Size + j])             # Append file contents
    return Generations                                      # Return 2d matrix where each generation is a list inside


# This function splits a generation into a list of symbols
# Output is a 2d matrix with each symbol in a list. Output can be used to create encoded symbols
def Split_Generation(Gen, Symbol_Size = 40):        # Arguments(Generation to split, Symbol size)
    if not Check_is_1D_Matrix(Gen):                 # Check if generation is a bytearray
        print("Split_Generation ERROR: File is not a bytearray or a list")
        return
    Gen_Data_Size = len(Gen)                        # Get the size of the Generation in bytes
    No_of_Symbols = Floor_Div_Round_Up(Gen_Data_Size, Symbol_Size)      # Get the number of symbols the generation will be split into
    Symbol = []                                     # Make empty matrix to fill with symbols
    for i in range(No_of_Symbols):
        Symbol.append([])                           # Create list inside Symbol
        for j in range(Symbol_Size):
            Symbol[i].append(Gen[i*Symbol_Size + j])    # Append data into the symbol
            # This function does not have zero filling, as it is expected to be used after Split_File
    return Symbol                                   # Return a 2d matrix with each symbol as a list of bytes
"""
#File = open("C:\\Users\moham\Desktop\LoPy files\main_to_edit.py","rb+")
File = open("C:\\Users\moham\Desktop\Gimp\Knuckeles.png","rb+")
ReadFile = File.read()
ListFile = list(ReadFile)
print(ListFile)
print(ReadFile)

File_Gen = Split_File(ListFile)
print(File_Gen)
File_Symbols = Split_Generation(File_Gen[114])
print(File_Symbols)
print(len(File_Gen))
print(len(File_Symbols))
print(len(File_Symbols[18]))
"""
