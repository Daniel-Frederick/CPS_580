import random

# State value space
v = [[0, 0, 0, 1],
    [0, 0, 0 -1],
    [0, 0, 0, 0]]

v_old = v.copy()

# Q-value object contains 4 values for actions
class qValues:
    def __init__(self):
        self.values = [0, 0, 0, 0]

    def __repr__(self):
        return f'{self.values}'

# Q-value value space
q = []
for i in range(3):
    row = []
    for j in range(4):
        temp_q = qValues()
        row.append(temp_q)

    q.append(row)

# Action space
action = (
    (1, 0), # Right
    (0, 1), # Down
    (-1, 0), # Left
    (0, -1)) # Up

# Init Policy
pi = []
for i in range(3):
    row = []
    for j in range(4):
        a = random.randint(0, 3) # Random action
        row.append(a)

    pi.append(row)

print(pi)

# Policy Iterations
for i in range(300):

    # Policy Evaluation
    for idx in range(50):

        for y in range(3): # Row
            for x in range(4):
                (xn, yn) = (x, y) + action(pi[x][y])

            # Is xn, yn the wall
            if (xn, yn) == (1, 1) or (x < 0 or x > 4) or (y < 0 or y >= 2):
                (sn, yn) = (x, y)

