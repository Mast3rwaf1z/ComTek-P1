# This function produces an x by x identity matrix
def Get_I_Matrix(x):            # Argument(Size of identity matrix)
    if not isinstance(x, int):
        print("Get_I_Matrix ERROR: Argument entered is not an integer")
    I=[]
    for i in range(x):
        I.append([])
    for i in range(x):
        for j in range(x):
            if j==i:
                I[i].append(1)      # If working with diagonals add 1
            else:
                I[i].append(0)      # Else add 0 everywhere else
    return I
