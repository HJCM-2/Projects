import logging
import random
import gym

logger = logging.getLogger(__name__)


class GridEnv1(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 2
    }

    def __init__(self):
        # The 10*10 frozen lake environment has a total of 100 state spaces. Use a list structure to store.
        self.states = list(range(100))
        # Use list structure to store action space: up, down, left, and right
        self.actions = [0, 1, 2, 3]
        # Number of rows or columns
        self.size = 10

        # Generate 100 * 25% = 25 holes that are different from each other,
        # and make them not at the initial point and the position of the frisbee.
        self.s = []
        while len(self.s) < 25:
            x = random.randint(1, 98)
            if x not in self.s:
                self.s.append(x)
        # Remove termination state
        # Remove holes
        for i in self.s:
            self.states.remove(i)
        # Remove frisbee
        self.states.remove(99)

        # Set every possible center coordinate
        self.x = [30, 50, 70, 90, 110, 130, 150, 170, 190, 210] * 10
        self.y = [210] * 10 + [190] * 10 + [170] * 10 + [150] * 10 + [130] * 10 + \
                 [110] * 10 + [90] * 10 + [70] * 10 + [50] * 10 + [30] * 10

        # Use dictionary structure to store termination status
        self.terminate_states = dict()
        for i in self.s:
            self.terminate_states[i] = 1
        self.terminate_states[99] = 1

        # Use a dictionary to store reward,
        # the form of key is 'a_b', where a is the current state and b is the selected action.
        # Here are all possible situations that can reach the end state.
        self.rewards = dict()
        for i in self.s:
            self.rewards[str(i + self.size) + '_0'] = -1
            self.rewards[str(i - self.size) + '_1'] = -1
            self.rewards[str(i + 1) + '_2'] = -1
            self.rewards[str(i - 1) + '_3'] = -1
        self.rewards[str(99 - 10) + '_1'] = 1
        self.rewards[str(98) + '_3'] = 1

        # Use dictionary structure to store state transition
        self.t = dict()
        # '_0','_1','_2', and'_3' respectively indicate the state change of up, down, left, and right actions.
        # And keep it in the same state at the edge of the environment.
        for j in range(self.size, self.size * self.size):
            self.t[str(j) + '_0'] = j - self.size

        for j in range(self.size * (self.size - 1)):
            self.t[str(j) + '_1'] = j + self.size

        for j in range(1, self.size * self.size):
            if j % self.size == 0:
                continue
            self.t[str(j) + '_2'] = j - 1

        for j in range(self.size * self.size):
            if (j+1) % self.size == 0:
                continue
            self.t[str(j) + '_3'] = j + 1

        self.viewer = None
        self.state = None
        self.blue_circle = None

    def step(self, action):
        # Get the current state of the agent
        state = self.state
        # Use agent states and actions to form the keys of the dictionary
        key = str(state) + '_' + str(action)

        # Get the next state of the agent
        if key in self.t:
            next_state = self.t[key]
        else:
            next_state = state
        self.state = next_state

        # Initialize is_terminal to false to facilitate subsequent judgments whether to end the episode.
        is_terminal = False
        if next_state in self.terminate_states:
            is_terminal = True
        # Agent gets reward
        if key not in self.rewards:
            r = 0.0
        else:
            r = self.rewards[key]
        # Get the next state, reward, termination flag and information.
        return next_state, r, is_terminal, {}

    def reset(self):
        # The agent is initialized from the upper left corner
        self.state = self.states[0]
        return self.state

    def render(self, mode='human'):
        from gym.envs.classic_control import rendering
        # Set screen size
        screen_width = 240
        screen_height = 240

        if self.viewer is None:
            self.viewer = rendering.Viewer(screen_width, screen_height)

            # Create a visual environment:
            # In order to create a list structure with 22 objects, just temporarily fill it with zeros.
            line = [0]*22
            for j in range(11):
                # Create horizontal lines
                line[j] = rendering.Line((20, 20*(j+1)), (220, 20*(j+1)))
                # Create vertical lines
                line[j+11] = rendering.Line((20*(j+1), 20), (20*(j+1), 220))
                # Set the color of the lines to black
                line[j].set_color(0, 0, 0)
                line[j+11].set_color(0, 0, 0)
                # Add lines to the geometry
                self.viewer.add_geom(line[j])
                self.viewer.add_geom(line[j+11])

            # Create holes and set their color to red
            # In order to create a list structure with 25 holes, just temporarily fill it with zeros.
            holes = [0] * 25
            for i in range(25):
                # a, b represent the row and column number respectively
                a, b = self.s[i]//self.size, self.s[i] % self.size
                # c and d respectively produce the coordinates of the center of the circle
                c = (b + 1) * 20 + 10
                d = (self.size - a) * 20 + 10

                holes[i] = rendering.make_circle(8)
                red_circle = rendering.Transform(translation=(c, d))
                holes[i].add_attr(red_circle)
                holes[i].set_color(1, 0, 0)
                self.viewer.add_geom(holes[i])

            # Create frisbee and set its color to green
            diamond = rendering.make_circle(8)
            green_circle = rendering.Transform(translation=(210, 30))
            diamond.add_attr(green_circle)
            diamond.set_color(0, 1, 0)
            self.viewer.add_geom(diamond)

            # Create robot and set its color to blue
            # Set the size of the robot to a slightly smaller 6.
            robot = rendering.make_circle(6)
            self.blue_circle = rendering.Transform()
            robot.add_attr(self.blue_circle)
            robot.set_color(0, 0, 1)
            self.viewer.add_geom(robot)

        if self.state is None:
            return None
        # Visualization of robot movement
        self.blue_circle.set_translation(self.x[self.state], self.y[self.state])

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None