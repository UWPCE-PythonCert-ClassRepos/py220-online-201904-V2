import sys
import pygame


def check_events(screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event)


def check_keydown_event(event):
    """ Check event when keydown is detected """
    if event.key == pygame.K_q:
        sys.exit()
