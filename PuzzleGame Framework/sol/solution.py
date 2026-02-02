#This is the only file you need to work on. You do NOT need to modify other files

# Below are the functions you need to implement. For the first project, you only need to finish implementing iddfs() 
# ie iterative deepening depth first search

# run: `python3 -m game.puzzle`

# Successor Funciton - Given current state, it returns all possible next states

# here you need to implement the Iterative Deepening Search Method
def iterativeDeepening(puzzle):
    # Movement lookup table
    movement = {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 5],
        3: [0, 4, 6],
        4: [1, 3, 5, 7],
        5: [2, 4, 8],
        6: [3, 7],
        7: [4, 6, 8],
        8: [5, 7]
    }

    start = tuple(puzzle)
    goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    if start == goal:
        return []

    # Generate child states
    def expand(state):
        s = list(state)
        pos8 = s.index(8)
        children = []

        for next in movement[pos8]:
            new_s = s[:]

            # Swap positions
            new_s[pos8], new_s[next] = new_s[next], new_s[pos8]

            # store: (state, new position of 8)
            children.append((tuple(new_s), next))

        return children

    # Depth-limited Search
    def dls(limit):
        # (state, path_of_positions, depth)
        stack = [(start, [], 0)]
        visited = set()

        while stack:
            state, path, depth = stack.pop()
            visited.add(state)

            if state == goal:
                return path

            if depth < limit:
                for child_state, pos8_new in expand(state):
                    if child_state not in visited:
                        stack.append((child_state, path + [pos8_new], depth + 1))

        return None

    # Iterative Deepening Loop
    for limit in range(40):
        result = dls(limit)
        if result is not None:
            return result

    return []

def astar(puzzle):
    list = []
    return list

