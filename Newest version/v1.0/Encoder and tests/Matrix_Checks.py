# Checks if a matrix is a list of numbers and nothing else
def Check_is_1D_Matrix(M):
    # Check if the entered thing is a list
    if not isinstance(M, list):
        return False
    # Check if the list has integers or floats in its entries (Elements of the matrix)
    for i in range(len(M)):
        if not (isinstance(M[i], int) or isinstance(M[i], float)):
            return False
    return True


# Checks if a matrix is a proper 2D matrix
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

