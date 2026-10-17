import random

import pygame
from classes.Dashboard import Dashboard
from classes.Level import Level
from Entities.Mario import Mario


windowSize = 640, 480


def main():
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(windowSize)
    max_frame_rate = 60
    dashboard = Dashboard("./img/font.png", 8, screen)
    level = Level(screen, dashboard)
    level.load_level("level1-1")

    #while not menu.start:
    #    menu.update()

    mario1 = Mario(0, 0, level, screen, dashboard)
    clock = pygame.time.Clock()
    options = [0, 1, 2, 3, 4]

    while not mario1.restart:
        #pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
        
        mario1.move(random.choice(options))
        level.draw_level(mario1.camera)
        dashboard.update(level.coins, level.points, 100)
        mario1.update()
        pygame.display.update()
        clock.tick(max_frame_rate)
    return 'restart'


if __name__ == "__main__":
    exitmessage = 'restart'
    while exitmessage == 'restart':
        exitmessage = main()