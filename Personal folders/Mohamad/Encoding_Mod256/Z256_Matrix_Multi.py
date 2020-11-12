from Matrix_Checks import Check_is_Matrix
from Operations import Z256_Add, Z256_Multi


# Multiplies two matrices with the operations in the ring Z256
def Matrix_Multi(M1, M2):                                       # Arguments(Left Matrix, Right Matrix) Order matters
    Not_Matrix=0
    if not Check_is_Matrix(M1):
        print("Matrix_Multi ERROR: First argument is not a 2d matrix")
        Not_Matrix=1
    if not Check_is_Matrix(M2):
        print("Matrix_Multi ERROR: Second argument is not a 2d matrix")
        return
    if Not_Matrix==1:
        return
    if len(M1[0])!=len(M2):
        print("Matrix_Multi ERROR: Matrix multiplication is not defined between " + str(len(M1)) + "x" + str(len(M1[0])) + " matrix and " + str(len(M2)) + "x" + str(len(M2[0])) + "matrix." )
        return
    M3=[]
    y = 0
    for i in range(len(M1)):
        M3.append([])
        for j in range(len(M2[0])):
            x = 0
            for k in range(len(M2)):
                y = Z256_Multi(M1[i][k], M2[k][j])
                x = Z256_Add(x, y)
            M3[i].append(x)
    return M3

# Too tired of commenting. Will comment this one day (Hopefully)
