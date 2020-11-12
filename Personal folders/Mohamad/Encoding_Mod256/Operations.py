# This function is used as a checker for all the functions in this file
# It checks that the entries are integers and that they are in Z256
def Z256_Operations_Checks(a, b):                                   # Arguments(1st element to check, 2nd element to check)
    #print("a is: " + str(a))
    #print("b is: " + str(b))
    Not_Int = False
    Not_Z256 = False
    if not isinstance(a, int):                                      # Checks if first entry is an integer
        print("Z256_Operations_Checks ERROR: First argument is not an integer")
        Not_Int = True                                              # If not assigns True to Not_Integer
    if not isinstance(b, int):                                      # Checks if second entry is an integer
        print("Z256_Operations_Checks ERROR: Second argument is not an integer")
        Not_Int = True                                              # If not assigns True to Not_Integer
    if Not_Int:
        return True                                                 # Returns True if integer check failed
    if not 0<=a<256:                                                # Checks if first entry is in Z256
        print("Z256_Operations_Checks ERROR: First argument not in Z256")
        Not_Z256 = True                                             # If not assigns True to Not_Z256
    if b < 0 or b > 255:                                            # Checks if second entry is in Z256
        print("Z256_Operations_Checks ERROR: Second argument not in Z256")
        Not_Z256 = True                                             # If not assigns True to Not_Z256
    if Not_Z256:
        return True                                                 # Returns True if Z256 check failed
    return False                                                    # Returns True if both elements are integers in Z256


# Does binary addition in the rung Z256 (Might be useless but I already did it)
def Z256_Add(a, b):                                                 # Arguments(1st element to add, 2nd element to add) Order does not matter
    if Z256_Operations_Checks(a, b):
        return
    return (a + b) % 256


# Does binary multiplication in the ring Z256 (Might be useless but I already di it)
def Z256_Multi(a, b):                                               # Arguments(1st element to multiply, 2nd element to multiply) Order does not matter
    if Z256_Operations_Checks(a, b):
        return
    return (a * b) % 256


# Gets the inverse of an elements over addition in Z256
def Z256_Add_Inverse(a):                                             # Argument(Element to find additive inverse for)
    if Z256_Operations_Checks(a, 0):
        return
    #print("Add Inverse is: " + str(256-a))
    return (256 - a)%256


# Gets the inverse of an element over multiplication in Z256
def Z256_Multi_Inverse(a):                                          # Argument (Element to find multiplicative inverse for)
    if Z256_Operations_Checks(a, 0):
        return
    d = 0
    # The Multiplication inverse of an element in Z256 is an element in Z256 that satisfies the equality bellow
    # The equality bellow has many solution between 0 and 256. However, only one of them is an integer
    # This while loop checks to find that integer solution and return it
    while True:
        Inva = (1 / a) + (256 / a) * d
        #print(Inva)
        if Inva < 256:
            if -0.00001<=Inva - int(Inva+0.0000001)<=0.00001:   #This was done due to some numbers having problems with floating point errors (7 for example)
                #print("Error: " + str(Inva - int(Inva+0.00001)))
                #print("Multi_Inverse is: " + str(int(Inva+0.0000001)))
                return (int(Inva+0.0000001))
            else:
                #print("Error: " + str(Inva - int(Inva+0.00001)))
                d += 1
        else:
            print("Z256_Multi_Inverse ERROR: Value entered does not have an inverse, as it is not an odd number")
            return
"""
print(Z256_Multi(255, 255))
print(Z256_Add_Inverse(22))
print(Z256_Multi_Inverse(53))
print(Z256_Multi(53, 29))
print(Z256_Multi_Inverse(22))
"""

#print(Z256_Multi_Inverse(221))
#print(int(221.0))

# This function was made to make sure the Multi_Inverse function was working properly
# As it had trouble with floating point errors
# Goes around trying to find the inverse for all odd numbers in Z256
def Check_Non_Inversed_Odds():
    NotInv=0
    NotInvMat = []
    for i in range(127):
        Inv = Z256_Multi_Inverse(2*i+1)
        print("Inverse of " + str(2*i+1) + " is: " + str(Inv))
        if Inv == None:
            NotInv+=1
            NotInvMat.append(2*i+1)

    print(NotInv)
    print(NotInvMat)


#Z256_Multi_Inverse(7)
#Check_Non_Inversed_Odds()
#print(int(182.99999999999997))
