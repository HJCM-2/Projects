import numpy as np
import random
from frozen_lake_environment import GridEnv1
from matplotlib import pyplot as plt


class Agent(object):
    def __init__(self, env):
        # Initialize the state of the agent
        self.s = env.states
        # Initialize the terminal state of the agent
        self.terminate_states = env.terminate_states
        # Initialize the action of the agent
        self.a = env.actions
        # The total number of agent actions
        self.a_size = 4
        # Initialize the Q table randomly. Since there are 16 states and 4 actions, it is 16*4.
        self.Q = np.random.rand(16, 4)
        # If it is a terminal state, its Q value is set to 0.
        for i in self.terminate_states:
            for j in self.a:
                self.Q[i, j] = 0

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
        if random.uniform(0, 1) < epsilon:
            a = random.choice(range(4))
        else:
            a = np.argmax(self.Q[s])
        return a


# Set up the environment
env = GridEnv1()
# Specify agent
agent = Agent(env=env)
# Set the learning rate for Q table update
alpha = 0.1
# The purpose of setting the exploration rate, the maximum value and the minimum value
# is to reduce the exploration in the later stage and stabilize the Q meter.
epsilon = 0.1
epsilon_min = 0.0  # 0.01
# The value between 0-1 reflects whether there is a long-term consideration for reward.
# The more it tends to 1, the longer the consideration.
gamma = 0.99
# Total number of episodes
episode = 3000  # 1000
# If the terminal state is not reached within such steps, stop and enter the next episode.
step = 30  # 100

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
    # Based on the Q table, use ε-greedy to select A from S
    a = agent.epsilon_greedy_policy(s)
    for j in range(step):
        # The agent interacts with the environment to get the next state,
        # the corresponding reward and whether it is a termination state
        s1, r, terminal, _ = env.step(a)
        if terminal == 1:
            # If it is a terminal state, target_Q is reward.
            agent.Q[s, a] = agent.Q[s, a] + alpha * (r - agent.Q[s, a])
            if s1 == 15:
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
        # Based on the Q table, use ε-greedy to select a1 from s1
        # Use the same strategy as the behavioral strategy to evaluate
        a1 = agent.epsilon_greedy_policy(s1)
        # For the case that is not a terminal state, target_Q is R+γ Q(S′, A′)−Q(S,A)
        agent.Q[s, a] = agent.Q[s, a] + alpha * (r + gamma * agent.Q[s1, a1] - agent.Q[s, a])
        # Visually refresh the environment
        env.render()
        # Use the next state as the current processing state
        s = s1
        # Use the next action as the current processing action
        a = a1

    # Real-time visualization drawing: average target rate and average number of steps
    if i % 20 == 0 and i != 0:
        plt.ion()
        y = target_num/finish_episode
        average_step = total_steps/finish_episode
        x_list.append(i/20)
        y_list.append(y)
        step_list.append(average_step)
        print('Target_rate:', y)
        print('Average_step:', average_step)
        plt.figure(1)
        plt.title("Target_rate")
        plt.xlabel("Every 20 episodes")
        plt.ylabel("Target rate in every 20 episodes")
        plt.plot(x_list, y_list)
        plt.savefig('./Target_rate_sarsa.jpg')
        plt.draw()
        # time.sleep(5)
        plt.figure(2)
        plt.title("Average_step")
        plt.xlabel("Every 20 episodes")
        plt.ylabel("Average_step for every 20 episodes")
        plt.plot(x_list, step_list)
        plt.savefig('./Average_step_sarsa.jpg')
        plt.draw()
        # time.sleep(5)
        # Clear the count every 20 episodes.
        target_num = 0
        total_steps = 0
        finish_episode = 0
    # The exploration rate decreases as the number of episodes increases
    epsilon = epsilon - (epsilon - epsilon_min) / episode
# Finally output Q table
print(agent.Q)






