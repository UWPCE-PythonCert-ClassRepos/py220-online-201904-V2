import sys
import pygame
import src.functions as func


def check_events(screen, settings, palette):

    start_pos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            settings._mouse_down = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            settings._mouse_up = pygame.mouse.get_pos()
            check_mouse_up_event(screen, settings, palette)
            # print(Settings.mouse_up[0] - Settings.mouse_down[0])


def check_mouse_up_event(screen, settings, palette):
    mouse_horz = abs(settings._mouse_down[0] - settings._mouse_up[0])
    mouse_vert = abs(settings._mouse_down[1] - settings._mouse_up[1])



    if (settings._mouse_down[0] < settings._mouse_up[0]):

        print(settings._mouse_down)
        print(settings._mouse_up)
        settings._mouse_up = (settings._mouse_up[0], settings._mouse_down[1] + (settings._mouse_up[0] - settings._mouse_down[0]))
        print(settings._mouse_down)
        print(settings._mouse_up)
        # settings._mouse_up[1] = settings._mouse_down[1] + (settings._mouse_up[0] - settings._mouse_down[0])

        start_percent_re = (settings._mouse_down[0] / settings.SCREEN_WIDTH)
        end_percent_re = (settings._mouse_up[0] / settings.SCREEN_WIDTH)
        start_percent_im = (settings._mouse_down[1] / settings.SCREEN_HEIGHT)
        end_percent_im = (settings._mouse_up[1] / settings.SCREEN_HEIGHT)

        new_start_re = settings.RE_START + abs((start_percent_re * abs((settings.RE_START - settings.RE_END))))
        new_end_re = new_start_re + abs((end_percent_re - start_percent_re)) * abs((settings.RE_START - settings.RE_END))

        new_start_im = settings.IM_START + abs((start_percent_im * abs((settings.IM_START - settings.IM_END))))
        new_end_im = new_start_im + abs((end_percent_im - start_percent_im)) * abs((settings.IM_START - settings.IM_END))


        print(f"start_percent_re:{start_percent_re}")
        print(f"end_percent_re:{end_percent_re}")
        print()
        print(f"old_start_re:{settings.RE_START}")
        print(f"new_start_re:{new_start_re}")
        print(f"old_end_re:{settings.RE_END}")
        print(f"new_end_re:{new_end_re}")
        print()
        print(f"old_start_im:{settings.IM_START}")
        print(f"new_start_im:{new_start_im}")
        print(f"old_end_im:{settings.IM_END}")
        print(f"new_end_im:{new_end_im}")
        print()

        settings.RE_START = new_start_re
        settings.RE_END = new_end_re

        settings.IM_START = new_start_im
        settings.IM_END = new_end_im

        point_list = func.fractal_list[settings.current_fractal](settings)

        for point in point_list:
            screen.set_at((point[0], point[1]), palette[point[2]])

        pygame.display.flip()


def check_keydown_event(event):
    """ Check event when keydown is detected """
    if event.key == pygame.K_q:
        sys.exit()

    # if event.key == pygame.K_m:
    #     calculate_mandelbrot()
    #     display_fractal(screen, point_list)
    #     update_screen()
