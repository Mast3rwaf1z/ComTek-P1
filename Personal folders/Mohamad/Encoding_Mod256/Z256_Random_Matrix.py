from random import randint


#Produces a random matrix with random elements in Z256
def Z256_Random_Matrix(n, m):                   # Arguments(Number of rows, Number of columns)
    if not isinstance(n, int):
        print("Z256_Random_Matrix ERROR: First argument entered is not an integer")
        return
    if not isinstance(n, int):
        print("Z256_Random_Matrix ERROR: Second argument entered is not an integer")
        return
    Mat=[]
    for i in range(n):
        Mat.append([])                          # Adds a row to the matrix
        for j in range(m):
            Mat[i].append(randint(0,255))       # Adds an integer between 0 and 255 in the row (Adds an element)

    return(Mat)

# Produces a random matrix that is always reducible if invertible
# The criteria for such a matrix is that the diagonal elements all have to be odd
# The elements in the lower triangle all have to be even
# While the elements in the upper triangle can be any element in Z256
# Produced matrix is square
def Z256_Random_Reducible_Matrix(n):                # Argument(Number of rows and columns of square matrix)
    if not isinstance(n, int):
        print("Z256_Random_Reducible_Matrix ERROR: Argument entered is not an integer")
    Mat = []
    for i in range(n):
        Mat.append([])                              # Adds a row to the matrix
        for j in range(n):
            if j < i:
                Mat[i].append(2*randint(0,127))     # If it is working with lower triangle adds a random even number
            elif j == i:
                Mat[i].append(2*randint(0,127)+1)   # If it is working with diagonal adds a random odd number
            elif j > i:
                Mat[i].append(randint(0,255))       # If it is working with upper triangle adds a random number
            else:
                print("Dahek u just gave me?")      # I have no idea what might trigger this. Probably will never be triggered
    return Mat

#print(Z256_Random_Matrix(6, 6))
#print(Z256_Random_Reducible_Matrix(4))
