class Settings():
    def __init__(self):

        self.current_fractal = 'mandelbrot'

        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 1000

        self.WIDTH = 1000
        self.HEIGHT = 1000

        self.MAX_ITER = 512
        self.BLACK_CENTER = True
        self.COLOR_DEPTH = 64

        # Default, FUll plot window
        self.RE_START = -2
        self.RE_END = 1
        self.IM_START = -1
        self.IM_END = 1

        # Interesting Julia Values
        julia_values = ((.4, .3), (.3, .2), (.35, .4))
        self.C_1 = julia_values[2][0]
        self.C_2 = julia_values[2][1]

        self._mouse_down = None
        self._mouse_up = None
