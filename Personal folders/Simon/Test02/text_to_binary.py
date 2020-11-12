import binascii
import os
import sys

a_string = "fissepik"
a_string = input("Enter text to be send: ")

def returnBinary():

    a_binary_array = bytearray(a_string, "utf8")

    binary_string = []

    for binary in a_binary_array:
        binary_representation = bin(binary)[2:].zfill(8)

        binary_string.append(binary_representation)

    binary_array = []

    for i in range(len(binary_string)):
        # print(binary_string[i])
        temp_array = []
        for j in range(len(str(binary_string[i]))):
            temp_array.append(int(binary_string[i][j]))
            # print(temp_array)
        binary_array.append(temp_array) 

    return binary_array

