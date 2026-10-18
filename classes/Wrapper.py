import pygame
from Entities.Mario import Mario
from classes.PlayerWrapper import PlayerWrapper
from classes.Dashboard import Dashboard
from classes.Level import Level

class Wrapper:
    def __init__(self, level_route, draw:bool, frame_rate):
        windowSize = 640, 480
        self.to_draw = draw
        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init()
        self.screen = pygame.display.set_mode(windowSize)
        self.max_frame_rate = 60
        self.dashboard = Dashboard("./img/font.png", 8, self.screen, draw)
        self.level = Level(self.screen, self.dashboard, draw)
        self.level.load_level(level_route)
        self.mario: Mario = Mario(0, 0, self.level, self.screen, self.dashboard)
        self.model:PlayerWrapper = PlayerWrapper()
        self.clock = pygame.time.Clock()

        self.max_pos = 0

    def get_max_mario_pos(self):
        return self.max_pos

    def get_state(self):
        return (self.mario, self.level)

    def set_model(self, model:PlayerWrapper):
        self.model = model        

    def simulate(self):
        self.max_pos = 0
        
        while not self.mario.restart and self.model.moves_left():
            #pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(clock.get_fps())))
            movement = self.model.make_move()
            self.mario.move(movement)
            self.level.update(self.to_draw, self.mario.camera)
            self.dashboard.update(self.to_draw, self.level.coins, self.level.points, 100)
            self.mario.update(self.to_draw)
            print("Mario is on position: ", self.mario.get_pos())
            pygame.display.update()
            self.clock.tick(self.max_frame_rate)

            if self.mario.get_pos()[0] > self.max_pos:
                self.max_pos = self.mario.get_pos()[0]

        return self.mario.restart
        