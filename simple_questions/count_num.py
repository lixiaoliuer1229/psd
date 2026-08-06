result = []
s = "3#5,2#9"

ps = s.split(",")
for p in ps:
    if "#" in p:
        m = p.split("#")
        for i in range(0,int(m[0])):
            result.append(m[1])
    else:
        result.append(p)

print(result)