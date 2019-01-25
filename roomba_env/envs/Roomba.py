import gym
import random
import pyglet
import math
from gym.envs.classic_control import rendering


#-------------------------------------------------------------------------------------------------------------------|
#                                                                                                                   |
#simple grid environment made to spawn two agents and make them compete against eachother using eg. multithreading  |
#                                                                                                                   |
#agents spawn at a fixed place                                                                                      |
#                                                                                                                   |
#goal of game: green agent should get at the top of the grid before the red agent is able to occupy it's position   |
#                                                                                                                   |
#actionspace= 5 (forward,backwards,left,right,stay)                                                                 |
#action space = 4 on the edge of the grid (agent is not allowed to leave it)                                        |
#action space = 3 on the very outer junctions of the grid (agent is not allowed to leave it)                        |
#state_space = 121 (every junction of the grid)                                                                     |
#                                                                                                                   |
#-------------------------------------------------------------------------------------------------------------------|


class RoombaEnv(gym.Env):

    metadata = {
        "render.modes": ["human", "rgb_array"],
    }




    def __init__(self):


        self.ACTION_ENEMY = ["F", "B", "L", "R", "S"]

        self.ACTION_FRIENDLY = ["F", "B", "L", "R", "S"]


        self.agents = ["enemy", "friendly"]

        self.viewer = None

        self.episodes = 0

        self.state_enemy = [350,350]
        self.state_friendly = [350,100]

        self.done = False


        self.info = {}

        self.reward_friendly = 0.0
        self.reward_enemy = 0.0

        self.render()


    def action_space(self):

        return len(self.ACTION_ENEMY)

    def _position_to_id(self, pos):

        #toch nog eens checken of dit wel klopt! (van mijn q value tabel was precies enkel de eerste ingevuld)
        return int(pos[0]/50 + (round(pos[1] / 100)-1)* 11 -1)

    def _id_top_position(self, id):
        pass

    def legal_actions(self, agent):



        if(agent == "enemy"):


        #check of ze op de rand staan ofniet (en dus niet uit de grid proberen te rijden)

            if (self.state_enemy[1] == 100 and self.state_enemy[0] != 100 and self.state_enemy[0] != 600):
                self.ACTION_ENEMY = [0, 2, 3, 4]
                return self.ACTION_ENEMY


            elif(self.state_enemy[1] == 600 and self.state_enemy[0] != 100 and self.state_enemy[0] != 600):

                self.ACTION_ENEMY = [1, 2, 3, 4]
                return self.ACTION_ENEMY


            elif(self.state_enemy[0] == 100 and self.state_enemy[1] != 100 and self.state_enemy[1] != 600):
                self.ACTION_ENEMY = [0, 1, 3, 4]
                return self.ACTION_ENEMY


            elif(self.state_enemy[0] == 600 and self.state_enemy[1] != 100 and self.state_enemy[1] != 600):
                self.ACTION_ENEMY = [0, 1, 2, 4]
                return self.ACTION_ENEMY



            elif(self.state_enemy == [100,100]):

                self.ACTION_ENEMY = [0, 3, 4]
                return self.ACTION_ENEMY


            elif (self.state_enemy == [100,600] ):

                self.ACTION_ENEMY = [1, 3, 4]
                return self.ACTION_ENEMY



            elif(self.state_enemy == [600,100]):

                self.ACTION_ENEMY = [0, 2, 4]
                return self.ACTION_ENEMY


            elif(self.state_enemy == [600,600]):
                self.ACTION_ENEMY = [1, 2, 4]
                return self.ACTION_ENEMY


            else:
                self.ACTION_ENEMY = [0, 1, 2, 3, 4]
                return self.ACTION_ENEMY



        elif(agent == "friendly"):

            if (self.state_friendly[1] == 100 and self.state_friendly[0] != 100 and self.state_friendly[0] != 600):
                self.ACTION_FRIENDLY = [0, 2, 3, 4]
                return self.ACTION_FRIENDLY


            elif(self.state_friendly[1] == 600 and self.state_friendly[0] != 100 and self.state_friendly[0] != 600):

                self.ACTION_FRIENDLY = [1, 2, 3, 4]
                return self.ACTION_FRIENDLY


            elif(self.state_friendly[0] == 100 and self.state_friendly[1] != 100 and self.state_friendly[1] != 600):
                self.ACTION_FRIENDLY = [0, 1, 3, 4]
                return self.ACTION_FRIENDLY


            elif(self.state_friendly[0] == 600 and self.state_friendly[1] != 100 and self.state_friendly[1] != 600):
                self.ACTION_FRIENDLY = [0, 1, 2, 4]
                return self.ACTION_FRIENDLY



            elif(self.state_friendly == [100,100]):

                self.ACTION_FRIENDLY = [0, 3, 4]
                return self.ACTION_FRIENDLY


            elif (self.state_friendly == [100,600] ):

                self.ACTION_FRIENDLY = [1, 3, 4]
                return self.ACTION_FRIENDLY



            elif(self.state_friendly == [600,100]):

                self.ACTION_FRIENDLY = [0, 2, 4]
                return self.ACTION_FRIENDLY


            elif(self.state_friendly == [600,600]):
                self.ACTION_FRIENDLY = [1, 2, 4]
                return self.ACTION_FRIENDLY


            else:
                self.ACTION_FRIENDLY = [0, 1, 2, 3, 4]
                return self.ACTION_FRIENDLY

    def state_space(self):

        return 121

    def agents(self):

        return self.agents

    def _check_done(self):

        self.done = bool(self.state_friendly[1] == 600 or self.state_enemy == self.state_friendly or self.state_friendly == self.state_enemy)
        return self.done

    def _check_reward(self,agent):



        if(self.state_friendly == self.state_enemy):

            self.reward_friendly -=1000
            self.reward_enemy += 1000

        elif(self.state_friendly[1] == 600):

            self.reward_friendly += 1000
            self.reward_enemy -= 1000

        else:
            if(agent == "enemy"):
                euclidean_distance_to_friendly = math.sqrt((self.state_friendly[0] - self.state_enemy[0]) ** 2 + (self.state_friendly[1] - self.state_enemy[1]) ** 2)
                self.reward_enemy -= 0.005 * math.pow(euclidean_distance_to_friendly,3)
                if(self.state_enemy[1] < self.state_friendly[1]):
                    self.reward_enemy -= 1000
            # print(euclidean_distance)
            else:
                distance_to_victory = 600 - self.state_friendly[1]
                euclidean_distance_to_enemy = math.sqrt((self.state_friendly[0] - self.state_enemy[0]) ** 2 + (self.state_friendly[1] - self.state_enemy[1]) ** 2)
                self.reward_friendly -= 0.004 * distance_to_victory
                self.reward_friendly += euclidean_distance_to_enemy * 0.001
                if(euclidean_distance_to_enemy == 50):
                    self.reward_friendly -= 1000
                # print(distance)

        return self.reward_friendly, self.reward_enemy

    def step(self, action, agent, render):

        if(agent == "enemy"):

            if(action == "F"):

                    index = 0
                    while index < 50:
                        self.state_enemy[1] += 1
                        if render:
                            self.render()
                        index +=1
                    self.done = self._check_done()
                    self.reward = self._check_reward("enemy")
                    return self._position_to_id(self.state_enemy), self.reward[1], self._position_to_id(self.state_friendly), self.done, self.info

            elif (action == "B"):

                    index = 0
                    while index < 50:
                        self.state_enemy[1] -= 1
                        if render:
                            self.render()
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward("enemy")
                    return self._position_to_id(self.state_enemy), self.reward[1],self._position_to_id(self.state_friendly), self.done, self.info

            elif (action == "R"):

                    index = 0
                    while index < 50:
                        self.state_enemy[0] += 1
                        if render:
                            self.render()
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward("enemy")
                    return self._position_to_id(self.state_enemy), self.reward[1],self._position_to_id(self.state_friendly), self.done, self.info

            elif (action == "L"):

                    index = 0
                    while index < 50:
                        self.state_enemy[0] -= 1
                        if render:
                            self.render()
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward("enemy")
                    return self._position_to_id(self.state_enemy), self.reward[1], self._position_to_id(self.state_friendly), self.done, self.info

            elif (action == "S"):

                self.state_enemy = self.state_enemy
                if render:
                    self.render()
                self.done = self._check_done()
                self.reward = self._check_reward("enemy")
                return self._position_to_id(self.state_enemy), self.reward[1],self._position_to_id(self.state_friendly), self.done, self.info

        elif agent == "friendly":

            if (action == "F"):

                    index = 0
                    while index < 50:
                        self.state_friendly[1] += 1
                        if render:
                            self.render()
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward("friendly")
                    return self._position_to_id(self.state_friendly), self.reward[0], self._position_to_id(self.state_enemy), self.done, self.info

            elif (action == "B"):

                    index = 0
                    while index < 50:
                        self.state_friendly[1] -= 1
                        if render:
                            self.render()
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward("friendly")
                    return self._position_to_id(self.state_friendly), self.reward[0],self._position_to_id(self.state_enemy), self.done, self.info

            elif (action == "R"):

                    index = 0
                    while index < 50:
                        self.state_friendly[0] += 1
                        if render:
                            self.render()
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward("friendly")
                    return self._position_to_id(self.state_friendly), self.reward[0],self._position_to_id(self.state_enemy), self.done, self.info

            elif (action == "L"):

                    index = 0
                    while index < 50:
                        self.state_friendly[0] -= 1
                        if render:
                            self.render()
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward("friendly")
                    return self._position_to_id(self.state_friendly), self.reward[0],self._position_to_id(self.state_enemy), self.done, self.info

            elif (action == "S"):

                self.state_friendly = self.state_friendly
                if render:
                    self.render()
                self.done = self._check_done()
                self.reward = self._check_reward("friendly")
                return self._position_to_id(self.state_friendly), self.reward[0],self._position_to_id(self.state_enemy), self.done, self.info

    def reset(self):

        self.state_enemy = [350, 350]
        self.state_friendly = [350, 100]

        self.ACTION_ENEMY = ["F", "B", "L", "R", "S"]

        self.ACTION_FRIENDLY = ["F", "B", "L", "R", "S"]

        self.reward_friendly = 0.0
        self.reward_enemy = 0.0

        self.episodes += 1

        self.info = {}

        self.done = False

        return self._position_to_id(self.state_enemy), self._position_to_id(self.state_friendly)

    def render(self, mode='human'):

        screen_width = 700
        screen_height = 700

        if self.viewer is None:

            self.viewer = rendering.Viewer(screen_width, screen_height)

            #GRID (static)

            index = 0

            row_values = [100,100,600,100]

            col_values = [100,100,100,600]

            while index <= 21:

                #ROWS
                if(index % 2 == 0):
                    self.line = rendering.Line((row_values[0], row_values[1]), (row_values[2], row_values[3]))
                    self.viewer.add_geom(self.line)
                    row_values[1] += 50
                    row_values[3] += 50

                #COLS
                else:
                    self.line = rendering.Line((col_values[0], col_values[1]), (col_values[2], col_values[3]))
                    self.viewer.add_geom(self.line)
                    col_values[0] += 50
                    col_values[2] += 50

                index+=1

            roombaradius = 20

            # ENEMY ROOMBA

            self.roomba_enemy = rendering.make_circle(roombaradius)
            self.roomba_enemy.set_color(255, 0, 0)
            self.roombatrans_enemy = rendering.Transform()
            self.roomba_enemy.add_attr(self.roombatrans_enemy)

            self.viewer.add_geom(self.roomba_enemy)

            # FRIENDLY ROOMBA

            self.roomba_friendly = rendering.make_circle(roombaradius)
            self.roomba_friendly.set_color(0, 255, 0)
            self.roombatrans_friendly = rendering.Transform()
            self.roomba_friendly.add_attr(self.roombatrans_friendly)

            self.viewer.add_geom(self.roomba_friendly)
            episodes = "Number of episodes: {0}".format(self.episodes)

        self.score_label = pyglet.text.Label('0000', font_size=36,
                                                 x=350, y=350, anchor_x='left', anchor_y='center',
                                                 color=(255, 255, 255, 255))

        self.score_label.text = "test"
        self.score_label.draw()

        self.roombatrans_enemy.set_translation(self.state_enemy[0], self.state_enemy[1])
        self.roombatrans_friendly.set_translation(self.state_friendly[0], self.state_friendly[1])

        return self.viewer.render()

    def close(self):

        if self.viewer:
            self.viewer.close()
            self.viewer = None