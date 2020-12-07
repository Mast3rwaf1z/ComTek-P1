packets = [
    b'0101',
    b'1010',
    b'1100',
    b'1001',
    b'0011'
]
decode1 = []
for i in range(len(packets)):
    decode1.append(packets[i].decode())
print(decode1)

decode2 = []
for i in range(len(decode1)):
    decode2.append(list(decode1[i]))
print(decode2)

decode3 = []
for i in range(len(decode2)):
    decode3.append([])
    for j in range(len(decode2[0])):
        if decode2[i][j] == '0':
            decode3[i].append(0)
        elif decode2[i][j] == '1':
            decode3[i].append(1)
print(decode3)
