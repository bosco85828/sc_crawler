with open("domain.txt") as f : 
    dlist=[ tuple(x.strip().split(',')) for x in f.readlines()]

print(dlist)

