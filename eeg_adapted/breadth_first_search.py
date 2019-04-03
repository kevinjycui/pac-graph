def bfs(by, bx, ey, ex, level):
    step = []
##    print(bx, by, ex, ey)
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

        if x+1<col_length and step[x+1][y]>step[x][y]+1 and level[x+1][y]!='W':
            x_queue.append(x+1)
            y_queue.append(y)
            step[x+1][y] = step[x][y]+1
        if x-1>=0 and step[x-1][y]>step[x][y]+1 and level[x-1][y]!='W':
            x_queue.append(x-1)
            y_queue.append(y)
            step[x-1][y] = step[x][y]+1
        if y+1<row_length and step[x][y+1]>step[x][y]+1 and level[x][y+1]!='W':
            x_queue.append(x)
            y_queue.append(y+1)
            step[x][y+1] = step[x][y]+1
        if y-1>=0 and step[x][y-1]>step[x][y]+1 and level[x][y-1]!='W':
            x_queue.append(x)
            y_queue.append(y-1)
            step[x][y-1] = step[x][y]+1

    path = []
    x = ex
    y = ey
    prev_x = x
    prev_y = y

##    print(step[ex][ey])
##
##    for row in range(col_length):
##        for col in range(row_length):
##            if len(str(step[row][col]))==1:
##                print(step[row][col], end="  ")
##            else:
##                print(step[row][col], end=" ")
##        print()
##    print()
    
    while len(path) != step[ex][ey]:
        if x+1<col_length and step[x+1][y]==step[x][y]-1:
            for delay in range(8):
                path.append(('y', -1))
            x += 1
        if x-1>=0 and step[x-1][y]==step[x][y]-1:
            for delay in range(8):
                path.append(('y', 1))
            x -= 1
        if y+1<row_length and step[x][y+1]==step[x][y]-1:
            for delay in range(8):
                path.append(('x', -1))
            y += 1
        if y-1>=0 and step[x][y-1]==step[x][y]-1:
            for delay in range(8):
                path.append(('x', 1))
            y -= 1
        if x==prev_x and y==prev_y:
            path.append(('n', 0))
            break
        prev_x = x
        prev_y = y

    return path
