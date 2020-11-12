from Operations import *

# Adds two vector matrices with the addition operation in Z256
def Z256_Matrix_1D_Add(Mat1, Mat2):
    if len(Mat1)!=len(Mat2):
        print("Z256_Matrix_1D_Add ERROR: Matrices are not same size!")
        return
    ResMat=[]
    for i in range(len(Mat1)):
        ResMat.append(Z256_Add(Mat1[i], Mat2[i]))

    return ResMat


# Multiplies all vector elements with a constant over the ring Z256
def Z256_Const_1D_Mat_Multi(Mat, c):            # Argumants(Matrix, Constant)
    ResMat = []
    for i in range(len(Mat)):
        ResMat.append(Z256_Multi(c, Mat[i]))
    return ResMat


