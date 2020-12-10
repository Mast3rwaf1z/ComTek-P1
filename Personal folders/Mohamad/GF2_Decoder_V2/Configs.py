from Constants import Full_File_Data, Generations, Generations_Decoded, Pivot_Pos, Pivot_Pos_Ran, Packets_Needed_To_Decode_Generation

# This function need to be adjusted beforehand, no it only works for generation size 32, symbol size 40
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
