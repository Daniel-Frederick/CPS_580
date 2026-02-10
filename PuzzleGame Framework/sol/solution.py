import heapq

# This is the only file you need to work on. You do NOT need to modify other files

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

    # Calculates the sum of distances
    def get_distance(state):
        distance = 0
        for i in range(9):
            tile = state[i]
            if tile != 8:  # Don't count the blank space
                # Current position
                curr_r, curr_c = divmod(i, 3)

                # Goal position
                goal_r, goal_c = divmod(tile, 3)
                distance += abs(curr_r - goal_r) + abs(curr_c - goal_c)
        return distance

    # h_score: heuristic; f_score: g + h
    start_h = get_distance(start)

    # Priority Queue: (f_score, g_score, current_state, path_of_moves)
    # f_score - the formula: `f = g + h`
    # g_score - number of steps to reach current_state
    # current_state - the given state the puzzle is in
    # path_of_moves - record of moves made so far
    queue = [(start_h, 0, start, [])]

    # Keep track of visited states
    visited = {start: 0}

    while queue:
        f, g, current_state, path = heapq.heappop(queue)

        if current_state == goal:
            return path

        pos8 = current_state.index(8)

        for move_to in movement[pos8]:
            new_state_list = list(current_state)
            new_state_list[pos8], new_state_list[move_to] = new_state_list[move_to], new_state_list[pos8]
            new_state = tuple(new_state_list)

            new_g = g + 1
            
            # Continue expanding states if there is a better path
            if new_state not in visited or new_g < visited[new_state]:
                visited[new_state] = new_g
                h = get_distance(new_state)
                heapq.heappush(queue, (new_g + h, new_g, new_state, path + [move_to]))

    return []

