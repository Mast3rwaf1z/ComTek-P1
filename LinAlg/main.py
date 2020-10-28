from matrixinverse import *
from matrixMult import *
from XOR import *

# first two entries symbolize the index vector, when the rows get XOR'ed,
# XOR the input with one row to get the other
A = [1, 0, 1, 0, 1, 0]
B = [0, 1, 0, 0, 1, 1]

mm = matrixmultiply(A, B)
print("matrix multiplication:")
for i in range(len(mm)):
    print(mm[i])

xor = XOR(A, B)
print("XOR")
print(xor)
