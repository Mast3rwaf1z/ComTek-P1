def multiply(c, constant):
    result = []
    for i in range(len(c)):
        result.append(constant * c[i])
    return result

# r1 must be a column while r2 must be a row, bigger matrices not yet supported
# and for the purpose of this project it is not needed yet


def matrixmultiplication(A, B):
    result = []
    for i in range(len(A)):
        result.append(multiply(B, A[i]))
    return result
