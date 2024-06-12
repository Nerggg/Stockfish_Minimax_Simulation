res = []
temp = str()

while temp != "zzz":
    temp = input()
    res.append(temp)
    print(temp)
    print("anjay")

for i in range (len(res)):
    print(f"{i+1}. {res[i]} ", end="")