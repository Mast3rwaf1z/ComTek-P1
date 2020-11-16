# Visualizations of the matrices
from b_colors import bcolors

def printMatrix(m, numberOfPackets, payloadSize, codedPacketSize):
    print(" ")
    print("* * * * * * * * * * Original Packet * * * * * * * * * *")
    print(" ")
    for i in range(numberOfPackets):
        index_value = ""

        for index_i in range(3-len(str(i + 1))):
            index_value += " "

        index_value += str(i + 1) + " "

        print(bcolors.HEADER + index_value + bcolors.ENDC, end = '')
        print("[", end = '')
        for j in range(numberOfPackets + payloadSize):
            if m[i][j] == 1:
                print(bcolors.ONES + " " + str(m[i][j]) + bcolors.ENDC, end = '')
            else: 
                print(bcolors.ZEROS + " " + str(m[i][j]) + bcolors.ENDC, end = '')

            if (j+1) == (numberOfPackets + payloadSize):
                print(" ]")
                continue
            print(",", end = '')

def printCodedMatrix(m, numberOfPackets, payloadSize, codedPacketSize):
    print(" ")
    print("* * * * * * * * * * Coded Packet * * * * * * * * * *")
    print(" ")
    for i in range(numberOfPackets + (codedPacketSize-1)):
        index_value = ""

        for index_i in range(3-len(str(i + 1))):
            index_value += " "

        index_value += str(i + 1) + " "
        
        print(bcolors.HEADER + index_value + bcolors.ENDC, end = '')
        print("[", end = '')
        for j in range(numberOfPackets + payloadSize):
            if m[i][j] == 1:
                print(bcolors.ONES + " " + str(m[i][j]) + bcolors.ENDC, end = '')
            else: 
                print(bcolors.ZEROS + " " + str(m[i][j]) + bcolors.ENDC, end = '')

            if (j+1) == (numberOfPackets + payloadSize):
                print(" ]")
                continue
            print(",", end = '')