  
#liste a og b med en masse tal
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 4, 55]
b = [1, 2, 3, 4, 5, 6, 7, 8, 55, 10, 11, 12, 13, 89]
c = []

#tal a og b har til fælles, tallet kan kun gå bruges en gang 
for x in set(a) & set(b):
    print(x)

list_of_students = ["Anders", "Thomas", "Mikkel"]

name = input("Enter student name: ")

if name in list_of_students:
    print(name + " is enrolled")
else:
    print("Student is not enrolled")