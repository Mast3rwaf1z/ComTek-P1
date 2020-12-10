from Constants import Pivot_Pos, Generations

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
