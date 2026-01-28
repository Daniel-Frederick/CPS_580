#This is the only file you need to work on. You do NOT need to modify other files

# Below are the functions you need to implement. For the first project, you only need to finish implementing iddfs() 
# ie iterative deepening depth first search

# run: `python3 -m game.puzzle`

# Successor Funciton - Given current state, it returns all possible next states

# here you need to implement the Iterative Deepening Search Method
def iterativeDeepening(puzzle):
    # puzzle = 1D list of current state

    # Create movement table
    # 1. Where "8" appears
    # 2. All the next possible new possitions for "8"
    movement = [][]
    movement[0] = [1,3]
    movement[4] = [1,3,5,7]

    # The sequence of "8" positions
    path = [] # Shortest path
    return path

def astar(puzzle):
    list = []
    return list

