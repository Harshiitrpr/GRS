import networkx as nx
import matplotlib.pyplot as plt

def copy_repos(allrepos, copy_repos):
    for i in copy_repos:
        allrepos.add(i)

def Graph_synthesis(G, conn):
    n = len(conn)
    for i in range(n):
        for j in range(i + 1, n):
            if(G.has_edge(conn[i], conn[j]) == False):
                G.add_edge(conn[i], conn[j])

G = nx.Graph()
f = open("/home/captain/Social Networks/Soical Project/Data Collection/data.txt")
lines = f.read().splitlines()
lines.sort()
nodes = {}
repos = {}
nodes_list = []
repos_list = []
allrepos = set()
length = 0
for i in range(1, len(lines)):
    if(lines[i] != ''):
        row = lines[i].split()
        if(length == 0):
            nodes_list.append(row[0])
            repos_list.append(row[1:])
            copy_repos(allrepos, repos_list[length])
            length += 1
        elif (nodes_list[length - 1] != row[0]):
            nodes_list.append(row[0])
            repos_list.append(row[1:])
            copy_repos(allrepos, repos_list[length])
            length += 1

G.add_nodes_from(range(len(nodes_list)))
allrepos = list(allrepos)
for i in allrepos:
    conn_nodes = []
    for j in range(len(repos_list)):
        if(i in repos_list[j]):
            conn_nodes.append(j)
    
    Graph_synthesis(G, conn_nodes)
    
print(len(G.edges()))
nx.draw(G)
plt.show()
