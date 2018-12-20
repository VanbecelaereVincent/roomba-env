import gym
import random
from gym.envs.classic_control import rendering


#-------------------------------------------------------------------------------------------------------------------|
#                                                                                                                   |
#simple grid environment made to spawn two agents and make them compete against eachother using eg. multithreading  |
#                                                                                                                   |
#agents spawn at a fixed place                                                                                      |
#                                                                                                                   |
#goal of game: green agent should get at the top of the grid before the red agent is able to occupy its position    |
#                                                                                                                   |
#actionspace= 5 (forward,backwards,left,right,stay)                                                                 |
#action space = 3 on the edge of the grid (agent is not allowed to leave it)                                        |
#action space = 3 on the very outer junctions of the grid (agent is not allowed to leave it)                        |
#state_space = 121 (every junction of the grid)                                                                     |
#                                                                                                                   |
#-------------------------------------------------------------------------------------------------------------------|


class RoombaEnv(gym.Env):

    metadata = {
        "render.modes": ["human", "rgb_array"],
    }


    #nog een 5e niet zo straight forward actie toevoegd: robot mag blijven staan (="S")

    def __init__(self):


        self.ACTION_ENEMY = ["F", "B", "L", "R", "S"]

        self.ACTION_FRIENDLY = ["F", "B", "L", "R", "S"]


        self.agents = ["enemy", "friendly"]

        self.viewer = None

        self.state_enemy = [350,350]
        self.state_friendly = [350,100]

        self.done = False

        #informatie die ik meegeef bij het nemen van een stap die goed is voor debugging
        self.info = {}

        self.reward_friendly = 0.0
        self.reward_enemy = 0.0

        self.render()


    def action_space(self):

        return len(self.ACTION_ENEMY)

    def action_space_sample(self, agent):


        if(agent == "enemy"):


        #check of ze op de rand staan ofniet (en dus niet uit de grid proberen te rijden)

            if (self.state_enemy[1] == 100 and self.state_enemy[0] != 100 and self.state_enemy[0] != 600):
                self.ACTION_ENEMY = ["F", "L", "R", "S"]
                self.info = [self.ACTION_ENEMY, "beneden"]
                number = random.randint(0, 3)
                return self.ACTION_ENEMY[number]

            elif(self.state_enemy[1] == 600 and self.state_enemy[0] != 100 and self.state_enemy[0] != 600):

                self.ACTION_ENEMY = ["B", "R", "L", "S"]
                self.info = [self.ACTION_ENEMY, "boven"]
                number = random.randint(0,3)
                return self.ACTION_ENEMY[number]

            elif(self.state_enemy[0] == 100 and self.state_enemy[1] != 100 and self.state_enemy[1] != 600):
                self.ACTION_ENEMY = ["F", "B", "R", "S"]
                self.info = [self.ACTION_ENEMY, "links"]
                number = random.randint(0,3)
                return self.ACTION_ENEMY[number]

            elif(self.state_enemy[0] == 600 and self.state_enemy[1] != 100 and self.state_enemy[1] != 600):
                self.ACTION_ENEMY = ["F", "B", "L", "S"]
                self.info = [self.ACTION_ENEMY, "rechts"]
                number = random.randint(0,3)
                return self.ACTION_ENEMY[number]


            elif(self.state_enemy == [100,100]):

                self.ACTION_ENEMY = ["F", "R", "S"]
                self.info = [self.ACTION_ENEMY, "benedenlinks"]
                number = random.randint(0, 2)
                return self.ACTION_ENEMY[number]

            elif (self.state_enemy == [100,600] ):

                self.ACTION_ENEMY = ["B", "R", "S"]
                self.info = [self.ACTION_ENEMY, "bovenlinks"]
                number = random.randint(0, 2)
                return self.ACTION_ENEMY[number]


            elif(self.state_enemy == [600,100]):

                self.ACTION_ENEMY = ["F", "L", "S"]
                self.info = [self.ACTION_ENEMY, "benedenrechts"]
                number = random.randint(0, 2)
                return self.ACTION_ENEMY[number]

            elif(self.state_enemy == [600,600]):
                self.ACTION_ENEMY = ["B", "L", "S"]
                self.info = [self.ACTION_ENEMY, "bovenrechts"]
                number = random.randint(0, 2)
                return self.ACTION_ENEMY[number]

            else:
                self.ACTION_ENEMY = ["F", "B", "L", "R", "S"]
                self.info = [self.ACTION_ENEMY, "niet speciaal"]
                number = random.randint(0,4)
                return self.ACTION_ENEMY[number]


        if(agent == "friendly"):

            if (self.state_friendly[1] == 100 and self.state_friendly[0] != 100 and self.state_friendly[0] != 600):
                self.ACTION_FRIENDLY = ["F", "L", "R", "S"]
                self.info = [self.ACTION_FRIENDLY, "beneden"]
                number = random.randint(0, 3)
                return self.ACTION_FRIENDLY[number]

            elif(self.state_friendly[1] == 600 and self.state_friendly[0] != 100 and self.state_friendly[0] != 600):

                self.ACTION_FRIENDLY = ["B", "R", "L", "S"]
                self.info = [self.ACTION_FRIENDLY, "boven"]
                number = random.randint(0,3)
                return self.ACTION_FRIENDLY[number]

            elif(self.state_friendly[0] == 100 and self.state_friendly[1] != 100 and self.state_friendly[1] != 600):
                self.ACTION_FRIENDLY = ["F", "B", "R", "S"]
                self.info = [self.ACTION_FRIENDLY, "links"]
                number = random.randint(0,3)
                return self.ACTION_FRIENDLY[number]

            elif(self.state_friendly[0] == 600 and self.state_friendly[1] != 100 and self.state_friendly[1] != 600):
                self.ACTION_FRIENDLY = ["F", "B", "L", "S"]
                self.info = [self.ACTION_FRIENDLY, "rechts"]
                number = random.randint(0,3)
                return self.ACTION_FRIENDLY[number]


            elif(self.state_friendly == [100,100]):

                self.ACTION_FRIENDLY = ["F", "R", "S"]
                self.info = [self.ACTION_FRIENDLY, "benedenlinks"]
                number = random.randint(0, 2)
                return self.ACTION_FRIENDLY[number]

            elif (self.state_friendly == [100,600] ):

                self.ACTION_FRIENDLY = ["B", "R", "S"]
                self.info = [self.ACTION_FRIENDLY, "bovenlinks"]
                number = random.randint(0, 2)
                return self.ACTION_FRIENDLY[number]


            elif(self.state_friendly == [600,100]):

                self.ACTION_FRIENDLY = ["F", "L", "S"]
                self.info = [self.ACTION_FRIENDLY, "benedenrechts"]
                number = random.randint(0, 2)
                return self.ACTION_FRIENDLY[number]

            elif(self.state_friendly == [600,600]):
                self.ACTION_FRIENDLY = ["B", "L", "S"]
                self.info = [self.ACTION_FRIENDLY, "bovenrechts"]
                number = random.randint(0, 2)
                return self.ACTION_FRIENDLY[number]

            else:
                self.ACTION_FRIENDLY = ["F", "B", "L", "R", "S"]
                self.info = [self.ACTION_FRIENDLY, "niet speciaal"]
                number = random.randint(0,4)
                return self.ACTION_FRIENDLY[number]



    def state_space(self):

        return 121

    def agents(self):

        return self.agents


    def _check_done(self):

        #sommige scenarios: ene agent krijgt done binnen & reset. Door deze directe reset krijgt de andere agent nooit done binnen
        #en doet hij gewoon verder

        self.done = bool(self.state_friendly[1] == 600 or self.state_enemy == self.state_friendly or self.state_friendly == self.state_enemy)
        return self.done


    def _check_reward(self):


        #dit klopt nog niet helemaal heb ik het gevoel

        # verdediger: krijgt -100 als de andere de overkant haalt, krijgt + 100 als hij op de positie van de andere graakt
        #aanvaller: krijgt + 100 als hij de overkant haalt: krijgt -100 als de andere roomba op hem rijdt

        if(self.state_friendly == self.state_enemy):

            self.reward_friendly -=100
            self.reward_enemy +=100

        elif(self.state_friendly[1] == 600):

            self.reward_friendly += 100
            self.reward_enemy -= 100

        #mss een elif die checkt hoe dicht de twee roombas bij elkaar zijn?

        else:

            self.reward_enemy = self.reward_enemy
            self.reward_friendly = self.reward_friendly

        return self.reward_friendly, self.reward_enemy


    def step(self,action, agent):

        if(agent == "enemy"):


            if(action == "F"):

                    index = 0
                    while index < 50:
                        self.state_enemy[1] += 1
                        index +=1
                    self.done = self._check_done()
                    self.reward = self._check_reward()
                    return self.state_enemy, self.reward[1], self.done, self.info

            elif (action == "B"):

                    index = 0
                    while index < 50:
                        self.state_enemy[1] -= 1
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward()
                    return self.state_enemy, self.reward[1], self.done, self.info

            elif (action == "R"):

                    index = 0
                    while index < 50:
                        self.state_enemy[0] += 1
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward()
                    return self.state_enemy, self.reward[1], self.done, self.info


            elif (action == "L"):

                    index = 0
                    while index < 50:
                        self.state_enemy[0] -= 1
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward()
                    return self.state_enemy, self.reward[1], self.done, self.info

            elif (action == "S"):

                self.state_enemy = self.state_enemy
                self.done = self._check_done()
                self.reward = self._check_reward()
                return self.state_enemy, self.reward[1], self.done, self.info


        elif agent == "friendly":

            if (action == "F"):

                    index = 0
                    while index < 50:
                        self.state_friendly[1] += 1
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward()
                    return self.state_friendly, self.reward[1], self.done, self.info

            elif (action == "B"):

                    index = 0
                    while index < 50:
                        self.state_friendly[1] -= 1
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward()
                    return self.state_friendly, self.reward[0], self.done, self.info

            elif (action == "R"):

                    index = 0
                    while index < 50:
                        self.state_friendly[0] += 1
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward()
                    return self.state_friendly, self.reward[0], self.done, self.info

            elif (action == "L"):

                    index = 0
                    while index < 50:
                        self.state_friendly[0] -= 1
                        index += 1

                    self.done = self._check_done()
                    self.reward = self._check_reward()
                    return self.state_friendly, self.reward[0], self.done, self.info

            elif (action == "S"):

                self.state_friendly = self.state_friendly
                self.done = self._check_done()
                self.reward = self._check_reward()
                return self.state_friendly, self.reward[0], self.done, self.info


    def reset(self):

        self.state_enemy = [350, 350]
        self.state_friendly = [350, 100]

        self.ACTION_ENEMY = ["F", "B", "L", "R", "S"]

        self.ACTION_FRIENDLY = ["F", "B", "L", "R", "S"]

        self.reward_friendly = 0.0
        self.reward_enemy = 0.0

        self.info = {}

        self.done = False


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




        self.roombatrans_enemy.set_translation(self.state_enemy[0], self.state_enemy[1])
        self.roombatrans_friendly.set_translation(self.state_friendly[0], self.state_friendly[1])

        return self.viewer.render()


    def close(self):

        if self.viewer:
            self.viewer.close()
            self.viewer = None