from Matrix_Checks import *
from Z256_Random_Matrix import *
from Get_Identity_Matrix import Get_I_Matrix
from Z256_Matrix_Extra_Functions import *
from Z256_Matrix_Operations import Z256_Const_1D_Mat_Multi
from Z256_Matrix_Multi import Matrix_Multi


# This is the function that perform row operations on a matrix and the same operations on an identity matrix
# It first reduces the matrix to echelon form, then reduces it to reduced echelon form
# Then it scales all rows into an identity row. Doing the same operations on the identity matrix
# Turns it into the inverse matrix, which is returned by the function
def Z256_Inverse_Matrix(Mat):                                               # Argument(Matrix to inverse)
    if not Check_is_2D_Matrix(Mat):                                         # Checks if the input is a 2d matrix
        print("Z256_Inverse_Matrix ERROR: Inputted list is not a 2d matrix!")
        return

    if not Check_Matrix_Elements_in_Z256(Mat):                              # Checks if the input has elements in Z256
        print("Z256_Inverse_Matrix ERROR: Matrix elements outside of Z256!")
        return

    if len(Mat) != len(Mat[0]):                                             # Checks if the inputed 2d matrix is in square form
        print("Z256_Inverse_Matrix ERROR: Inputted matrix is not square!")
        return

    LocalMat = Mat[:]                                                       # Copies the input into a local matrix (Not really needed, was implemented just in case)
    LocalI = Get_I_Matrix(len(Mat))                                         # Creates the identity matrix

    # Reducing to echelon form while doing all the operations on the identity matrix too
    for i in range(len(Mat)):                                               # This is the pivot work we are working on

        #print(LocalMat)
        #print(LocalI)

        #LocalMat = Check_Pivot_Not_Zero(LocalMat, LocalI, i)               This is not needed, as functions modify the contents of the lists
        #Check_Pivot_Not_Zero(LocalMat, LocalI, i)                          This is not needed, as we can run the function in the if statement bellow

        # Checks if the pivot element we are trying to create is a zero, while checking if the matrix is invertible at the same time
        # If the matrix is singular, or it has all even elements in pivot column, then it returns none and breaks the function
        if not (Check_Pivot_Not_Zero(LocalMat, LocalI, i) and Check_Pivot_Not_Even(LocalMat, LocalI, i)):
            return
        for j in range(i + 1, len(Mat)):                                    # This is the row we are working on
            LocalI[j] = Z256_Inverse_Matrix_Fun2(LocalMat[i], LocalMat[j], LocalI[i], LocalI[j], i)
            LocalMat[j] = Z256_Inverse_Matrix_Fun1(LocalMat[i], LocalMat[j], i)

    # Reducing to reduced echelon form while doing all the operations on the identity matrix too
    for i in range(len(Mat) - 1, 0, -1):                                    # This is the pivot work we are working on
        for j in range(i - 1, -1, -1):                                      # This is the row we are working on
            LocalI[j] = Z256_Inverse_Matrix_Fun2(LocalMat[i], LocalMat[j], LocalI[i], LocalI[j], i)
            LocalMat[j] = Z256_Inverse_Matrix_Fun1(LocalMat[i], LocalMat[j], i)
    # No need to check for zeroes or evens in this for loop, as if the first loop succeeds, then the matrix is invertible


    # Scales the matrix into an identity matrix, while doing the same scaling on the identity matrix
    for i in range(len(Mat)):
        LocalI[i] = Z256_Const_1D_Mat_Multi(LocalI[i], Z256_Multi_Inverse(LocalMat[i][i]))
        LocalMat[i] = Z256_Const_1D_Mat_Multi(LocalMat[i], Z256_Multi_Inverse(LocalMat[i][i]))

    # Sometimes the inverse matrix has some elements as -0.0 and 0.0, this checks for these elements and turns them to a normal 0
    for i in range(len(Mat)):
        for j in range(len(Mat)):
            if LocalMat[i][j] == 0:
                LocalMat[i][j] = 0
            if LocalI[i][j] == 0:
                LocalI[i][j] = 0
    return LocalI

"""
Mat123 = [[35, 48, 126, 134], [21, 45, 68, 57], [34, 138, 243, 13], [28, 138, 210, 35]]     #This gives a shit ton of error, needs to invistigated
Odd_Mat = [[135, 49, 213], [134, 255, 187], [10, 58, 99]]
InvMat123=Z256_Inverse_Matrix(Mat123)
print(Mat123)
print(InvMat123)
print(Matrix_Multi(Mat123, InvMat123))
print(Z256_Inverse_Matrix(Mat123))
print(Z256_Inverse_Matrix(Odd_Mat))
"""
#M123 = Z256_Random_Matrix(3, 3)
#print(M123)
#print(Z256_Inverse_Matrix(M123))

"""
RandMat = Z256_Random_Reducible_Matrix(5)
RandMatInv = Z256_Inverse_Matrix(RandMat)
print(RandMat)
print(RandMatInv)
print(Matrix_Multi(RandMat, RandMatInv))
print(Matrix_Multi(RandMatInv, RandMat))
"""
