import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


class RoombaEnv(gym.Env):

    metadata = {
        "render.modes": ["human", "rgb_array"],
    }

    ACTION = ["F", "B", "L", "R"]

    def __init__(self):


        self.viewer = None

        self.min_position = -1.2
        self.max_position = 0.6

        self.start_position = [300,200]

        #deze zal ik moeten instellen naar helemaal bovenaan (dus y zoveel, x mag omheteven wat zijn)
        self.goal_position = None



    def step(self,action):

        self.start_position[0] += 10
        self.start_position[1] += 10


    def reset(self):
        pass


    def render(self, mode='human'):
        screen_width = 600
        screen_height = 400


        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

            roombaradius = 20


            self.roomba_enemy = rendering.make_circle(roombaradius)
            self.roomba_enemy.add_attr(rendering.Transform(translation=(10, 10)))

            self.cartrans_enemy = rendering.Transform()
            self.roomba_enemy.add_attr(self.cartrans_enemy)
            self.viewer.add_geom(self.roomba_enemy)


        self.cartrans_enemy.set_translation(self.start_position[0], self.start_position[1])



        return self.viewer.render(return_rgb_array=mode == 'rgb_array')


    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None