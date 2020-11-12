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


def Check_Matrix_Elements_in_Z256(M):
    #print("Checking element in Z256")
    # If the matrix is 1D, then check each element in the row
    if Check_is_1D_Matrix(M):
        for i in range(len(M)):
            if not 0<=M[i]<256:
                return False

        return True

    # If the matrix is 2D, it goes around each row and column and checks each element
    elif Check_is_2D_Matrix(M):
        for i in range(len(M)):
            for j in range(len(M[i])):
                if not 0<=M[i][j]<256:
                    return False
        return True

    # If it is neither a 1D or 2D matrix then it returns a false and prints Not Matrix
    else:
        print("Not Matrix")
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
"""
# Old function used to check for a 2d matrix. Above function is 1 line shorter :P
# Checks if an input is a 2d matrix
def Check_is_2D_Matrix(M):                          # Argument(Matrix to check)

    # Returns False if the element is not a matrix with dimension 2 or more
    try:
        if len(M) < 2:                              # Checks if the elements length is shorter than 2
            return False                            # If yes then it is not a 2d matrix
    except TypeError:
        return False                                # If the length function does not work on the input then it is not a matrix at all

    # Returns false if the matrix of dimension 2 or more does not have rows of the same length
    # (Only checks the first 2d matrix if the matrix has a dimension of more than 2)
    for i in range(len(M) - 1):                     # Checks the rows of the matrix
        try:
            if len(M[i]) != len(M[i + 1]):          # Checks if all the rows of the matrix are the same length
                return False                        # If not, then it is not a matrix
        except TypeError:
            return False                            # If the row has an element that does not support the length function, then if is not a matrix

    # Returns False if the matrix has a dimension more than 2
    try:
        if len(M[0][0]) > -1:                       # Check if the matrix has 3rd dimension
            return False                            # If the matrix has a 3rd dimension return False
    except TypeError:                               # If the matrix does not have a 3rd dimension, then we are taking the length of an integer
        return True                                 # Taking the length of an integer produces a TypeError, so if the error occurs return True

"""
