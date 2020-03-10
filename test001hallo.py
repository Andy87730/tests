print("Hallo")
print("Welt 12:45")
print("Branch 1")
for i in range(10,29):
    print (i,end='-')
while i > 4:
    print (i,end="+")
    i = i - 1

print()

i = input("Bitte Zahl eingeben: ")

i = int(i)

if i == 3:
    print("Das war die 3")
elif i < 3:
    print("kleiner als 3")
else:
    print("größer als 3")           
    