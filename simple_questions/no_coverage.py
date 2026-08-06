pp = [(1, 5), (3, 6), (7, 9)]

for i in range(0,len(pp)):
    if i < len(pp)-1:
        if max(pp[i]) > min(pp[i+1]):
            tt = max(pp[i]) - min(pp[i+1])
            print(tt)
        else:
            print(pp[i+1])