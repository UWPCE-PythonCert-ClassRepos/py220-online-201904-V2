#!/usr/bin/env python3
import pygame
import colorsys
import pygame_functions as pf
# from random import random
import random


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800         

# Image size (pixels)
WIDTH = 1200
HEIGHT = 800

# Plot window
RE_START = -2
RE_END = 1
IM_START = -1
IM_END = 1

MAX_ITER = 256


def run_game():
    fractal_list = [calculate_mandelbrot, calculate_julia]
    current_fractal = 0
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Fractals")

    calculate_julia(screen)
    # calculate_mandelbrot(screen)
    update_screen()

    while True:
        pf.check_events(screen)


def update_screen():
    pygame.display.flip()


# Calculate the mandelbrot sequence for the point c with start value z
def mandelbrot(c, z=0):
    n = 0
    for n in range(MAX_ITER):
        z = z * z + c
        if abs(z) > 2: return n
    return MAX_ITER


def calculate_mandelbrot(screen):
    # Draw our image

    palette = colorize()

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                        IM_START + (y / HEIGHT) * (IM_END - IM_START))

            m = mandelbrot(c)

            if m == MAX_ITER:
                m = 0

            pygame.draw.circle(screen, palette[m], (x, y), 1)


def calculate_julia(screen):
    SCALE = 1.3
    CENTER = (.5, 1.5)
    C_1 = .4
    C_2 = .3

    palette = colorize()

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            c = complex((RE_START + (x / WIDTH) * (RE_END - RE_START)) * SCALE + CENTER[0],
                        (IM_START + (y / HEIGHT) * (IM_END - IM_START))* SCALE)
            m = mandelbrot(complex(C_1, C_2), c)  # Julia
            pygame.draw.circle(screen, palette[m], (x, y), 1)


def colorize():
    # Calculate a tolerable palette
    colors_max = 256
    palette = [0] * colors_max

    for i in range(colors_max):
        f = 1 - abs((float(i) / colors_max - 1) ** 16)
        r, g, b = colorsys.hsv_to_rgb(0.36 + f / 3, 1 - f, f)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


if __name__ == "__main__":
    run_game()
