from operations import rowOperations
from matrixMult import multiply


def Get_I(s):
    print("identity matrix")
    I = []
    for i in range(s):
        I.append([])
    for i in range(s):
        for j in range(s):
            if i == j:
                I[i].append(1)
            else:
                I[i].append(0)
    return I

def invertMatrix(M):
    MC = len(M)
    MR = len(M[0])
    I = Get_I(MC)
    localM = M

    if MC != MR:
        return 0
        
    for C in range(MC):                         #cycle through all spaces in columns
        pivotval = M[C][C]                      #current pivot
        #print(pivotval)
        for R in range(MR):
            if R != C:
                difference = pivotval/M[C][R]   #calculate difference between currently selected space in matrix and pivot
                print(difference)               #print difference
    return I