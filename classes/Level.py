import json
from numpy import tile
import pygame

from Entities.EntityBase import EntityBase
from classes.Camera import Camera
from classes.Sprites import Sprites
from classes.Tile import Tile
from Entities.Coin import Coin
from Entities.CoinBrick import CoinBrick
from Entities.Goomba import Goomba
from Entities.Mushroom import RedMushroom
from Entities.Koopa import Koopa
from Entities.CoinBox import CoinBox
from Entities.RandomBox import RandomBox
from classes.Dashboard import Dashboard

class Level:
    def __init__(self, screen, dashboard, draw:bool):
        self.sprites = Sprites()
        self.dashboard = dashboard
        self.screen = screen
        self.level:list[list[Tile]] = []
        self.level_length = 0
        self.entity_list:list[EntityBase] = []

        self.points = 0
        self.coins = 0

        self.to_draw = draw

    def load_level(self, level_name):
        with open(f"./levels/{level_name}.json") as jsonData:
            data = json.load(jsonData)
            self.load_layers(data)
            self.load_objects(data)
            self.load_entities(data)
            self.level_length = data["length"]

    def set_dashboard(self, new_dashboard:Dashboard):
        self.dashboard = new_dashboard

    def load_entities(self, data):
        print(data)
        try:
            [self.add_coin_box(x, y) for x, y in data["level"]["entities"]["CoinBox"]]
            print("coin boxes added")
            [self.add_goomba(x, y) for x, y in data["level"]["entities"]["Goomba"]]
            print("goombas added")
            [self.add_koopa(x, y) for x, y in data["level"]["entities"]["Koopa"]]
            print("koopas added")
            [self.add_coin(x, y) for x, y in data["level"]["entities"]["coin"]]
            print("coins added")
            [self.add_coin_brick(x, y) for x, y in data["level"]["entities"]["coinBrick"]]
            print("coin bricks added")
            [self.add_random_box(x, y, item) for x, y, item in data["level"]["entities"]["RandomBox"]]
            print("random boxes added")
        except Exception:
            print("except called")
            # if no entities in Level

    def load_layers(self, data):
            layers = []
            for x in range(*data["level"]["layers"]["sky"]["x"]):
                layers.append(
                    [
                        Tile(self.sprites.spriteCollection.get("sky"), None)
                        for y in range(*data["level"]["layers"]["sky"]["y"])
                    ]
                    + 
                    [
                        Tile(
                            self.sprites.spriteCollection.get("ground"),
                            pygame.Rect(x * 32, (y - 1) * 32, 32, 32),
                        )
                        for y in range(*data["level"]["layers"]["ground"]["y"])
                    ]
                )
            self.level = list(map(list, zip(*layers)))

    def load_objects(self, data):
            for x, y in data["level"]["objects"]["bush"]:
                self.add_bush_sprite(x, y)
            for x, y in data["level"]["objects"]["cloud"]:
                self.add_cloud_sprite(x, y)
            for x, y, z in data["level"]["objects"]["pipe"]:
                self.add_pipe_sprite(x, y, z)
            for x, y in data["level"]["objects"]["sky"]:
                self.level[y][x] = Tile(self.sprites.spriteCollection.get("sky"), None)
            for x, y in data["level"]["objects"]["ground"]:
                self.level[y][x] = Tile(
                    self.sprites.spriteCollection.get("ground"),
                    pygame.Rect(x * 32, y * 32, 32, 32),
                )

    def update_entities(self, draw:bool, camera: Camera):
        for entity in list(self.entity_list):   # iterate over a copy
            entity.update(draw, camera)
        self.entity_list = [e for e in self.entity_list if e.alive is not None]

    def update(self, visual, camera:Camera):
        if visual:
            self.draw_level(camera)

        self.update_entities(visual, camera)
        

    def draw_level(self, camera:Camera):
        try:
            for y in range(0, 15):
                for x in range(0-int(camera.pos.x + 1), 20-int(camera.pos.x-1)):
                    if self.level[y][x].sprite is not None:
                        if self.level[y][x].sprite.redraw_background:
                            self.screen.blit(
                                self.sprites.spriteCollection.get("sky").image,
                                ((x + camera.pos.x) * 32, y*32)
                            )

                        self.level[y][x].sprite.drawSprite(
                            x + camera.pos.x, y, self.screen
                        )
        except IndexError:
            return
        
    def add_cloud_sprite(self, x, y):
        try:
            for y_off in range(0, 2):
                for x_off in range(0, 3):
                    self.level[y + y_off][x + x_off] = Tile(
                        self.sprites.spriteCollection.get(f"cloud{y_off+1}_{x_off+1}"), None,
                    )
        except IndexError:
            return

    def add_pipe_sprite(self, x, y, length=2):
        try:
            # add the pipe's head
            self.level[y][x] = Tile(
                self.sprites.spriteCollection.get("pipeL"),
                pygame.Rect(x*32, y*32, 32, 32)
            )
            self.level[y][x+1] = Tile(
                self.sprites.spriteCollection.get("pipeR"),
                pygame.Rect((x+1)*32, y*32, 32, 32)
            )

            # add the pipe's body
            for i in range(1, length + 20):
                self.level[y+i][x] = Tile(
                    self.sprites.spriteCollection.get("pipe2L"),
                    pygame.Rect(x*32, (y+i)*32, 32, 32)
                )
                self.level[y+i][x+1] = Tile(
                    self.sprites.spriteCollection.get("pipe2R"),
                    pygame.Rect((x+1)*32, (y+i)*32, 32, 32)
                )
        except IndexError:
            return

    def add_bush_sprite(self, x, y):
        try:
            self.level[y][x] = Tile(self.sprites.spriteCollection.get("bush_1"), None)
            self.level[y][x+1] = Tile(self.sprites.spriteCollection.get("bush_2"), None)
            self.level[y][x+2] = Tile(self.sprites.spriteCollection.get("bush_3"), None)
        except IndexError:
            return

    def add_coin_box(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x*32, y*32-1, 32, 32))
        self.entity_list.append(
            CoinBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.dashboard,
                self.to_draw
            )
        )

    def add_random_box(self, x, y, item):
        self.level[y][x] = Tile(None, pygame.Rect(x*32, y*32-1, 32, 32))
        self.entity_list.append(
            RandomBox(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                item,
                self.dashboard,
                self
            )
        )

    def add_coin_brick(self, x, y):
        self.level[y][x] = Tile(None, pygame.Rect(x*32, y*32-1, 32, 32))
        self.entity_list.append(
            CoinBrick(
                self.screen,
                self.sprites.spriteCollection,
                x,
                y,
                self.dashboard,
                self.to_draw
            )
        )

    def add_coin(self, x, y):
        self.entity_list.append(Coin(self.screen, self.sprites.spriteCollection, x, y))

    def add_goomba(self, x, y):
        print("adding goomba on ", x, ", ", y)
        self.entity_list.append(
            Goomba(self.screen, self.sprites.spriteCollection, x, y, self)
        )

    def add_koopa(self, x, y):
        self.entity_list.append(
            Koopa(self.screen, self.sprites.spriteCollection, x, y, self)
        )

    def add_red_mushroom(self, x, y):
        self.entity_list.append(
            RedMushroom(self.screen, self.sprites.spriteCollection, x, y, self)
        )

        