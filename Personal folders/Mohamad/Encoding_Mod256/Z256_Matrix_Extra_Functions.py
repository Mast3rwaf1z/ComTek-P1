from Operations import Z256_Add_Inverse, Z256_Multi_Inverse
from Z256_Matrix_Operations import *

# This function is used to replace the previous row, with a row that has a 0 at the pivot column
def Z256_Inverse_Matrix_Fun1(Mat1, Mat2, x):                         # Arguments(Pivot row of matrix, Row of matrix to do row operation on, Column being worked on)
    LocMat1 = Z256_Const_1D_Mat_Multi(Mat1, Z256_Multi(Z256_Multi_Inverse(Mat1[x]), Z256_Add_Inverse(Mat2[x])))
    Mat3 = Z256_Matrix_1D_Add(Mat2, LocMat1)
    return Mat3


# This function is used to apply the operations done in the above function on the identity matrix
def Z256_Inverse_Matrix_Fun2(Mat1, Mat2, IdMat1, IdMat2, x):         # Arguments(Pivot row of matrix, Row of matrix to do row operation on,Pivot row of identity matrix, Row of identity matrix to do row operation on, Column being worked on)
    LocIdMat1 = Z256_Const_1D_Mat_Multi(IdMat1, Z256_Multi(Z256_Multi_Inverse(Mat1[x]), Z256_Add_Inverse(Mat2[x])))
    Mat3 = Z256_Matrix_1D_Add(IdMat2, LocIdMat1)
    return Mat3


# These two functions are only supposed to be used in the Inverse Matrix function
# As they are the building blocks for the algorithm
# They are not really built to be used anywhere else
