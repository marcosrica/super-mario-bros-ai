import pygame
from classes.Font import Font

class Dashboard(Font):
    def __init__(self, file_path, size, screen, draw):
        Font.__init__(self, file_path, size)
        self.state = "menu"
        self.screen = screen
        self.level_name = ""
        self.ticks = 0
        self.time = 0
        self.to_draw = draw

    def update(self, draw:bool, coins, points, time):
        if draw:
            self.draw_text("MARIO", 50, 20, 15)
            self.draw_text(self.point_string(points), 50, 37, 15)
            
            self.draw_text(f"@x{self.coin_string(coins)}", 225, 37, 15)
        
            self.draw_text("WORLD", 380, 20, 15)
            self.draw_text(str(self.level_name), 395, 37, 15)

        self.ticks += 1
        if(self.ticks == 60):
            self.ticks = 0
            self.time += 1

    def draw_text(self, text, x, y, size):
        if not self.to_draw:
            return
        
        for char in text:
            charSprite = pygame.transform.scale(self.char_sprites[char], (size, size))
            self.screen.blit(charSprite, (x, y))

            if char == " ":
                x += size // 2
            else:
                x += size

    def coin_string(self, coins):
        if not self.to_draw:
            return
        return "{:02d}".format(coins)

    def point_string(self, points):
        if not self.to_draw:
            return
        return "{:06d}".format(points)

    def time_string(self):
        if not self.to_draw:
            return
        return "{:03d}".format(self.time)