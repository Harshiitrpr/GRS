import networkx as nx
import matplotlib.pyplot as plt

with open("values.txt") as values:
    values = values.read().splitlines()
    values = values[0].split()

numUsers = 1965


print(len(values))
print(1965*1964 + 1964)
x = []
y = []

for k in range(1,8):
    G = nx.Graph()
    for i in range(1965):
        for j in range(1965):
            if(i != j and i*1965 + j < len(values) and float(values[i*1965 + j]) > k):
                G.add_edge(i,j)

    cnt = 0
    ind = 0
    for i in G.nodes():
        ind += G.degree(i)
        cnt+=1
    y.append(ind/cnt)
    x.append(k)

plt.plot(x,y)
plt.show()