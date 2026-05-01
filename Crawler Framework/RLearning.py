
"""
@author: Ju Shen
@email: jshen1@udayton.edu
@date: 02-16-2026
"""
import random
import numpy as np
import math as mth

# The state class
class State:
    def __init__(self, angle1=0, angle2=0):
        self.angle1 = angle1
        self.angle2 = angle2

class ReinforceLearning:

    #
    def __init__(self, unit=5):

        ####################################  Needed: here are the variable to use  ################################################

        # The crawler agent
        self.crawler = 0

        # Number of iterations for learning
        self.steps = 1000

        # learning rate alpha
        self.alpha = 0.2

        # Discounting factor
        self.gamma = 0.95

        # E-greedy probability
        self.epsilon = 0.1

        self.Qvalue = []  # Update Q values here
        self.unit = unit  # 5-degrees
        self.angle1_range = [-35, 55]  # specify the range of "angle1"
        self.angle2_range = [0, 180]  # specify the range of "angle2"
        self.rows = int(1 + (self.angle1_range[1] - self.angle1_range[0]) / unit)  # the number of possible angle 1
        self.cols = int(1 + (self.angle2_range[1] - self.angle2_range[0]) / unit)  # the number of possible angle 2

        ########################################################  End of Needed  ################################################



        self.pi = [] # store policies
        self.actions = [-1, +1] # possible actions for each angle

        # Controlling Process
        self.learned = False



        # Initialize all the Q-values
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                for a in range(9):
                    row.append(0.0)
            self.Qvalue.append(row)



        # Initialize all the action combinations
        self.actions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))


        # Initialize the policy
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(random.randint(0, 8))
            self.pi.append(row)


    # Reset the learner to empty
    def reset(self):
        self.Qvalue = [] # store Q values
        self.R = [] # not working
        self.pi = [] # store policies

        # Initialize all the Q-values
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                for a in range(9):
                    row.append(0.0)
            self.Qvalue.append(row)

        # Initiliaize all the Reward
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                for a in range(9):
                    row.append(0.0)
            self.R.append(row)

        # Initialize all the action combinations
        self.actions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))


        # Initialize the policy
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(random.randint(0, 8))
            self.pi.append(row)

        # Controlling Process
        self.learned = False

    # Set the basic info about the robot
    def setBot(self, crawler):
        self.crawler = crawler


    def storeCurrentStatus(self):
        self.old_location = self.crawler.location
        self.old_angle1 = self.crawler.angle1
        self.old_angle2 = self.crawler.angle2
        self.old_contact = self.crawler.contact
        self.old_contact_pt = self.crawler.contact_pt
        self.old_location = self.crawler.location
        self.old_p1 = self.crawler.p1
        self.old_p2 = self.crawler.p2
        self.old_p3 = self.crawler.p3
        self.old_p4 = self.crawler.p4
        self.old_p5 = self.crawler.p5
        self.old_p6 = self.crawler.p6

    def reverseStatus(self):
        self.crawler.location = self.old_location
        self.crawler.angle1 = self.old_angle1
        self.crawler.angle2 = self.old_angle2
        self.crawler.contact = self.old_contact
        self.crawler.contact_pt = self.old_contact_pt
        self.crawler.location = self.old_location
        self.crawler.p1 = self.old_p1
        self.crawler.p2 = self.old_p2
        self.crawler.p3 = self.old_p3
        self.crawler.p4 = self.old_p4
        self.crawler.p5 = self.old_p5
        self.crawler.p6 = self.old_p6



    def updatePolicy(self):
        # After convergence, generate policy y
        for r in range(self.rows):
            for c in range(self.cols):
                max_idx = 0
                max_value = -1000
                for i in range(9):
                    if self.Qvalue[r][9 * c + i] >= max_value:
                        max_value = self.Qvalue[r][9 * c + i]
                        max_idx = i

                # Assign the best action
                self.pi[r][c] = max_idx


    # This function will do additional saving of current states than Q-learning
    def onLearningProxy(self, option):
        self.storeCurrentStatus()
        if option == 0:
            self.onMonteCarlo()
        elif option == 1:
            self.onTDLearning()
        elif option == 2:
            self.onQLearning()
        self.reverseStatus()


        # Turn off learned
        self.learned = True



    # For the play_btn uses: choose an action based on the policy pi
    def onPlay(self, ang1, ang2, mode=1):

        epsilon = self.epsilon

        ang1_cur = ang1
        ang2_cur = ang2

        # get the state index
        r = int((ang1_cur - self.angle1_range[0]) / self.unit)
        c = int((ang2_cur - self.angle2_range[0]) / self.unit)

        # Choose an action and udpate the angles
        idx, angle1_update, angle2_update = self.chooseAction(r=r, c=c)
        ang1_cur += self.unit * angle1_update
        ang2_cur += self.unit * angle2_update

        return ang1_cur, ang2_cur



    ####################################  Needed: here are the functions you need to use  ################################################

    # epsilon = e-greedy
    # gamma = discount
    # alpha = Learning rate

    # This function is similar to the "runReward()" function but without returning a reward.
    # It only update the robot position with the new input "angle1" and "angle2"
    def setBotAngles(self, ang1, ang2):
        self.crawler.angle1 = ang1
        self.crawler.angle2 = ang2
        self.crawler.posConfig()

    # Method 1: Monte Carlo learning
    def onMonteCarlo(self):
        """
        Monte Carlo on-policy control with epsilon-greedy.
        For each episode:
          1. Generate a trajectory using the current epsilon-greedy policy.
          2. Compute the total return G (x-displacement of the crawler).
          3. Update every (state, action) pair visited in the episode.
        """

        epsilon = self.epsilon
        gamma   = self.gamma

        # We'll use a returns accumulator: sum_returns[r][col_action] and count[r][col_action]
        # so we can do incremental first-visit MC averaging across all episodes.
        # (We re-use the existing Qvalue array and just do simple averaging via a running mean.)

        # How many episodes we run is controlled by self.steps (each "step" = one episode here,
        # matching the MC convention where steps = number of episodes / 10 set by the GUI).
        num_episodes = self.steps

        for _ in range(num_episodes):

            # --- 1. Generate one episode (trajectory) ---
            # Start from the current crawler position (already stored/restored externally)
            ang1 = self.crawler.angle1
            ang2 = self.crawler.angle2
            init_x = self.crawler.location[0]

            trajectory = []  # list of (r, c, action_idx, angle1_update, angle2_update)

            # Random-length episode: between 5 and 30 steps
            episode_len = random.randint(5, 30)

            for _ in range(episode_len):
                r = int((ang1 - self.angle1_range[0]) / self.unit)
                c = int((ang2 - self.angle2_range[0]) / self.unit)

                # Clamp indices to valid range
                r = max(0, min(r, self.rows - 1))
                c = max(0, min(c, self.cols - 1))

                idx, a1_upd, a2_upd = self.chooseAction(r, c)
                trajectory.append((r, c, idx))

                # Move the bot
                new_ang1 = ang1 + a1_upd * self.unit
                new_ang2 = ang2 + a2_upd * self.unit
                self.setBotAngles(new_ang1, new_ang2)
                ang1 = self.crawler.angle1
                ang2 = self.crawler.angle2

            # --- 2. Compute total return = x-displacement ---
            final_x = self.crawler.location[0]
            G = final_x - init_x   # positive = moved forward (right)

            # --- 3. First-visit MC update for each (state, action) in the trajectory ---
            visited = set()
            for (r, c, idx) in trajectory:
                key = (r, c, idx)
                if key not in visited:
                    visited.add(key)
                    col = c * 9 + idx
                    # Incremental mean update: Q <- Q + alpha * (G - Q)
                    self.Qvalue[r][col] += self.alpha * (G - self.Qvalue[r][col])

        return


    # Method 2: TD online learning based on SARSA
    def onTDLearning(self):
        """
        On-policy TD control: SARSA.
        For each step in self.steps:
          - Choose action A from state S using epsilon-greedy.
          - Take action, observe reward r and next state S'.
          - Choose next action A' from S' using epsilon-greedy.
          - Update: Q(S,A) <- Q(S,A) + alpha * [r + gamma*Q(S',A') - Q(S,A)]
        """

        epsilon = self.epsilon
        gamma   = self.gamma
        alpha   = self.alpha

        ang1 = self.crawler.angle1
        ang2 = self.crawler.angle2

        for _ in range(self.steps):
            r = int((ang1 - self.angle1_range[0]) / self.unit)
            c = int((ang2 - self.angle2_range[0]) / self.unit)
            r = max(0, min(r, self.rows - 1))
            c = max(0, min(c, self.cols - 1))

            # Choose action A (epsilon-greedy)
            idx, a1_upd, a2_upd = self.chooseAction(r, c)

            # Record position before move
            old_x = self.crawler.location[0]

            # Take action
            new_ang1 = ang1 + a1_upd * self.unit
            new_ang2 = ang2 + a2_upd * self.unit
            self.setBotAngles(new_ang1, new_ang2)

            # Reward = change in x position
            reward = self.crawler.location[0] - old_x

            # Next state
            ang1_next = self.crawler.angle1
            ang2_next = self.crawler.angle2
            r_next = int((ang1_next - self.angle1_range[0]) / self.unit)
            c_next = int((ang2_next - self.angle2_range[0]) / self.unit)
            r_next = max(0, min(r_next, self.rows - 1))
            c_next = max(0, min(c_next, self.cols - 1))

            # Choose next action A' (epsilon-greedy) — SARSA uses the actual next action
            idx_next, _, _ = self.chooseAction(r_next, c_next)

            # SARSA update
            q_current = self.Qvalue[r][c * 9 + idx]
            q_next    = self.Qvalue[r_next][c_next * 9 + idx_next]
            self.Qvalue[r][c * 9 + idx] += alpha * (reward + gamma * q_next - q_current)

            ang1 = ang1_next
            ang2 = ang2_next

        return

    # Given the current state, return an action index and angle1_update, angle2_update
    # Return values:
    #  - index: any number from 0 to 8, which indicates the next action to take (epsilon-greedy)
    #  - angle1_update: -1, 0, or +1
    #  - angle2_update: -1, 0, or +1
    def chooseAction(self, r, c):
        """
        Epsilon-greedy action selection.
        With probability epsilon  -> pick a random action index (0-8)
        With probability 1-epsilon -> pick the greedy (max Q) action index
        """

        epsilon = self.epsilon

        # Epsilon-greedy: explore with probability epsilon
        if random.random() < epsilon:
            idx = random.randint(0, 8)
        else:
            # Greedy: find the action with the highest Q-value for state (r, c)
            max_val = float('-inf')
            idx = 0
            for i in range(9):
                if self.Qvalue[r][c * 9 + i] > max_val:
                    idx = i
                    max_val = self.Qvalue[r][c * 9 + i]

        (angle1_update, angle2_update) = self.actions[idx]

        # If out of range, clamp to 0 (no movement in that direction)
        if angle1_update * self.unit + self.crawler.angle1 < self.angle1_range[0] or \
           angle1_update * self.unit + self.crawler.angle1 > self.angle1_range[1]:
            angle1_update = 0

        if angle2_update * self.unit + self.crawler.angle2 < self.angle2_range[0] or \
           angle2_update * self.unit + self.crawler.angle2 > self.angle2_range[1]:
            angle2_update = 0

        return idx, angle1_update, angle2_update


    # Method 3: TD-online learning based on Bellman operator (Q-learning)
    def onQLearning(self):
        """
        Off-policy TD control: Q-learning (Bellman).
        For each step in self.steps:
          - Choose action A from state S using epsilon-greedy.
          - Take action, observe reward r and next state S'.
          - Update: Q(S,A) <- Q(S,A) + alpha * [r + gamma * max_a Q(S',a) - Q(S,A)]
        The key difference from SARSA: we use max over next actions (off-policy).
        """

        epsilon = self.epsilon
        gamma   = self.gamma
        alpha   = self.alpha

        ang1 = self.crawler.angle1
        ang2 = self.crawler.angle2

        for _ in range(self.steps):
            r = int((ang1 - self.angle1_range[0]) / self.unit)
            c = int((ang2 - self.angle2_range[0]) / self.unit)
            r = max(0, min(r, self.rows - 1))
            c = max(0, min(c, self.cols - 1))

            # Choose action A (epsilon-greedy for behavior policy)
            idx, a1_upd, a2_upd = self.chooseAction(r, c)

            # Record position before move
            old_x = self.crawler.location[0]

            # Take action
            new_ang1 = ang1 + a1_upd * self.unit
            new_ang2 = ang2 + a2_upd * self.unit
            self.setBotAngles(new_ang1, new_ang2)

            # Reward = change in x position
            reward = self.crawler.location[0] - old_x

            # Next state
            ang1_next = self.crawler.angle1
            ang2_next = self.crawler.angle2
            r_next = int((ang1_next - self.angle1_range[0]) / self.unit)
            c_next = int((ang2_next - self.angle2_range[0]) / self.unit)
            r_next = max(0, min(r_next, self.rows - 1))
            c_next = max(0, min(c_next, self.cols - 1))

            # Q-learning update: use max Q over all next actions (greedy target policy)
            max_q_next = max(self.Qvalue[r_next][c_next * 9 + i] for i in range(9))

            q_current = self.Qvalue[r][c * 9 + idx]
            self.Qvalue[r][c * 9 + idx] += alpha * (reward + gamma * max_q_next - q_current)

            ang1 = ang1_next
            ang2 = ang2_next

        return

