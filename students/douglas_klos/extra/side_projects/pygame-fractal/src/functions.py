from pygame import display
from colorsys import hsv_to_rgb
from collections import defaultdict
from src.settings import Settings
from datetime import datetime
from math import log, log2, floor, ceil


# def iterate_mandelbrot(BLACK_CENTER, MAX_ITER, c, z=0):
#     """ Calculate the mandelbrot sequence for the point c with start value z """
#     n = 0
#     for n in range(MAX_ITER):
#         z = z * z + c
#         if abs(z) > 2:
#             return n
#     if BLACK_CENTER:
#         return 0
#     else:
#         return MAX_ITER - 1


def iterate_mandelbrot(BLACK_CENTER, MAX_ITER, c, z=0):
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER - 1
    
    return n + 1 - log(log2(abs(z)))



def mandelbrot(settings):
    """ Mandelbrot sequence """
    SCALE = 1
    CENTER = (0, 0)
    start = datetime.now()
    point_list = []

    for x in range(0, settings.SCREEN_WIDTH):
        for y in range(0, settings.SCREEN_HEIGHT):
            c = complex(
                (settings.RE_START + (x / settings.WIDTH) * (settings.RE_END - settings.RE_START)) * SCALE + CENTER[0],
                (settings.IM_START + (y / settings.HEIGHT) * (settings.IM_END - settings.IM_START)) * SCALE + CENTER[1],
            )

            m = iterate_mandelbrot(settings.BLACK_CENTER, settings.MAX_ITER, c)
            point_list.append((x, y, m))
        print(f"Calculating Fractal: {((x / settings.SCREEN_WIDTH) * 100):0.2f} % complete  ", end='\r')
    print(f"time:{datetime.now()-start}")
    return point_list


def julia(settings):
    """ Julia sequence """
    SCALE = 1
    CENTER = (0, 0)

    point_list = []

    for x in range(0, settings.SCREEN_WIDTH):
        for y in range(0, settings.SCREEN_HEIGHT):
            c = complex(
                (settings.RE_START + (x / settings.WIDTH) * (settings.RE_END - settings.RE_START)) * SCALE + CENTER[0],
                (settings.IM_START + (y / settings.HEIGHT) * (settings.IM_END - settings.IM_START)) * SCALE + CENTER[1],
            )
            m = iterate_mandelbrot(settings.BLACK_CENTER, settings.MAX_ITER, complex(settings.C_1, settings.C_2), c)
            point_list.append((x, y, m))
        print(f"Calculating Fractal: {((x / settings.SCREEN_WIDTH) * 100):0.2f} % complete  ", end='\r')
    return point_list


def colorize(settings):
    """ Calculate color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        f = 1 - abs((float(i) / settings.MAX_ITER - 1) ** (settings.MAX_ITER/settings.COLOR_DEPTH))
        r, g, b = hsv_to_rgb(0.66 + f / 3, 1 - f, f if i < settings.MAX_ITER - 1 else 0)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def linear_colorize(settings):
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        r, g, b = hsv_to_rgb(i/settings.MAX_ITER, 1, 1 if i < settings.MAX_ITER - 1 else 0)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def display_fractal(palette, screen, point_list):
    """ Draw the fractal to the screen """
    for point in point_list:
        screen.set_at((point[0], point[1]), palette[floor(point[2])])


def update_screen():
    """ Update pygame display """
    display.flip()


fractal_list = {"mandelbrot": mandelbrot,
                "julia": julia}


# def min_max(point_list):
#     """ For checking rendered min max values, useless at the moment really """
#     min_x = 10 ** 10
#     min_y = 10 ** 10
#     min_m = 10 ** 10

#     max_x = -10 ** 10
#     max_y = -10 ** 10
#     max_m = -10 ** 10

#     for point in point_list:
#         if point[0] < min_x:
#             min_x = point[0]
#         if point[1] < min_y:
#             min_y = point[1]
#         if point[2] < min_m:
#             min_m = point[2]

#         if point[0] > max_x:
#             max_x = point[0]
#         if point[1] > max_y:
#             max_y = point[1]
#         if point[2] > max_m:
#             max_m = point[2]

#     print(min_x)
#     print(min_y)
#     print(min_m)
#     print(max_x)
#     print(max_y)
#     print(max_m)
