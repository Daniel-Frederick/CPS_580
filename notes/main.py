# MDP Practice
v = [10, 0, 0, 0, 1] # All states' values [a,b,c,d,e]
v_old = v.copy() # All states' values [a,b,c,d,e]

# Q-values, every two elements correspond to one v-value
q = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

gamma = .9 # Discounting factor
R = 1 # Reward R(s a, s')

for i in range(50):
    print(f"--------------Iteration {i} ---------------")
    for idx in range(1, 4): # Traverse all non-terminal states
        # Compute the two Q-values for the states
        q[2 * idx] = R + gamma * v_old[idx - 1] # Left neighbor
        q[2 * idx + 1] = R + gamma * v_old[idx + 1] # Right neighbor
        v[idx] = max(q[2 * idx], q[2 * idx + 1])
        print(f"V[{idx}]: {v[idx]}, Q({q[2*idx]}, {q[2*idx+1]})")


    # Replace v_old by v
    v_old = v.copy()


