def Check_is_1D_Matrix(M):
    # Check if the entered thing is a list
    if not isinstance(M, list):
        return False
    # Check if the list has integers or floats in its entries (Elements of the matrix)
    for i in range(len(M)):
        if not (isinstance(M[i], int) or isinstance(M[i], float)):
            return False
    return True



def Check_is_2D_Matrix(M):
    # Check if the entered thing is a list to start with
    if not isinstance(M, list):
        return False
    # Check if the list has lists inside it (Rows of matrix), and those lists have integers or floats in them (Elements of matrix).
    for i in range(len(M)):
        if isinstance(M[i], list):
            for j in range(len(M[i])):
                if not (isinstance(M[i][j], int) or isinstance(M[i][j], float)):
                    return False
        else:
            return False
    # Checks if all the rows have same length (Same amount of columns in each row)
    for i in range(len(M) - 1):                     # Checks the rows of the matrix
        try:
            if len(M[i]) != len(M[i + 1]):          # Checks if all the rows of the matrix are the same length
                return False                        # If not, then it is not a matrix
        except TypeError:
            return False                            # If the row has an element that does not support the length function, then if is not a matrix
    return True


# This initiates the Matrix checks to see if the input is a Matrix
# Instead of writing "if Check_is_1D_Matrix() and Check_is_2D_Matrix():"
def Check_is_Matrix(M):
    if Check_is_1D_Matrix(M):
        return True
    elif Check_is_2D_Matrix(M):
        return True
    else:
        return False

# This function checks if there is a 0 in the pivot we are working on
# Then searches for a row that does not have 0 in the column we are working on
# If it finds one, then it switches between the pivot row and the row that does not have a 0
# If it does not find one, then the matrix is singular, therefore it returns None to the Matrix
def Check_Pivot_Not_Zero(Mat, I, x):                # Argument(Matrix to work on, Identity matrix to work on, column and row of pivot element)
    #print("Checking pivot not zero")
    if Mat[x][x] != 0:
        return Mat
    else:
        for i in range(x + 1, len(Mat)):
            if Mat[i][x] != 0:
                LocMat = Mat[x]
                Mat[x] = Mat[i]
                Mat[i] = LocMat
                LocI = I[x]
                I[x] = I[i]
                I[i] = LocI
                return Mat
        print("Matrix is not invertible!")
        return


# This function checks if there is a 0 in the pivot we are working on
# Then searches for a row that does not have 0 in the column we are working on
# If it finds one, then it switches between the pivot row and the row that does not have a 0
# If it does not find one, then the matrix is singular, therefore it returns None to the Matrix
def Check_Pivot_Not_Even(Mat, I, x):                # Argument(Matrix to work on, Identity matrix to work on, column and row of pivot element)
    #print("Checking pivot not even")
    if Mat[x][x]%2 != 0:
        return True
    else:
        for i in range(x + 1, len(Mat)):
            if Mat[i][x]%2 != 0:
                LocMat = Mat[x]
                Mat[x] = Mat[i]
                Mat[i] = LocMat
                LocI = I[x]
                I[x] = I[i]
                I[i] = LocI
                return True
        print("Matrix is not reducible in Z256!")
        return False
