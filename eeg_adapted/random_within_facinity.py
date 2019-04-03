import random

def rand(bx, by, ex, ey, level):
    step = []
    col_length = len(level)
    row_length = len(level[0])
    for row in range(col_length+10):
        lis = []
        for col in range(row_length+10):
            lis.append(50)
        step.append(lis)
    step[bx][by] = 0

    x_queue = [bx]
    y_queue = [by]

    while x_queue:
        x = x_queue.pop()
        y = y_queue.pop()

        if x+1<col_length-1 and step[x+1][y]>step[x][y]+1 and level[x+1][y]!='W':
            x_queue.append(x+1)
            y_queue.append(y)
            step[x+1][y] = step[x][y]+1
        if x-1>=0 and step[x-1][y]>step[x][y]+1 and level[x-1][y]!='W':
            x_queue.append(x-1)
            y_queue.append(y)
            step[x-1][y] = step[x][y]+1
        if y+1<row_length-1 and step[x][y+1]>step[x][y]+1 and level[x][y+1]!='W':
            x_queue.append(x)
            y_queue.append(y+1)
            step[x][y+1] = step[x][y]+1
        if y-1>=0 and step[x][y-1]>step[x][y]+1 and level[x][y-1]!='W':
            x_queue.append(x)
            y_queue.append(y-1)
            step[x][y-1] = step[x][y]+1

    direct_set = ['x', 'y']
    movement_set = [-1, 1]
    path = []
    for i in range(9):      
        if step[bx][by] <= 9:
            rand_direct = random.choice(direct_set)
            rand_movement = random.choice(movement_set)
            for delay in range(8):
                path.append((rand_direct, rand_movement))
        else:
            if bx<ex and level[x+1][y]!='W':
                for delay in range(8):
                    path.append(('x', 1))
            elif bx>ex and level[x-1][y]!='W':
                for delay in range(8):
                    path.append(('x', -1))
            if by<ey and level[x][y+1]!='W':
                for delay in range(8):
                    path.append(('y', 1))
            elif by>ey and level[x+1][y-1]!='W':
                for delay in range(8):
                    path.append(('y', -1))

    return path
    
        

            
