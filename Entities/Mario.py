import pygame

from Entities.EntityBase import EntityBase
from Entities.Item import Item
from Entities.Koopa import Koopa
from Entities.Mushroom import RedMushroom
from classes.Animation import Animation
from classes.Camera import Camera
from classes.Collider import Collider
from classes.Dashboard import Dashboard
from classes.EntityCollider import CollisionState, EntityCollider
from classes.Level import Level
from classes.Sprites import Sprites
from traits.Bounce import bounceTrait
from traits.Go import GoTrait
from traits.Jump import JumpTrait

sprite_collection = Sprites().spriteCollection
small_animation = Animation(
    [
        sprite_collection["mario_run1"].image,
        sprite_collection["mario_run2"].image,
        sprite_collection["mario_run3"].image,
    ],
    sprite_collection["mario_idle"].image,
    sprite_collection["mario_jump"].image,
)
big_animation = Animation(
    [
        sprite_collection["mario_big_run1"].image,
        sprite_collection["mario_big_run2"].image,
        sprite_collection["mario_big_run3"].image,
    ],
    sprite_collection["mario_big_idle"].image,
    sprite_collection["mario_big_jump"].image,
)

class Mario(EntityBase):
    def __init__(self, x, y, level:Level, screen, dashboard:Dashboard, gravity=0.8):
        super().__init__(x, y, gravity)
        self.camera:Camera = Camera(self.rect, self)
        self.in_air = False
        self.in_jump = False
        self.power_up_state = 0
        self.invincibility_frames = 0
        self.traits = {
            "jumpTrait": JumpTrait(self),
            "goTrait": GoTrait(small_animation, screen, self.camera, self),
            "bounceTrait": bounceTrait(self)
        }

        self.level_obj:Level = level
        self.collision:Collider = Collider(self, level)
        self.screen = screen
        self.entity_collider:EntityCollider = EntityCollider(self)
        self.dashboard:Dashboard = dashboard
        self.restart = False

    def update(self):
        if self.invincibility_frames > 0:
            self.invincibility_frames -= 1

        self.update_traits()
        self.move_mario()
        self.camera.move()
        self.apply_gravity()
        self.check_entity_collision()

    def move(self, key):
        if key == 0:
            self.traits["goTrait"].direction = 0 #do nothing
        elif key == 1:
            self.traits["goTrait"].direction = -1 #go left
        elif key == 2:
            self.traits["goTrait"].direction = 1 #go right
        elif key == 3:
            self.traits['jumpTrait'].jump(True) # jump
        elif key == 4:
            self.traits['jumpTrait'].jump(False) #not jump

    def move_mario(self):
        self.rect.y += self.vel.y
        self.collision.check_y()
        self.rect.x += self.vel.x
        self.collision.check_x()

    def check_entity_collision(self):
        for entity in self.level_obj.entity_list:
            collision_state = self.entity_collider.check(entity)
            if collision_state.is_colliding:
                if entity.type == "Item":
                    self.on_collision_with_item(entity)
                elif entity.type == "Block":
                    self.on_collision_with_block(entity)
                elif entity.type == "Mob":
                    self.on_collision_with_mob(entity, collision_state)

    def on_collision_with_item(self, item:EntityBase):
        self.level_obj.entity_list.remove(item)
        self.level_obj.points += 100
        self.level_obj.coins += 1

    def on_collision_with_block(self, block:EntityBase):
        if not block.triggered:
            self.level_obj.coins += 1
        block.triggered = True
        
    def on_collision_with_mob(self, mob, collision_state:CollisionState):
        if isinstance(mob, RedMushroom) and mob.alive:
            self.power_up(1)
            self.kill_entity(mob)
        elif collision_state.is_top and (mob.alive or mob.bouncing):
            self.rect.bottom = mob.rect.top
            self.bounce()
            self.kill_entity(mob)
        elif collision_state.is_colliding and mob.alive and not mob.active and not mob.bouncing:
            mob.bouncing = True
            if mob.rect.x < self.rect.x:
                mob.left_right_trait.direction -= 1
                mob.rect.x += -5
            else:
                mob.rect.x += 5
                mob.left_right_trait.direction = 1
        elif collision_state.is_colliding and mob.alive and not self.invincibility_frames:
            if self.power_up_state == 0:
                self.game_over()
            elif self.power_up_state == 1:
                self.power_up_state = 0
                self.traits['goTrait'].updateAnimation(small_animation)
                x, y = self.rect.x, self.rect.y
                self.rect = pygame.Rect(x, y+32, 32, 32)
                self.invincibility_frames = 60              

    def kill_entity(self, entity:EntityBase):
        if entity.__class__.__name__ != "koopa":
            entity.alive = False
        else:
            entity.timer = 0
            entity.left_right_trait.speed = 1
            entity.alive = True
            entity.active = False
            entity.bouncing = False

        self.level_obj.points += 100

    def game_over(self):
        srf = pygame.Surface((640, 480))
        srf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        srf.set_alpha(128)
        self.restart = True

    def bounce(self):
        self.traits["bounceTrait"].jump = True

    def power_up(self, powerup_id):
        if self.power_up_state == 0 and powerup_id == 1:
            self.power_up_state = 1
            self.traits['goTrait'].updateAnimation(big_animation)
            self.rect = pygame.Rect(self.rect.x, self.rect.y-32, 32, 64)
            self.invincibility_frames = 20

    def get_pos(self):
        return self.camera.x + self.rect.y + self.rect.y

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y