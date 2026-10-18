class JumpTrait:
    def __init__(self, entity):
        self.verticalSpeed = -12
        self.jumpHeight = 120
        self.entity = entity
        self.initalHeight = 384
        self.deaccelerationHeight = self.jumpHeight - ((self.verticalSpeed*self.verticalSpeed)/(2*self.entity.gravity))

    def jump(self, jumping):
        if jumping:
            if self.entity.on_ground:
                self.entity.vel.y = self.verticalSpeed
                self.entity.inAir = True
                self.initalHeight = self.entity.rect.y
                self.entity.in_jump = True
                self.entity.obeyGravity = False  # always reach maximum height

        if self.entity.in_jump:
            if (self.initalHeight-self.entity.rect.y) >= self.deaccelerationHeight or self.entity.vel.y == 0:
                self.entity.in_jump = False
                self.entity.obeyGravity = True

    def reset(self):
        self.entity.inAir = False

    def update(self, draw):
        pass
