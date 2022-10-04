import numpy as np
import random
from frozen_lake_environment_10 import GridEnv1
from matplotlib import pyplot as plt


class Agent(object):
    def __init__(self, env):
        # Initialize the state of the agent
        self.s = env.states
        # Initialize the action of the agent
        self.a = env.actions
        # The total number of agent actions
        self.a_size = 4
        # Initialize the Q table randomly. Since there are 16 states and 4 actions, it is 16*4.
        self.Q = np.random.rand(100, 4)
        # Store the whole process of state transition of an episode.
        self.history = []
    # Algorithms tried

    # def epsilon_greedy_policy(self, s):
    #     # pi = np.zeros(self.a_size)
    #     greedy_a = np.argmax(self.Q[s])
    #     pi = [epsilon_max / self.a_size]*self.a_size
    #     pi[greedy_a] = 1 - epsilon_max + epsilon_max / self.a_size
    #     return np.random.choice(self.a, p=pi)

    # For actions that do not make Q the maximum,
    # the selection probability is the real_epsilon / self.a_size, which guarantees epsilon_soft_policy,
    # but since it is a number, it can be written as epsilon directly.
    def epsilon_greedy_policy(self, s):
        if random.random() < epsilon:
            a = random.choice(range(4))
        else:
            a = np.argmax(self.Q[s])
        return a

    def Returns(self):
        # Initialize return = 0
        G = 0
        # Use the dict structure to store the return of each state in an episode.
        Returns = {}
        # The advantage of using dict with reversed history is that
        # the return of the same state can be overwritten
        # by the return value that arrived in that state for the first time.
        for k in reversed(self.history):
            # It is more convenient to use reversed history to calculate return
            G = gamma * G + k[2]
            Returns[k[0]] = G
        return Returns

    def update(self, returns):
        # Use the set structure to determine whether the state has been visited
        s_dict = set()
        # Taking out the state, action, reward of a complete episode
        for m in self.history:
            # If it is not in the set structure, it is the first visit.
            if m[0] not in s_dict:
                s_dict.add(m[0])
                # Update the Q value of the state action pair by using alpha
                self.Q[m[0], m[1]] = self.Q[m[0], m[1]] + alpha * (returns[m[0]] - self.Q[m[0], m[1]])
        return self.Q


# Set up the environment
env = GridEnv1()
# Specify agent
agent = Agent(env=env)
# Set the learning rate for Q table update
alpha = 0.1
# The purpose of setting the exploration rate, the maximum value and the minimum value
# is to reduce the exploration in the later stage and stabilize the Q meter.
epsilon = 0.1
epsilon_min = 0.0
# The value between 0-1 reflects whether there is a long-term consideration for reward.
# The more it tends to 1, the longer the consideration.
gamma = 0.99
# Total number of episodes
episode = 3000
step = 50

# Data used to plot the average target rate and the number of steps in real time
target_num = 0
total_steps = 0
finish_episode = 0
x_list = []
y_list = []
step_list = []

# Main function
for i in range(episode):
    # Initialize the environment
    s = env.reset()
    agent.history = []
    for j in range(step):
        # Based on the Q table, use ε-greedy to select A from S
        a = agent.epsilon_greedy_policy(s)
        # The agent interacts with the environment to get the next state,
        # the corresponding reward and whether it is a termination state
        s1, r, terminal, _ = env.step(a)
        # Add state actions and rewards into history
        agent.history.append([s, a, r])
        if terminal == 1:
            if s1 == 99:
                # If it reaches the frisbee, count towards the target.
                print("goal")
                target_num += 1
            else:
                # Otherwise fall into the hole and output "failure"
                print("fail")

            # As long as the end state is reached within the specified number of steps (steps),
            # true_step j will be counted into total_steps to facilitate subsequent calculation of the average value.
            total_steps += j
            # Count of episodes that reach the end state
            finish_episode += 1
            break
        # Use the next state as the current processing state
        s = s1
        env.render()
    # When an episode is completed, get the return of each state in this episode
    returns = agent.Returns()
    # Update the Q value of the corresponding state
    agent.update(returns)
    # The exploration rate decreases as the number of episodes increases
    epsilon = epsilon - (epsilon - epsilon_min) / episode

    # Real-time visualization drawing: average target rate and average number of steps
    if i % 20 == 0 and i != 0:
        plt.ion()
        y = target_num / finish_episode
        average_step = total_steps / finish_episode
        x_list.append(i / 20)
        y_list.append(y)
        step_list.append(average_step)
        print('Target_rate:', y)
        print('Average_step:', average_step)
        plt.figure(1)
        plt.title("Target_rate")
        plt.xlabel("Every 20 episodes")
        plt.ylabel("Target rate in every 20 episodes")
        plt.plot(x_list, y_list)
        plt.savefig('./Target_rate_10_mc_alpha.jpg')
        plt.draw()
        # time.sleep(5)
        plt.figure(2)
        plt.title("Average_step")
        plt.xlabel("Every 20 episodes")
        plt.ylabel("Average_step for every 20 episodes")
        plt.plot(x_list, step_list)
        plt.savefig('./Average_step_10_mc_alpha.jpg')
        plt.draw()
        # time.sleep(5)
        # Clear the count every 20 episodes.
        target_num = 0
        total_steps = 0
        finish_episode = 0

print(agent.Q)
