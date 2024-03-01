import math
import random

def perf(PATH1):
    #Finds performance measures
    def fittness(population,Q):
        #PATH LENGTH
        X = []
        Y = []
        # k=0
        for i in range(len(population)):
            weight = len(population)
            x = []
            y = []
            for j in range(len(population[i])):
                x.append(population[i][j][0])
                y.append(population[i][j][1])
            X.append(x)
            Y.append(y)
        angle_list = []
        # print("X", X)
        for i in range(len(X)):
            length = 0
            for j in range(len(X[i]) - 1):
                #Euclidean distance between node i and node i+1
                length = (length + (((X[i][j] - X[i][j + 1]) ** 2 + (Y[i][j] - Y[i][j + 1]) ** 2) ** 0.5)) 
        print("Path length = {:.4f}".format(length))

        #PATH SAFETY
        for i in range(len(X)):
            safety = 0
            COST = 1
            COUNT = 0
            for j in range(len(X[i])):
                x = X[i][j]  # x co-ord of node
                y = Y[i][j]  # y co-ord of node
                N = [] #Neighbour nodes
                
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
            safety = round(COST)
        print("Path safety = ", safety)
       
        #PATH SMOOTHNESS
        for i in range(len(X)):
            ang = [] #Angle of deviation
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
                    cost = cost + 15
                elif ang_deg == 90:
                    COUNT = COUNT + 1
                    cost = cost + 30
                elif ang_deg == 45:
                    COUNT = COUNT + 1
                    cost = cost + 45
                ang.append(ang_deg)
            smoothness = cost
            print("Path smoothness = ",smoothness)

    # Matrix input from map.txt file
    matrix=[]
    with open('map.txt') as f:
        rows = f.readlines()
        for row in rows:
            matrix.append(list(map(int, row.split(" "))))

    Q = [] #List of all walkable nodes
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                Q.append([i, j])
     
    population = PATH1
    start = population[0][0]
    dest = population[0][len(population[0]) - 1]
    fittness(population,Q) #calls fitness function

