#Create a program that asks the user to enter their name and their age. 
#Print out a message addressed to them that tells them the year that they will turn 100 years old.

import time

s_delay = 1
l_delay = 2

name = input("Hvad er dit navn: ")
time.sleep(l_delay)
x = input("Indtast dit fødselsår: ")
time.sleep(s_delay)
age = 2020 - int(x)
age2 = age + 100

time.sleep(s_delay)
print("Hej " + name + ", du er " + str(age) + " år gammel.")
time.sleep(l_delay)
print("Om 100 år er du " + str(age2))