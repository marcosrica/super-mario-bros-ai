class Animation:
    def __init__(self, images, idle_sprite=None, air_sprite=None, delta_time=7):
        self.images = images
        self.timer = 0
        self.index = 0
        self.image = self.images[self.index]
        self.idle_sprite = idle_sprite
        self.air_sprite = air_sprite
        self.delta_time = delta_time

    def update(self):
        self.timer += 1
        if self.timer % self.delta_time == 0:
            if self.index < len(self.images) - 1:
                self.index += 1
            else:
                self.index = 0
        self.image = self.images[self.index]

    def idle(self):
        self.image = self.idle_sprite

    def inAir(self):
        self.image = self.air_sprite
