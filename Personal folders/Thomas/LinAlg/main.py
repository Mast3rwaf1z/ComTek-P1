from operations import rowOperations
from matrixinverse import *
from matrixMult import *
from XOR import *

# first two entries symbolize the index vector, when the rows get XOR'ed,
# XOR the input with one row to get the other
A = [1, 0, 1, 0, 1, 0]
B = [0, 1, 0, 0, 1, 1]

I = [
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 1]
    ]

M = [
    [5,6,6],
    [6,5,6],
    [6,6,5]
]

mm = matrixmultiplication(A, B)
print("matrix multiplication:")
for i in range(len(mm)):
    print(mm[i])
AB = XOR(A, B)
print("XOR")
print(AB)
B = XOR(AB, A)
print(B)

inv = Get_I(3)
for i in range(len(inv)):
    print(inv[i])

I[1] = rowOperations(I[1], I[0], "addition")
print("addition:")
for i in range(len(I)):
    print(I[i])

I[1] = rowOperations(I[1], I[0], "subtraction")
print("subtraction:")
for i in range(len(I)):
    print(I[i])

I[1] = rowOperations(I[1], 2, "multiplication")
print("multiplication:")
for i in range(len(I)):
    print(I[i])

I[0] = rowOperations(I[0], I[1], "replace")
print("replace:")
for i in range(len(I)):
    print(I[i])

invertMatrix(M)