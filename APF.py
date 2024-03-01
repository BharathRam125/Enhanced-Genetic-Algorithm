#APF PESUDO RANDOM FOR COMPLEX MAPS

import re #To unpack potential_matrix
import networkx as nx
from pyvis.network import Network
import random
import PotentialAssignmentForNodes
from GeneticAlgorithm import g_algo

def graph_gen(potential_matrix, start):
    print("Running APF..")
    graph = nx.DiGraph()
    
    dest = [0,0]
    for i in range(len(potential_matrix)):
        for j in range(len(potential_matrix[i])):
            if potential_matrix[i][j] > potential_matrix[dest[0]][dest[1]]:
                dest = [i,j]
    
    def N_loop(graph, TRAV, ct):     
        N = []  #List of neighbour of Q
        Q = [TRAV[ct]]
        
        x = Q[0][0]  #x co-ord of node
        y = Q[0][1]  #y co-ord of node
        
    #For edge nodes of matrix neighbour node calc.
        if ((x == 0) | (x == len(potential_matrix)-1) | (y == 0) | (y == len(potential_matrix)-1)):
            #Adjacent neighbours
            if x != 0:
                N.append([x-1,y])  
            if y != 0:
                N.append([x,y-1])
            if x != len(potential_matrix)-1:
                N.append([x+1,y])
            if y != len(potential_matrix)-1:
                N.append([x,y+1])
                
            #Diagonal neighbours
            if  (x != 0 and y != 0):
                N.append([x-1,y-1])
            if  (x != 0 and y != len(potential_matrix)-1):
                N.append([x-1,y+1])
            if  (x != len(potential_matrix)-1 and y != 0):
                N.append([x+1,y-1])
            if  (x != len(potential_matrix)-1 and y != len(potential_matrix)-1):
                N.append([x+1,y+1])
                
        #For inner nodes of matrix neighbour node calc.
        else:
           #Adjacent neighbours
           N.append([x-1,y])
           N.append([x,y-1])
           N.append([x+1,y])
           N.append([x,y+1])
           
           #Diagonal neighbours
           N.append([x-1,y-1])
           N.append([x-1,y+1])
           N.append([x+1,y-1])
           N.append([x+1,y+1])
        
        for i in N:
            if potential_matrix[i[0]][i[1]] > potential_matrix[x][y]:
                TRAV.append(i)
                root = str(x) + " " + str(y)
                leaf = str(i[0]) + " " + str(i[1])
                #print(root + " " + leaf)
                graph.add_edge(root, leaf)
        
        TRAV1 = []
        for t in TRAV:
            if t not in TRAV1:
                TRAV1.append(t)
        
        N.clear()
        Q.clear()
        return [graph, TRAV1]
    
    TRAV = [start]
    ct = 0
    while len(TRAV) > ct:
        LST = N_loop(graph, TRAV, ct)
        ct += 1
        graph = LST[0]
        TRAV = LST[1]
    return graph

#Main Function
potential_matrix = []
with open('potential_matrix.txt') as f:
    rows = f.readlines()
    for row in rows:
        potential_matrix.append([int(i) for i in re.findall(r'-?\d+\b',row)])

#Start node input    
s = input("Enter start as i,j (eg. 46,6): ")
start = s.split(",")
start[0] = int(start[0])
start[1] = int(start[1])

#Call function to generate graph
graph = nx.DiGraph()
graph = graph_gen(potential_matrix, start)


dest = [0,0]
for i in range(len(potential_matrix)):
    for j in range(len(potential_matrix[i])):
        if potential_matrix[i][j] > potential_matrix[dest[0]][dest[1]]:
            dest = [i,j]
    
    
pts = []
Paths = []
mylist = [1, 0]
path = nx.all_simple_paths(graph, source=str(str(start[0]) + " " + str(start[1])), target=str(str(dest[0]) + " " + str(dest[1])))

# Count the total number of paths
num_paths= 0

for i in path:
    # Increment the number of paths
    num_paths += 1
    if num_paths > 99999:
        break

selected_paths =[]

# Randomly select 50 paths
for _ in range(100000):
        if random.choices(mylist, weights = [1, 1000], k = 1)[0] == 1:
            selected_paths.append(next(path))
            if len(pts)>=50:  
                break
        next(path)

# Append selected paths to pts
pts.extend(selected_paths)


    
ct = 0    
for pth in pts:
    Paths.append([])
    for node in pth:
        nds = [int(nd) for nd in node.split() if nd.isdigit()]
        Paths[ct].append(nds)
    ct += 1

p=Paths  
g_algo(p)  #calls Genetic Algorithm module