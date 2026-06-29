import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)

        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER

        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1

        self.image = self.game.character_spritesheet.get_sprite(10,12 ,self.height,self.width)
        self.image.set_colorkey(BLACK)

        self.rect=self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'

        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change +=  PLAYER_SPEED
            self.facing = 'down'

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

        if hits:
            self.kill()
            self.game.playing = False

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.x - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.x + self.rect.width
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:

                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        down_animation = [self.game.character_spritesheet.get_sprite(10, 10, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(60, 15, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(105, 15, self.width, self.height),
                                self.game.character_spritesheet.get_sprite(155, 15, self.width, self.height)]

        up_animation = [self.game.character_spritesheet.get_sprite(10, 75, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(60, 75, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(109, 75, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(155, 75, self.width, self.height)]

        left_animation = [self.game.character_spritesheet.get_sprite(35, 120, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(100, 120, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(162, 120, self.width, self.height),
                              self.game.character_spritesheet.get_sprite(225, 120, self.width, self.height)]

        right_animation = [self.game.character_spritesheet.get_sprite(5, 170, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(68, 170, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(130, 170, self.width, self.height),
                               self.game.character_spritesheet.get_sprite(195, 170, self.width, self.height),]

        if self.facing == 'down':
            if self.y_change == 0:
                    self.image = self.game.character_spritesheet.get_sprite(10,15,self.width,self.height)
            else:
                self.image = down_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(10, 75, self.width, self.height)
            else:
                self.image = up_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(35, 120, self.width, self.height)
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(5, 170, self.width, self.height)
            else:
                self.image = right_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMIES_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right"])

        self.animation_loop = 0
        self.animation_speed = 0.15

        self.movement_loop = 0
        self.max_travel = random.randint(40, 100)

        # ---------- Load animations once ----------
        frame_positions = [5, 35, 70, 100, 130, 160, 190, 220, 250]

        self.right_animation = []

        for x_pos in frame_positions:
            frame = self.game.enemy_spritesheet.get_sprite(
                x_pos, 10, TILESIZE, TILESIZE
            )
            frame = pygame.transform.scale(
                frame,
                (ENEMY_SIZE, ENEMY_SIZE)
            )
            self.right_animation.append(frame)

        self.left_animation = [
            pygame.transform.flip(frame, True, False)
            for frame in self.right_animation
        ]

        self.image = self.right_animation[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):

        if self.facing == "right":
            self.x_change = ENEMY_SPEED
            self.movement_loop += ENEMY_SPEED

            if self.movement_loop >= self.max_travel:
                self.facing = "left"

        elif self.facing == "left":
            self.x_change = -ENEMY_SPEED
            self.movement_loop -= ENEMY_SPEED

            if self.movement_loop <= -self.max_travel:
                self.facing = "right"

    def animate(self):

        if self.facing == "right":
            self.image = self.right_animation[int(self.animation_loop)]

        else:
            self.image = self.left_animation[int(self.animation_loop)]

        self.animation_loop += self.animation_speed

        if self.animation_loop >= len(self.right_animation):
            self.animation_loop = 0

class TopBlock(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(32, 192, TILESIZE, TILESIZE)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(192, 224, TILESIZE, TILESIZE *2)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = DOOR_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(224, 354, TILESIZE *2, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
