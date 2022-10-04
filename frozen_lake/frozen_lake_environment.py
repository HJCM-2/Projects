import logging
import gym

logger = logging.getLogger(__name__)


class GridEnv1(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 2
    }

    def __init__(self):
        # The 4*4 frozen lake environment has a total of 16 state spaces. Use a list structure to store.
        self.states = list(range(16))
        # Use list structure to store action space: up, down, left, and right
        self.actions = [0, 1, 2, 3]
        # Number of rows or columns
        self.size = 4

        # Remove termination state (including holes and frisbee)
        self.states.remove(5)
        self.states.remove(7)
        self.states.remove(11)
        self.states.remove(12)
        self.states.remove(15)
        # Use dictionary structure to store termination status
        self.terminate_states = dict()
        self.terminate_states[5] = 1
        self.terminate_states[7] = 1
        self.terminate_states[11] = 1
        self.terminate_states[12] = 1
        self.terminate_states[15] = 1

        # Set every possible center coordinate
        self.x = [150, 250, 350, 450] * 4
        self.y = [450] * 4 + [350] * 4 + [250] * 4 + [150] * 4

        # Use a dictionary to store reward,
        # the form of key is 'a_b', where a is the current state and b is the selected action.
        # Here are all possible situations that can reach the end state.
        self.rewards = dict()
        self.rewards['1_1'] = -1.0
        self.rewards['4_3'] = -1.0
        self.rewards['6_2'] = -1.0
        self.rewards['9_0'] = -1.0

        self.rewards['3_1'] = -1.0
        self.rewards['6_3'] = -1.0

        self.rewards['10_3'] = -1.0
        self.rewards['13_2'] = -1.0

        self.rewards['8_1'] = -1.0

        self.rewards['14_3'] = 1.0

        # Use dictionary structure to store state transition
        self.t = dict()

        # '_0','_1','_2', and'_3' respectively indicate the state change of up, down, left, and right actions.
        # And keep it in the same state at the edge of the environment.
        for i in range(self.size, self.size * self.size):
            self.t[str(i) + '_0'] = i - 4

        for i in range(self.size * (self.size - 1)):
            self.t[str(i) + '_1'] = i + 4

        for i in range(1, self.size * self.size):
            if i % self.size == 0:
                continue
            self.t[str(i) + '_2'] = i - 1

        for i in range(self.size * self.size):
            if (i+1) % self.size == 0:
                continue
            self.t[str(i) + '_3'] = i + 1

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
        screen_width = 600
        screen_height = 600

        if self.viewer is None:
            self.viewer = rendering.Viewer(screen_width, screen_height)

            # Create a visual environment:
            # Create horizontal lines
            line1 = rendering.Line((100,100),(500,100))
            line2 = rendering.Line((100, 200), (500, 200))
            line3 = rendering.Line((100, 300), (500, 300))
            line4 = rendering.Line((100, 400), (500, 400))
            line5 = rendering.Line((100, 500), (500, 500))
            # Create vertical lines
            line6 = rendering.Line((100, 100), (100, 500))
            line7 = rendering.Line((200, 100), (200, 500))
            line8 = rendering.Line((300, 100), (300, 500))
            line9 = rendering.Line((400, 100), (400, 500))
            line10 = rendering.Line((500, 100), (500, 500))

            # Set the color of the lines to black
            line1.set_color(0, 0, 0)
            line2.set_color(0, 0, 0)
            line3.set_color(0, 0, 0)
            line4.set_color(0, 0, 0)
            line5.set_color(0, 0, 0)
            line6.set_color(0, 0, 0)
            line7.set_color(0, 0, 0)
            line8.set_color(0, 0, 0)
            line9.set_color(0, 0, 0)
            line10.set_color(0, 0, 0)

            # Create holes and set their color to red
            # Set the center coordinates of the representative object

            # Create the first hole
            hole1 = rendering.make_circle(40)
            red_circle = rendering.Transform(translation=(150, 150))
            hole1.add_attr(red_circle)
            hole1.set_color(1, 0, 0)

            # Create the second hole
            hole2 = rendering.make_circle(40)
            red_circle = rendering.Transform(translation=(250, 350))
            hole2.add_attr(red_circle)
            hole2.set_color(1, 0, 0)

            # Create the third hole
            hole3 = rendering.make_circle(40)
            red_circle = rendering.Transform(translation=(450, 250))
            hole3.add_attr(red_circle)
            hole3.set_color(1, 0, 0)

            # Create the fourth hole
            hole4 = rendering.make_circle(40)
            red_circle = rendering.Transform(translation=(450, 350))
            hole4.add_attr(red_circle)
            hole4.set_color(1, 0, 0)

            # Create frisbee and set its color to green
            frisbee = rendering.make_circle(40)
            green_circle = rendering.Transform(translation=(450, 150))
            frisbee .add_attr(green_circle)
            frisbee .set_color(0, 1, 0)

            # Create robot and set its color to blue
            # Set the size of the robot to a slightly smaller 30.
            robot = rendering.make_circle(30)
            self.blue_circle = rendering.Transform()
            robot.add_attr(self.blue_circle)
            robot.set_color(0, 0, 1)

            # Add these created objects to the geometry
            self.viewer.add_geom(line1)
            self.viewer.add_geom(line2)
            self.viewer.add_geom(line3)
            self.viewer.add_geom(line4)
            self.viewer.add_geom(line5)
            self.viewer.add_geom(line6)
            self.viewer.add_geom(line7)
            self.viewer.add_geom(line8)
            self.viewer.add_geom(line9)
            self.viewer.add_geom(line10)
            self.viewer.add_geom(hole1)
            self.viewer.add_geom(hole2)
            self.viewer.add_geom(hole3)
            self.viewer.add_geom(hole4)
            self.viewer.add_geom(frisbee)
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