import random
# Step 1: create state value space, Q-values
v = [[0, 0, 0, 1], [0, 0, 0, -1], [0, 0, 0, 0]]
v_old = []
for i in range(3):
    row = v[i].copy()
    v_old.append(row)

v[0][1] = 100
R = 0.1
gamma = 0.9
probability = 0.8 # 80% lands to the action direction neighbor
# 20% lands on all the other possible neighbors

class qValues:
    def __init__(self):
        self.values = [0, 0, 0, 0]
    def __repr__(self):
        return f'{self.values}'

# initialize Q values
q = []
for i in range(3):
    row = []
    for j in range(4):
        temp_q = qValues()
        row.append(temp_q)
    q.append(row)

# define action space: right, down, left, up
action = ((1, 0), (0, 1), (-1, 0), (0, -1))

# Initialize a policy
pi = []
for i in range(3):
    row = []
    for j in range(4):
        a = random.randint(0, 3)
        row.append(a)
    pi.append(row)

# Policy Iteration
for i in range(10):

    # Policy Evaluation
    for idx in range(1):
        for y in range(3):
            for x in range(4):

                if (y, x) != (1, 1) and (y, x) != (0, 3) and (y, x) != (1, 3):

                    v[y][x] = R

                    for action_idx in range(4):

                        (xn, yn) = (x + action[action_idx][0],
                                    y + action[action_idx][1])

                        if (xn, yn) == (1, 1) or (xn < 0 or xn > 3) or (yn < 0 or yn > 2):
                            (xn, yn) = (x, y)

                        p = 0
                        if action_idx == pi[y][x]:
                            p = probability
                        else:
                            p = (1 - probability) / 3.0

                        v[y][x] += p * gamma * v_old[yn][xn]

    print('v')
    print(v)
    print('pi')
    print(pi)

    # Policy Improvement (max)
    for y in range(3):
        for x in range(4):
            if (y, x) != (1, 1) and (y, x) != (0, 3) and (y, x) != (1, 3):
                best_action = 0
                best_value = q[y][x].values[0]

                for a in range(4):
                    if q[y][x].values[a] > best_value:
                        best_value = q[y][x].values[a]
                        best_action = a

                pi[y][x] = best_action
