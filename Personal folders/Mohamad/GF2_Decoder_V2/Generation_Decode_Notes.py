# Notes
#
# Function(Coded_Symbol, Gen_Num, Gen_Size):
#
# Loc_Symbol = Coded_Symbol[:]
#
# Check the position of the first 1, if there are not 1s then it is useless
#
# for i in range(Gen_Size):
#   if Packet[i] == 1:
#       Useless_Packet = 0
#       Position = i
#   else:
#       Useless_Packet = 1
# if Useless_Packet = 1
#   return -1
#
# Check if this can be used without reducing it (It can make a pivot position without reducing)
#
# if Pivot_Pos[Gen_Num][Position] == 0:
#   Pivot_Pos[Gen_Num][Position] = 1
#   Loc_Symbol.insert(0, Position)
#   Loc_Symbol.insert(0, Gen_Size)
#   Generations[Gen_Num].append(Loc_Symbol)
#   return 1
#
# Go and do the reduction using all currently available packets in the generation (You will have to remove the 2 things at the start again)
#
# a = Loc_Symbol[:]
# for i in range(len(Generations[Gen_Num]):
#   Initial_Pivot_Pos = Generations[Gen_Num][i][1]                  # Get the pivot position that this packet represents
#   if a[Initial_Pivot_Pos] == 1:
#       b = Generations[Gen_Num][i][:]
#       b.pop(0)
#       b.pop(0)
#       a = bytes([a ^ b for a, b in zip(a, b)])
#
# After it is reduced do the same check for the position of 1
#
# for i in range(Gen_Size):
#   if Packet[i] == 1:
#       Useless_Packet = 0
#       Position = i
#   else:
#       Useless_Packet = 1
# if Useless_Packet = 1
#   return -1
#
# One last check that can be deleted later
#
# if Pivot_Pos[Gen_Num][Position] == 0:
#   Pivot_Pos[Gen_Num][Position] = 1
#   Loc_Symbol.insert(0, Position)
#   Loc_Symbol.insert(0, Gen_Size)
#   Generations[Gen_Num].append(Loc_Symbol)
#   return 1
# else:
#   print("There is a bug in the system, the thing got reduced and still did not get a unique pivot position)
#
# Check if the generation was fully decoded
#
# if len(Generations[Gen_Num]) == Gen_Size:
#   Num_Pivots =  Pivot_Pos[Gen_Num][0]
#   for i in range(len(Pivot_Pos[Gen_Num]) - 1):
#         Num_Pivots = Num_Pivots + Pivot_Pos[Gen_Num][i + 1]
#   if Num_Pivots != Gen_Size:
#       print("There is a bug, the generation has enough symbols inside, but they do not form a pivot position)
#   else:
#       Run a function to finalize the generation and sort it correctly
