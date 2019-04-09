import random

def rand():
    direct_set = ['x', 'y']
    movement_set = [-1, 1]
    path = []
    for i in range(9):      
            rand_direct = random.choice(direct_set)
            rand_movement = random.choice(movement_set)
            for delay in range(8):
                path.append((rand_direct, rand_movement))
    return path
    
        

            
