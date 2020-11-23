#import modules
from time import sleep as s

#sætter tids variabler
s_delay = 1
l_delay = 3

#intro
print("Hej, nu skal vi finde ud af hvad du må ud fra din alder")
s(l_delay)
age = input("Så hvor gammel er du?: ")

#converter string input til integere
age = int(age)

#resultatet ud fra din alder
if age >= 25:
    print("Du må alt ude i den større verden, giv den gas!!")
elif age < 25 and age > 21:
    print("Forsikringselskaber i udlandet vil ikke forsikre dig endnu")
    s(l_delay)
    print("MEN")
    s(s_delay)
    print("Du kan købe alkohol overalt i verden")
elif age < 21 and age > 18:
    print("Du må nu stemme, men du kan ikke købe alkohol over alt i verden")
    s(l_delay)
    print("Stay strong!")
elif age == 18:
    print("Tillykke du må stemme og købe alt alkohol i DK")
    print("Og gammel nok til at komme i fængsel nu")