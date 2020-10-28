def XOR(p1, p2):
    A = [p1, p2]
    result = []
    for i in range(len(p1)):
        if A[0][i] == A[1][i]:
            result.append(0)
        elif A[0][i] != A[1][i]:
            result.append(1)
    return result
