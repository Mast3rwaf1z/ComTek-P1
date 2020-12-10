# Notes
#
# def Generation_Sort_Reduce(Gen_Num, Gen_Size, Symbol_Size):
#   Loc_Gen = Generations[Gen_Num][:]
#   Sorted_Gen = []
#   for i in range(Gen_Size):
#       Sorted_Gen.append([])
#
#   Sort the generation
#
#   for i in range(Gen_Size):
#       Sorting_Pos = Loc_Gen[i][0]
#       for j in range(len(Loc_Gen[i]):
#           Sorted_Gen[Sorting_Pos].append(Loc_Gen[i][j])
#
#   Check that it has sorted correctly, if yes pop out the pivot position indicator
#
#   for i in range(Gen_Size):
#       if Sorted_Gen[i][0] == i:
#           Sorted_Gen[i].pop(0)
#       else:
#           print("There is a bug, the sorting algorithm has failed to sort the generation)
#           return -1
#
#   Reduce to reduced echelon form
#
#   for i in range(len(Sorted_Gen) - 1, 0, -1):                                 # The bottom symbol
#       a = Sorted_Gen[i][:]
#       for j in range(i):                                                      # The upper symbols
#           if Sorted_Gen[j][i] == 1:
#               b = Sorted_Gen[j][:]
#               Sorted_Gen[j] = bytes([a ^ b for a, b in zip(a, b)])
#
#   Append all the symbol data into the Full_File_Data list
#
#   for i in range(Gen_Size):
#       for j in range(Symbol_Size):
#           Full_File_Data[Gen_Num].append(Sorted_Gen[i][Gen_Size + j])
#   Generations_Decoded[Gen_Num] = 1
#   return 1
