import math
import sys
import copy 

def depth_first(row,col,inp):
    def dfs(row,col,matrix,visit,level):
        global states
        global moves
        global sequence
        global visited
        visited=visit
        n=len(matrix)
        m=len(matrix[0])

        if level >= 15:
            return False
        if matrix == goal:
            moves = level
            for mat in visited:
                sequence.append([r[:] for r in mat])
            return True
        for direction in dirs:
            r_new,c_new=row+direction[0],col+direction[1]
            
            temp_inp = copy.deepcopy(matrix)
            if r_new>=0 and r_new<n and c_new>=0 and c_new<m:
                states +=1
                temp=temp_inp[row][col]
                temp_inp[row][col]=temp_inp[r_new][c_new]
                temp_inp[r_new][c_new]=temp  
                if temp_inp not in visited:
                    visited.append(temp_inp)
                    if dfs(r_new,c_new,temp_inp,visited,level+1):
                        return True
                    visited.pop()
        return False

    if dfs(row,col,inp,[inp],0):
        return True
    return False

def ids(row,col,inp):
    def dfs1(row,col,matrix,visit,level, max_level):
        global states
        global moves
        global sequence
        global visited
        visited=visit
        n=len(matrix)
        m=len(matrix[0])

        if level >= max_level:
            return False
        if matrix == goal:
            moves = level
            for mat in visited:
                sequence.append([r[:] for r in mat])
            return True
        for direction in dirs:        
            r_new,c_new=row+direction[0],col+direction[1]
            states +=1
            temp_inp = copy.deepcopy(matrix)
            if r_new>=0 and r_new<n and c_new>=0 and c_new<m:
                temp=temp_inp[row][col]
                temp_inp[row][col]=temp_inp[r_new][c_new]
                temp_inp[r_new][c_new]=temp  
                if temp_inp not in visited:
                    visited.append(temp_inp)
                    if dfs1(r_new,c_new,temp_inp,visited,level+1,max_level):
                        return True
                    visited.pop()
        return False

    for k in range(1, 16):
        if dfs1(row,col,inp,[inp],0, k):
            return True
    return False

def a_star(row,col,inp, htype):
    
    heuristic_vals = []
    goal_coord = {}
    global states
    global moves
    global sequence
    global visited


    n=len(inp)
    m=len(inp[0])

    for i in range(n):
        for j in range(m):
            goal_coord[goal[i][j]] = (i,j)

    def misplaced(current_matrix): #htype1, counts miplaced tiles
        count = 0
        for i in range(n):
            for j in range(m):
                if current_matrix[i][j] != goal[i][j]:
                    count += 1
        return count
    
    def manhattan_distance(current_matrix): #htype2, calculates manhattan distance
        distance = 0
        for i in range(n):
            for j in range(m):
                if goal_coord[current_matrix[i][j]] != (i,j):
                    goal_i, goal_j = goal_coord[current_matrix[i][j]]
                    distance = distance +abs((i - goal_i))+ abs((j - goal_j))
        return distance

    if htype == 1:
        init = misplaced(inp)
    else:
        init = manhattan_distance(inp)
    heuristic_vals.append((init,0,inp,row,col,[inp]))
    visited.append(inp)
    while heuristic_vals:
        f,level,grid,row,col,seq = heuristic_vals.pop(0)
        if level >= 15:
            return False
        if grid == goal:
            moves = level
            for mat in seq:
                sequence.append([r[:] for r in mat])
            return True

        for direction in dirs:
            r_new,c_new=row+direction[0],col+direction[1]
            states +=1
            temp_inp = copy.deepcopy(grid)
            if r_new>=0 and r_new<n and c_new>=0 and c_new<m:
                temp=temp_inp[row][col]
                temp_inp[row][col]=temp_inp[r_new][c_new]
                temp_inp[r_new][c_new]=temp 
                if temp_inp not in visited:
                    visited.append(temp_inp)
                    if htype == 1:
                        th = misplaced(temp_inp)
                    else:
                        th = manhattan_distance(temp_inp)
                    tg = level + 1
                    tf = th + tg
                    heuristic_vals.append((tf,tg,temp_inp,r_new,c_new,seq + [temp_inp]))
                    heuristic_vals = sorted(heuristic_vals)

def print_sequence(sequence):
    for i in sequence:
        for j in i:
            print(j)
        print("\n")

if __name__ == "__main__":
    goal = [['1','2','3'],['8','*','4'],['7','6','5']]
    dirs = [[0,1],[1,0],[-1,0],[0,-1]]
    states = 0
    moves = 0
    sequence = []
    algo = sys.argv[1] #algo type
    input_file = sys.argv[2] 
    visited=[]

    file1 = open(input_file, 'r') 
    input_grid = file1.readline()
    #print(input_grid)
    if input_grid[-1] == '\n':
        input_grid = input_grid[:-1]
    start = input_grid.split(" ")
    #print(start)
    if len(start) != 9:
        print("Invalid input.")
        exit()
    inp_cpy = [[-1 for _ in range(3)] for _ in range(3)]
    k = 0
    for i in range(3):
        for j in range(3):
            val = start[k]
            if val == '*':
                 row,col=i,j
            inp_cpy[i][j] = val
            k+=1
    
    if algo == "dfs":
        reached = depth_first(row,col,inp_cpy)
    elif algo == "ids":
        reached = ids(row,col,inp_cpy)
    elif algo == "astar1":
        reached = a_star(row,col,inp_cpy,1)
    elif algo == "astar2":
        reached = a_star(row,col,inp_cpy,2)
    else:
        print("Invalid algorithm value.")
        exit()
    if not reached:
        print("Goal state could not be reached.")
    else:
        print("Number of states : ",states)
        print("Number of moves : ", moves)
        print_sequence(sequence)