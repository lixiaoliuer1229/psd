pp =  [4, 5, 6, 5, 4, 7, 8]

result = []

for i in range(0,len(pp)):
    t_max = max(pp)
    t_min = min(pp)
    if t_max - t_min > 2:
        pp.remove(t_max)

print(pp)