from matrixMult import multiply


def rowOperations(r1, r2, operation):
    result = []
    if operation == "multiplication":
        result = multiply(r1, r2)
    elif len(r1) != len(r2):
        return 0
    elif operation == "addition":
        for i in range(len(r1)):
            result.append(r1[i] + r2[i])
    elif operation == "subtraction":
        for i in range(len(r1)):
            result.append(r1[i] - r2[i])
    elif operation == "replace":
        result = r2
    return result