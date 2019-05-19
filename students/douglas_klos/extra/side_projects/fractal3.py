#!/usr/bin/env python3
import colorsys
from PIL import Image, ImageDraw
from kivy.graphics import *
from kivy.app import App

class FractalKivy(App):
    def build(self):
        self.box = BoxLayout(orientation='horizontal', spacing=20)

with self.canvas:
    # Add a red color
    Color(1., 0, 0)

    # Add a rectangle
    Rectangle(pos=(10, 10), size=(500, 500))


# Calculate the mandelbrot sequence for the point c with start value z
def iterate_mandelbrot(c, z=0):
    for n in range(iterate_max + 1):
        z = z * z + c
        if abs(z) > 2:
            return n
    return None



def fractal1():
    dimensions = (800, 800)
    scale = 1.0 / (dimensions[0] / 3)
    center = (2.2, 1.5)  # Use this for Mandelbrot set
    # center = (1.5, 1.5)       # Use this for Julia set
    iterate_max = 100
    colors_max = 50

    img = Image.new("RGB", dimensions)
    d = ImageDraw.Draw(img)

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

            n = iterate_mandelbrot(c)  # Use this for Mandelbrot set
            # n = iterate_mandelbrot(complex(0.3, 0.6), c)  # Use this for Julia set

            if n is None:
                v = 1
            else:
                v = n / 100.0

            d.point((x, y), fill = palette[int(v * (colors_max-1))])

    del d
    img.save("result.png")


if __name__ == "__main__":
    #fractal1()
    FractalKivy().run()
