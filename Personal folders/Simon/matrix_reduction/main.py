# Generate 20 random arrays of 8 values + 20 values for the EV - these represent our update

# Encoding:
#   Now we generate coded packets existing of 5 individual packets (arrays)
#   This will be done by XOR'ing the arrays with their EV's together

# Transmission:
#   Each time a coded packet gets generated it gets send to another function

# Decoding:
#   When packets arrive
#   WE DECODE

from text_to_binary import returnBinary
from visualizations import printMatrix, printCodedMatrix
from b_colors import bcolors

from random import randint
import sys
import time
import copy

numberOfPackets = 8
payloadSize = 8
codedPacketSize = 5

originalArray = []
encodedArray = []
decodedArray = []

binary_array = returnBinary()
numberOfPackets = len(binary_array)
payloadSize = len(binary_array[0])

# Representation of the data we want to send
def generateArray(binArr):
    # Firstly generate the encoding vector:
    for i in range(numberOfPackets):
        coded_packet = []
        for j in range(numberOfPackets):
            if (i == j):
                coded_packet.append(1)
            else:
                coded_packet.append(0)
        # Now we input the payload to the 
        for k in range(payloadSize):
            coded_packet.append(binary_array[i][k])
            # coded_packet.append(randint(0,1))             #Randomized
        originalArray.append(coded_packet)

# Encoding 
def encodePackets(orgArr):      # original array
    lowerRange = None
    higherRange = None
    for i in range(numberOfPackets + (codedPacketSize-1)):          #number of coding packets

        if(i < numberOfPackets):
            higherRange = i+1
        else:
            higherRange = numberOfPackets

        if(i >= codedPacketSize):
            lowerRange = i-codedPacketSize+1
        else:
            lowerRange = 0

        copyOriginal = copy.deepcopy(orgArr)
        tempArray = copyOriginal[lowerRange]
        
        for j in range(lowerRange, higherRange):                    #every single coding packet
            for k in range(payloadSize + numberOfPackets):
                if j == lowerRange:
                    continue
                else:
                    tempArray[k] = tempArray[k] ^ copyOriginal[j][k]
        encodedArray.append(tempArray)

# Takes in the encoded packet -> Sends it forward to the decoder
def transmission(m):
    decodePackets(m)

# Takes in the encoded packet and decodes it
def decodePackets(m):
    coordinateToReduce(m)

def coordinateToReduce(m):
    row_bound = 0
    for j in range(numberOfPackets):
        row_bound += 1
        for i in range(row_bound, numberOfPackets):         # MAYBE THIS INSTEAD : numberOfPackets + (codedPacketSize-1)
            if m[i][j] != 0:
                print('\nCoordinate to be reduced: [' + str(i) + "," + str(j) + "]")
                rowToReduceWith(m, i, j)

def rowToReduceWith(m, i, j):
    row_to_reduce_w = None
    for ii in range(numberOfPackets):
        if ii == i:
            continue
        elif m[ii][j] != 0:
            row_to_reduce_w = ii
            break
    reduceMatrix(m, i, j, row_to_reduce_w)

def reduceMatrix(m, i, j, ii):
    for jj in range(j, numberOfPackets + payloadSize):
        m[i][jj] = m[i][jj] ^ m[ii][jj]
    
    printCodedMatrix(m, numberOfPackets, payloadSize, codedPacketSize)
    if i == (numberOfPackets - 1) and j == (numberOfPackets - 2):
        extractPayload(m, i, j)

def extractPayload(m, i, j):
    for x in range(numberOfPackets):
            temp_array = []
            for y in range(numberOfPackets + payloadSize):
                temp_array.append(m[x][y])
            # decodedArray[x] = m[x]
            decodedArray.append(temp_array)

def binaryInterpretation(m, numberOfPackets, payloadSize):
    ascii_string = ""
    for i in range(0, numberOfPackets):
        temp_string = ""
        for j in range(numberOfPackets, (numberOfPackets+payloadSize)):
            temp_string += str(m[i][j])
            
        an_integer = int(temp_string, 2)
        ascii_character = chr(an_integer)
        ascii_string += ascii_character

    print(" ")
    print(bcolors.SUCCESS + ascii_string + bcolors.ENDC)
    print(" ")



generateArray(binary_array)
printMatrix(originalArray, numberOfPackets, payloadSize, codedPacketSize)
encodePackets(originalArray)
printCodedMatrix(encodedArray, numberOfPackets, payloadSize, codedPacketSize)
transmission(encodedArray)
binaryInterpretation(decodedArray, numberOfPackets, payloadSize)