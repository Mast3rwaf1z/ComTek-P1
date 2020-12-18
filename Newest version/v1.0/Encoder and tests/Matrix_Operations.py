from Matrix_Checks import Check_is_1D_Matrix

# Adds two vector matrices
def Matrix_1D_Add(Mat1, Mat2):
    # Check that the arguments are 1D matrices and that they have the same length
    if not Check_is_1D_Matrix(Mat1):
        print("Matrix_1D_Add ERROR: 1st argument is not a 1D matrix")
        return
    if not Check_is_1D_Matrix(Mat2):
        print("Matrix_1D_Add ERROR: 2nd argument is not a 1D matrix")
        return
    if len(Mat1)!=len(Mat2):
        print("Matrix_1D_Add ERROR: Matrices are not same size!")
        return
    # Add the two vectors together and append them in ResMat then return ResMat
    ResMat=[]
    for i in range(len(Mat1)):
        ResMat.append(Mat1[i] + Mat2[i])
    return ResMat


# Multiplies all vector elements with a constant
def Const_1D_Mat_Multi(Mat, c):            # Argumants(Matrix, Constant)
    # Checks that the first argument is a vector and that the second argument is a number
    if not Check_is_1D_Matrix(Mat):
        print("Const_1D_Mat_Multi ERROR: 1st argument is not a 1D matrix")
        return
    if not isinstance(c, (int, float)):
        print("Const_1D_Mat_Multi ERROR: 2nd argument is not an integer or a float")
    # Multiply all elements in the vector with the constant and append it to ResMat, then return ResMat
    ResMat = []
    for i in range(len(Mat)):
        ResMat.append(c * Mat[i])
    return ResMat
