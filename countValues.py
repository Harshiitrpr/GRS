f = open("values.txt",'r')
vals = f.read().split()

for i in range(20):
    print(i,"=",vals.count(str(i)))