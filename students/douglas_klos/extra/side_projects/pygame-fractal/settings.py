class Settings():
    def __init__(self):


        self.SCREEN_WIDTH = 1400
        self.SCREEN_HEIGHT = 1400

        self.WIDTH = 1000
        self.HEIGHT = 1000

        # Plot window
        self.RE_START = -2
        self.RE_END = 1
        self.IM_START = -1
        self.IM_END = 1

        self.MAX_ITER = 256


        # Interesting Julia Values
        julia_values = ((.4, .3), (.3, .2), (.35, .4))
        self.C_1 = julia_values[2][0]
        self.C_2 = julia_values[2][1]

        