import random

v = [[0, 0, 0, 1],
     [0, 0, 0, -1],
     [0, 0, 0, 0]]
v_old = []

for i in range(3):
    row = v[i].copy()
    v_old.append(row)

v[0][1] = 100
print(v_old[0][1])

R = 0.1
gamma = 0.9

probability = 0.8  # 80% lands to the action direction neighbor
# 20% lands on all the other possible neighbors

# Q-value object contains 4 values for actions
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

print(pi)

# Policy Iteration
for i in range(1):

    # Policy Evaluation
    for idx in range(1):

        for y in range(3):
            for x in range(4):

                if (x, y) != (1, 1) and (x, y) != (3, 0) and (x, y) != (3, 1):

                    (xn, yn) = (x + action[pi[y][x]][0],
                                y + action[pi[y][x]][1])

                    # find neighbor state
                    if (xn, yn) == (1, 1) or (xn < 0 or xn > 3) or (yn < 0 or yn > 2):
                        (xn, yn) = (x, y)

                    val = 0

                    # intended direction (80%)
                    val += probability * v_old[yn][xn]

                    # other directions share remaining 20%
                    others = [a for a in range(4) if a != pi[y][x]]
                    share = (1 - probability) / len(others)

                    for a in others:
                        xn2 = x + action[a][0]
                        yn2 = y + action[a][1]

                        if (xn2, yn2) == (1, 1) or (xn2 < 0 or xn2 > 3) or (yn2 < 0 or yn2 > 2):
                            xn2, yn2 = x, y

                        val += share * v_old[yn2][xn2]

                    v[y][x] = R + gamma * val

                    print(f'({y}, {x}): action {pi[y][x]}, neighbor({yn}, {xn}), {v[y][x]}, {v_old[yn][xn]}')

print(v)
