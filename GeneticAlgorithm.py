import numpy as np
import random
import math
from collections import OrderedDict
import sys
import time
from Performance import perf
sys.setrecursionlimit(2000)
from GUI import gui

def g_algo(p):
    def ga(population, matrix,gen,Population):
        # Calculating probability for roulette wheel selection
        gen=gen+1
        beta = 1
        fitness1 = []

        for i in range(len(Population)):
            # list of all the population fitness
            f=Population[i]['fitness']
            fitness1.append(f)
        fitness1 = np.array(fitness1)
        avg_fitness = np.mean(fitness1)
        if avg_fitness != 0:
            fitness1 = fitness/avg_fitness
        probs = np.exp(-beta * fitness1)

        p1 = Population[roulette_wheel_selection(probs)]
        p2 = Population[roulette_wheel_selection(probs)]

        #crossover
        offspring = []
        crossover(p1, p2, offspring, population, matrix,Q,gen,Population)


    def roulette_wheel_selection(p):
        c = np.cumsum(p)
        r = sum(p) * np.random.rand()
        ind = np.argwhere(r <= c)
        return ind[0][0]

    #Crossover operator
    def crossover(p1, p2, offspring, population, matrix,Q,gen,Population):
        offspring = []
        c1 = [] #crossover child 1
        c2 = [] #crossover child 2
        pl1 = len(p1['chromosome'])
        pl2 = len(p2['chromosome'])
        if (pl1 != pl2):
            p_min_l = min(pl1, pl2)
            if (p_min_l == pl1):
                p_min = p1['chromosome']
                p_max = p2['chromosome']
            else:
                p_min = p2['chromosome']
                p_max = p1['chromosome']
        else:
            p_min = p1['chromosome']
            p_max = p2['chromosome']

        x1 = [] #list of all x co-ordinates of parent 1
        x2 = [] #list of all x co-ordinates of parent 2
        y1 = [] #list of all y co-ordinates of parent 1
        y2 = [] #list of all y co-ordinates of parent 2
        xf = [] #list of all x co-ordinates of child
        yf = [] #list of all y co-ordinates of child
        for i in p_min:
            x = i[0]
            y = i[1]

            x1.append(x)
            y1.append(y)

        for i in range(len(p_min)):
            j = p_max[i]
            x = j[0]
            y = j[1]

            x2.append(x)
            y2.append(y)

        for i in range(len(x1)):
            xf.append(round((x1[i] + x2[i]) / 2))

        for i in range(len(y1)):
            yf.append(round((y1[i] + y2[i]) / 2))

        for i in range(len(xf)):
            c1.append([xf[i], yf[i]])

        xf = []
        yf = []
        a = random.uniform(-1, 1)
        for i in range(len(x1)):
            xf.append(round(abs((a * x1[i]) + ((1 - a) * x2[i]))))

        for i in range(len(y1)):
            yf.append(round(abs(a * y1[i]) + ((1 - a) * y2[i])))

        for i in range(len(xf)):
            c2.append([xf[i], yf[i]])

        offspring.append(c1)
        offspring.append(c2)
        #Calling mutation operator
        mutation(p1, offspring, population, matrix,Q,gen,Population)

    #Mutation operator
    def mutation(p1, offspring, population, matrix,Q,gen,Population):
        x1 = [] #list of all x co-ordinates of parent
        y1 = [] #list of all y co-ordinates of parent 
        xf = [] #list of all x co-ordinates of child
        yf = [] #list of all x co-ordinates of child
        a = 0.5
        b = 1
        m1 = [] #Mutation child
        for i in p1['chromosome']:
            x = i[0]
            y = i[1]
            x1.append(x)
            y1.append(y)

        for i in range(len(x1)):
            if (i == 0) or (i == len(x1) - 1):
                xf.append(x1[i])
                yf.append(y1[i])
            elif i != 0 and i != len(x1) - 1:
                xfi =round(abs( x1[i] + (a * (x1[i - 1] - x1[i])) + (b * (x1[i + 1] - x1[i]))))
                yfi = round(abs(y1[i] + (a * (y1[i - 1] - y1[i])) + (b * (y1[i + 1] - y1[i]))))
                xf.append(xfi)
                yf.append(yfi)
        for i in range(len(xf)):
            m1.append([xf[i], yf[i]])
        offspring.append(m1)
        #Calling deletion operator
        deletion(offspring, population, matrix, start, dest,Q,gen,Population)
    
    #Deletion operator
    def deletion(offspring, population, matrix, start, dest,Q,gen,Population):
        Q = [] #list of all obstacle nodes
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    Q.append([i, j])
        OPEN = [] #list of all walkable nodes
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                 OPEN.append([i, j])

        d = [] #list of offspring to be deleted
        #removing infeasible paths
        for i in offspring:
            for j in i:
                if ((j in Q) or ((i[0] != start) and (i[len(i) - 1] != dest))):
                    d.append(i)
                if j not in OPEN:
                    d.append(i)
        
        #removing duplicate paths
        for i in offspring:
            dupes = [x for n, x in enumerate(i) if x in i[:n]]
            if len(dupes)>0:
                d.append(i)

        for i in d:
            if i in offspring:
                offspring.remove(i)

        temp = population
        population = offspring
        flag=1 
        #calling objective function
        fittness(population, Q, matrix, temp,flag,gen,Population)
    
    #Objective function
    def fittness(population, Q, matrix, temp,flag,gen,Population):
        X = []
        Y = []
        for i in range(len(population)):
            weight = len(population)
            x = []
            y = []
            for j in range(len(population[i])):
                x.append(population[i][j][0])
                y.append(population[i][j][1])
            X.append(x)
            Y.append(y)
        fitness = [] #list of fitness value of all paths
        f1 = [] #path length
        f2 = [] #path safety
        f3 = [] #path smoothness
        angle_list = []

        #PATH LENGTH
        for i in range(len(X)):
            length = 0
            for j in range(len(X[i]) - 1):
                #Euclidean distance between node i and node i+1
                length = (length + (((X[i][j] - X[i][j + 1]) ** 2 + (Y[i][j] - Y[i][j + 1]) ** 2) ** 0.5))
            f1.append(length*10)
        
        #PATH SAFETY
        for i in range(len(X)):
            safety = 0
            COST = 1
            COUNT = 0
            for j in range(len(X[i])):
                x = X[i][j]  # x co-ord of node
                y = Y[i][j]  # y co-ord of node
                N = [] # Neighbour nodes

                # For edge nodes of matrix neighbour node calc.
                if ((x == 0) | (x == len(matrix) - 1) | (y == 0) | (y == len(matrix) - 1)):
                    # Adjacent neighbours
                    if x != 0:
                        N.append([x - 1, y])
                    if y != 0:
                        N.append([x, y - 1])
                    if x != len(matrix) - 1:
                        N.append([x + 1, y])
                    if y != len(matrix) - 1:
                        N.append([x, y + 1])

                    # Diagonal neighbours
                    if (x != 0 and y != 0):
                        N.append([x - 1, y - 1])
                    if (x != 0 and y != len(matrix) - 1):
                        N.append([x - 1, y + 1])
                    if (x != len(matrix) - 1 and y != 0):
                        N.append([x + 1, y - 1])
                    if (x != len(matrix) - 1 and y != len(matrix) - 1):
                        N.append([x + 1, y + 1])

                # For inner nodes of matrix neighbour node calc.
                else:
                    # Adjacent neighbours
                    N.append([x - 1, y])
                    N.append([x, y - 1])
                    N.append([x + 1, y])
                    N.append([x, y + 1])

                    # Diagonal neighbours
                    N.append([x - 1, y - 1])
                    N.append([x - 1, y + 1])
                    N.append([x + 1, y - 1])
                    N.append([x + 1, y + 1])
                COST=1
                for k in range(len(N)):
                    if N[k] in Q:
                        COUNT = COUNT + 1
                        #Euclidean distance between node i and obstacle
                        COST = COST + (((X[i][j] - N[k][0]) ** 2) + ((Y[i][j] - N[k][1]) ** 2) ** 0.5)
                COST = COUNT/COST
            safety = COST
            f2.append(safety)

        #PATH SMOOTHNESS 
        for i in range(len(X)):
            ang = [] # angle of deviation
            cost = 0
            Count = 0

            for j in range(len(X[i]) - 2):
                A = []
                B = []

                A = [(X[i][j] - X[i][j + 1]), (Y[i][j] - Y[i][j + 1])]
                B = [(X[i][j + 1] - X[i][j + 2]), (Y[i][j + 1] - Y[i][j + 2])]
                AB = A[0] * B[0] + A[1] * B[1]
                modA = float(A[0] ** 2 + A[1] ** 2) ** 0.5
                modB = float(B[0] ** 2 + B[1] ** 2) ** 0.5
                #cosine law
                angle = math.acos((float(AB) / float(modA * modB)))
                ang_deg = round(math.degrees(angle))
                ang_deg = 180 - ang_deg
                #Assigning weights or cost for the angles
                if ang_deg == 180:
                    cost = cost + 0
                elif ang_deg == 135:
                    COUNT = COUNT + 1
                    cost = cost + 30
                elif ang_deg == 90:
                    COUNT = COUNT + 1
                    cost = cost + 60
                elif ang_deg == 45:
                    COUNT = COUNT + 1
                    cost = cost + 90
                ang.append(ang_deg)

            smoothness = cost*COUNT
            f3.append((smoothness))
        
        #Fitness values of the paths
        for i in range(len(X)):
            #Fitness value = sum of length ,safety and smoothness of a path
            fitness.append(round(f1[i] + f2[i] + f3[i]))

        if flag==1:
            Offspring={}
            #Appending Fitness to the offsprings dict
            for i in range(len(population)):
                Offspring[i]={'chromosome': population[i], 'fitness': fitness[i]}
            
            #Appending offsprings to the population
            for t in range(len(Offspring)):
                Population[len(Population)]=Offspring[t]
            
            #Sorting population based on fitness
            def sort_pop(Population):
                pop=dict(OrderedDict(sorted(Population.items(), key=lambda x: x[1]['fitness'])))
                return pop
            Population=sort_pop(Population)

            n = 50 # no. of generations
            #Terminal condition
            if (gen == n):
                path=[]
                print("GA Completed for", n, " generations")
                print("Optimal path = ", Population[1]['chromosome'])
                print("Runtime of GA  = %.4f Seconds" % (time.time() - start_time))
                PATH1=[Population[1]['chromosome']]
                #Calls Performance module
                perf(PATH1)
                PATH1= Population[1]['chromosome']
                lab="EGA"
                #Calls GUI module
                gui(PATH1,lab)
            while (gen != n):
                return ga(population, matrix, gen, Population)
        elif flag==0:
            return fitness

    # Matrix input from map.txt file
    matrix = []
    paths =p
    with open('map.txt') as f:
        rows = f.readlines()
        for row in rows:
            matrix.append(list(map(int, row.split(" "))))

    Q = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                Q.append([i, j])

    population = paths
    start = paths[0][0]
    dest = paths[0][len(paths[0]) - 1]
    Population = {} 
    temp=[]
    flag=0 
    gen=0 #initial generation 
    fitness=fittness(population, Q, matrix, temp,flag,gen,Population)

    for i in range(len(population)):
        Population[i] = {'chromosome': population[i], 'fitness': fitness[i]}

    print("Running GA...")
    print("Initial Population = ",len(paths))
    start_time = time.time()
    ga(population, matrix,gen,Population)


