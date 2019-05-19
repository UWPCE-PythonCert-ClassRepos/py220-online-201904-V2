#!/usr/bin/env python3
import pygame
import colorsys


def update_screen():
    pygame.display.flip()


def run_game():

    pygame.init()
    screen = pygame.display.set_mode((2000, 2000))
    pygame.display.set_caption("Draw stuff")

    #for point_x in range(100):
    #    pygame.draw.circle(screen, 200, (point_x * 10, point_x ** 2), 10, 2)
    fractal1(screen)
    update_screen()


# Calculate the mandelbrot sequence for the point c with start value z
def iterate_mandelbrot(c, z=0):
    iterate_max = 1000
    for n in range(iterate_max + 1):
        z = z * z + c
        if abs(z) > 2:
            return n
    return None


def fractal1(screen):
    dimensions = (2000, 2000)
    scale = 1.0 / (dimensions[0] / 3)
    center = (1.5, 1.5)  # Use this for Mandelbrot set
    # center = (1.5, 1.5)       # Use this for Julia set
    # center = (1.0, 1.0)
    colors_max = 5000


    # Calculate a tolerable palette
    palette = [0] * colors_max
    for i in range(colors_max):

        f = 1 - abs((float(i) / colors_max - 1) ** 15)
        r, g, b = colorsys.hsv_to_rgb(0.66 + f / 3, 1 - f / 2, f)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))


    # Draw our image
    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            c = complex(x * scale - center[0], y * scale - center[1])

            # n = iterate_mandelbrot(c)  # Use this for Mandelbrot set
            n = iterate_mandelbrot(complex(0.43, 0.6), c)  # Use this for Julia set

            if n is None:
                v = 1
            else:
                v = n / 100.0

            #print(f"x:{x}, y:{y}")
            pygame.draw.circle(screen, palette[int(v * (colors_max - 1))], (x, y), 1)
            # d.point((x, y), fill = palette[int(v * (colors_max-1))])









if __name__ == "__main__":
    run_game()
    while True:
        update_screen()
