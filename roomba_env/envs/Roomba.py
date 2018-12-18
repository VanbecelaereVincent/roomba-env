import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


class RoombaEnv(gym.Env):

    metadata = {
        "render.modes": ["human", "rgb_array"],
    }


    #nog een 5e niet zo straight forward actie toevoegd: robot mag blijven staan (="S")
    ACTION = ["F", "B", "L", "R", "S"]

    def __init__(self):

        self.viewer = None

        self.min_position_x = 100
        self.max_position_x = 600

        self.min_position_y = 100
        self.max_position_y = 600

        self.current_position_enemy = [350,350]
        self.current_position_friendly = [350,100]

        #deze zal ik moeten instellen naar helemaal bovenaan (dus y zoveel, x mag omheteven wat zijn)
        self.goal_position_friendly = ["mag alles zijn", 600]

        self.goal_position_enemy = "dit moet de positie van de andere roomba zijn"


        #deze wordt op true gezet als het environment klaar is en opnieuw gereset moet worden..
        #moet ik meegeven bij het nemen van een step
        #wordt aangepast als de friendlyroomba de overkant haalde, of als ze gebotst zijn (zijnde de enemy wint)
        self.done = False


        #dit is een specifieke observatie van het spel die ik terug geef bij het nemen van een step
        #ik veronderstel dat dit bij mij de positie van de roombas zal zijn
        self.observation = None

        #van de enemy is dit steeds de positie waar de andere staat natuurlijk


        #informatie die ik meegeef bij het nemen van een stap die goed is voor debugging
        #bijvoorbeeld de positie van de roomba
        self.info = {}


        #de reward die de agent krijgt voor de stap
        self.reward = 0.0




        self.render(mode="human")


    #zodat de gebruiker die acties kan opvragen
    def action_space(self):

        return self.ACTION


    #wat zet ik hier in? gebruiker zou moeten de observation space terug krijgen
    def observation_space(self):

        pass


    def step(self,action):

        #deze code is voor stappen per 50 (dan ziet het er niet uit alsof hij rijdt)
        # if(action == "F"):
        #     if(self.current_position_enemy[1] + 50 <= self.max_position_x):
        #         self.current_position_enemy[1] += 50
        #     else:
        #         #opmerking moet ik hier ook iets doen zodat de reward naar 0 Gaat ofzo en hij dus niet achteruit zal gaan??
        #         pass
        #
        # elif(action == "B"):
        #     if(self.current_position_enemy[1] - 50 <= self.min_position_x):
        #         self.current_position_enemy[1] -=50
        #     else:
        #         pass
        #
        # elif(action == "R"):
        #     if(self.current_position_enemy[0] +50 <= self.max_position_y):
        #         self.current_position_enemy[0] +=50
        #     else:
        #         pass
        #
        # elif(action == "L"):
        #     if(self.current_position_enemy[0] - 50 <= self.min_position_y):
        #         self.current_position_enemy[0] -= 50
        #
        #
        # elif(action =="S"):
        #     self.current_position_friendly = self.current_position_friendly
        #     self.current_position_enemy = self.current_position_enemy

        # opmerking: nog eens checken of mijn checks juist zijn (hij mag niet uit het environment rijden, heb het gevoel van niet)


        # opmerking: nog eens checken of mijn checks juist zijn (hij mag niet uit het environment rijden, heb het gevoel van niet)
        # opmerking: moet ik hier ook checken of de positie van de roomba_enemy dezelfde is als die van de gewone?
        #komt dit in mijn else?


        #opmerking: er zijn twee manieren om het spel te doen stoppen.
        #1) de friendly roomba heeft een y_positie van 600
        #2) de enemy roomba heeft de zelfde positie als de friendly. In feite niet echt dezelfde, iets alsin zijn x, y + radius + 1/0.1  doen (dan reedt hij er net tegen)



        if (action == "F"):
            if (self.current_position_enemy[1] + 50 <= self.max_position_y):
                index = 0
                while index < 50:
                    self.current_position_enemy[1] +=1
                    self.render(mode="human")
                    index +=1

            else:
                # opmerking moet ik hier ook iets doen zodat de reward naar 0 Gaat ofzo en hij dus niet achteruit zal gaan??
                pass

        elif (action == "B"):
            if (self.current_position_enemy[1] - 50 >= self.min_position_y):

                index = 0
                while index < 50:
                    self.current_position_enemy[1] -= 1
                    self.render(mode="human")
                    index += 1
            else:
                pass

        elif (action == "R"):
            if (self.current_position_enemy[0] + 50 <= self.max_position_x):

                index = 0
                while index < 50:
                    self.current_position_enemy[0] += 1
                    self.render(mode="human")
                    index += 1
            else:
                pass

        elif (action == "L"):
            if (self.current_position_enemy[0] - 50 >= self.min_position_x):

                index = 0
                while index < 50:
                    self.current_position_enemy[0] -= 1
                    self.render(mode="human")
                    index += 1
            else:
                pass


        elif (action == "S"):
            self.current_position_friendly = self.current_position_friendly
            self.current_position_enemy = self.current_position_enemy

        self.render(mode="human")

        return self.observation, self.reward, self.done, self.info



    def reset(self):

        self.current_position_enemy = [350, 350]
        self.current_position_friendly = [350, 100]

        self.done = False


    def render(self, mode='human'):
        screen_width = 700
        screen_height = 700


        if self.viewer is None:
            from gym.envs.classic_control import rendering
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




        self.roombatrans_enemy.set_translation(self.current_position_enemy[0], self.current_position_enemy[1])
        self.roombatrans_friendly.set_translation(self.current_position_friendly[0], self.current_position_friendly[1])



        return self.viewer.render(return_rgb_array=mode == 'rgb_array')


    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None