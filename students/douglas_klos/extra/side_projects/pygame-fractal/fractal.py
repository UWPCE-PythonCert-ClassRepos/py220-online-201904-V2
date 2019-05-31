#!/usr/bin/env python3
from pygame import display, init
from src.settings import Settings as Settings
import src.functions as func
import src.pygame_functions as pf


def main():

    settings = Settings()
    

    point_list = func.fractal_list[settings.current_fractal](settings)
    # palette = func.linear_colorize(settings)
    palette = func.colorize(settings)

    init() #pygame
    screen = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    display.set_caption(f"Fractals")
    
    func.display_fractal(palette, screen, point_list)
    func.update_screen()

    while True:
        pf.check_events(screen, settings, palette)


if __name__ == "__main__":
    main()
