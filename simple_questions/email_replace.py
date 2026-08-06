ss = [
    "john.doe+ads@gmail.com",
    "john+newsletter@gmail.com",
    "bob@yahoo.com",
    "alice+bob@outlook.com",
    "al.ice@outlook.com"
]

item = {}

for s in ss:
    if '@' in s:
        t = s.split("@")
        item[t[1]] = []

for s in ss:
    if "@" in s:
        t = s.split("@")
        if t[1] in item and "+" not in s:
            item[t[1]].append(s)
        else:
            p = t[0].split("+")
            l = p[0] + "@" + t[1]
            item[t[1]].append(l)
print(item)