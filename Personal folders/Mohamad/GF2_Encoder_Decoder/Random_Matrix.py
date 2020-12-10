from random import randint, choices

# Make a random matrix with 0 and 1 with a selected density
def Random_2D_Bit_Matrix(n, Density):                      # Args(Size of square matrix, Densiter (Ratio of 1s))
    if not isinstance(n, int):                          # Check 1st arg is integer
        print("Random_Bit_Matrix ERROR:  1st argument entered is not an integer")
        return
    if not isinstance(Density, (int, float)):           # Check 2nd arg is float or integer
        print("Random_Bit_Matrix ERROR: 2nd argument entered is not an integer or a float")
        return
    if Density > 1 or Density < 0:                      # Check 2nd arg is between 0 and 1
        print("Random_Bit_Matrix ERROR: Density given is over not between 0 and 1")
    DensList = [1-Density, Density]                     # Fill probability list
    Mat = choices([0, 1], weights=DensList, k=n*n)      # Fill a list with 0s and 1s
    ResMat = []
    # Make the list into a 2d matrix
    for i in range(n):
            ResMat.append([])
            for j in range(n):
                ResMat[i].append(Mat[i * n + j])
    return ResMat

# Make a random matrix with 0 and 1 with a selected density
def Random_1D_Bit_Matrix(n, Density):                   # Args(Size of list, Densiter (Ratio of 1s))
    if not isinstance(n, int):                          # Check 1st arg is integer
        print("Random_Bit_Matrix ERROR:  1st argument entered is not an integer")
        return
    if not isinstance(Density, (int, float)):           # Check 2nd arg is float or integer
        print("Random_Bit_Matrix ERROR: 2nd argument entered is not an integer or a float")
        return
    if Density > 1 or Density < 0:                      # Check 2nd arg is between 0 and 1
        print("Random_Bit_Matrix ERROR: Density given is over not between 0 and 1")
    DensList = [1-Density, Density]                     # Fill probability list
    ResMat = choices([0, 1], weights=DensList, k=n)       # Fill a list with 0s and 1s
    ResMat_Sum = 0
    for i in range(len(ResMat)):
        ResMat_Sum += ResMat[i]
    if ResMat_Sum > 0:
        return ResMat
    else:
        return -1
