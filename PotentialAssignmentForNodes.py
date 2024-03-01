# Function to generate potential map
def potential_map_gen(matrix, dest):
    # Variable declaration
    OPEN = []  # List of nodes without Eo
    CLOSE = []  # List of nodes with them and neighbour Eo
    TEMP = []  # List of nodes with Eo
    Pq = []  # List of Eo in sequence as CLOSE index
    Q = []  # List for node being assigned Eo
    potential_matrix = matrix  # Filling potential_matrix to have same num of elements as matrix
    Eo = 3000  # Initial Destination Eo

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            OPEN.append([i, j])  # Add all nodes to OPEN (OPEN = [all])
            if matrix[i][j] == 0:
                Q.append([i, j])  # Add obstacle nodes to Q (Q = [obstacles])
    
    # For obstacle nodes Eo assignment
    for i in Q:
        if i in OPEN:
            OPEN.remove(i)  # Remove obstacle nodes from OPEN (OPEN = [all - obstacles])
   

    for i in Q:
        Pq.append(-Eo)  # Assign -ve Eo to obstacle in Pq sequence
        CLOSE.append(i)  # Add obstacle nodes to CLOSE (CLOSE = [obstacles])

    Q = []  # Remove obstacle nodes from Q (Q = [])

    # For destination node Eo assignment
    Q.append(dest)  # Add dest node to Q (Q = [dest])
    Pq.append(Eo)  # Add dest Eo to Pq

    for i in Q:
        TEMP.append(i)  # Add dest node to TEMP (TEMP = [dest])
        OPEN.remove(i)  # Remove dest node from OPEN (OPEN = [all - obstacles - dest])
    

    # Nested function to find neighbour of first node from TEMP and assign Eo
    def N_loop(TEMP, CLOSE, OPEN, Pq, Eo, Q):
        N = []  # List of neighbour not in TEMP|CLOSE
        Q = [TEMP[0]]

        x = Q[0][0]  # x co-ord of node
        y = Q[0][1]  # y co-ord of node

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

        # Removing neighbours with Eo
        N_rem = []
        for i in N:
            if i in OPEN:
                N_rem.append(i)
        N = N_rem

        for i in N:
            Pq.append(Eo - 10)  # Add Eo corresponding to each neighbour in Pq

        CLOSE.append(TEMP[0])  # Neighbour assigned Eo so TEMP[0] is CLOSE (CLOSE = [obstacles + TEMP[0]])
        TEMP.remove(Q[0])  # Remove first element from TEMP
        TEMP = TEMP + N  # Neighbour's neighbours may not have Eo so TEMP <-- N

        OPEN_rem = []
        for i in OPEN:
            if i not in N:
                OPEN_rem.append(i)  # Neighbours removed from OPEN
        OPEN = OPEN_rem

        N = []  # Neighbour cleared
        return [TEMP, CLOSE, OPEN, Pq, Eo, Q]

    while len(TEMP) != 0:  # End of while means all nodes have Eo
        Eo = Pq[len(CLOSE)]
        LST = N_loop(TEMP, CLOSE, OPEN, Pq, Eo, Q)
        TEMP = LST[0]
        CLOSE = LST[1]
        OPEN = LST[2]
        Pq = LST[3]
        Eo = LST[4]
        Q = LST[5]

        # If OPEN is empty then all nodes have Eo so TEMP is CLOSED
    CLOSE = CLOSE + TEMP
    TEMP = []

    # Mapping nodes from CLOSE to Eq from Pq and generating potential_matrix
    ct = 0
    for i in CLOSE:
        potential_matrix[i[0]][i[1]] = Pq[ct]
        ct += 1

    return potential_matrix


# Main Program
# Matrix input from map.txt file
matrix = []
with open('map.txt') as f:
    rows = f.readlines()
    for row in rows:
        matrix.append(list(map(int, row.split(" "))))
print("Matrix = ")
for i in matrix:
    print(i)

# Destination input
d = input("Enter destination as i,j (eg. 35,44): ")
dest = d.split(",")
dest[0] = int(dest[0])
dest[1] = int(dest[1])

# Calling potential_map_gen function
potential_matrix = potential_map_gen(matrix, dest)

# Potential map output to map_out.txt file
row = ""
for rows in potential_matrix:
    for i in rows:
        row = row + str("{0:6}".format(i))
    row = row + "\n"
    with open('potential_matrix.txt', 'w') as f:
        f.write(row)

print("Potential Matrix = ")
for i in potential_matrix:
    print(i)
