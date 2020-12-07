

#liste over tal
a = [1,1,2,"Anders",5,8,"Vaffel",34,55,89]

a.append(100)

for x in a:
    print(x)

#Indtast et tal imellem 0-100
grade = input("Enter your grade: ")
grade = int(grade)
if grade >= 90:
    print("A")
elif grade >=80:
    print("B")
elif grade >=70:
    print("C")
elif grade >=65:
    print("D")
else:
    print("F")
