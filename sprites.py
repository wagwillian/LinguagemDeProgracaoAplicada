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
        self.collide_stairs()

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

    def collide_stairs(self):

        if pygame.sprite.spritecollide(self, self.game.stairs, False):
            self.game.playing = False
            self.game.continues_screen()

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
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def update(self):

        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        right_animation = [self.game.attack_spritesheet.get_sprite(265, 170, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(330, 170, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(265, 170, 60, self.height)]

        left_animation = [self.game.attack_spritesheet.get_sprite(290, 120, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(345, 120, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(395, 120, 60, self.height)]

        up_animation = [self.game.attack_spritesheet.get_sprite(205, 75, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(255, 75, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(300, 75, self.width, self.height)]


        down_animation = [self.game.attack_spritesheet.get_sprite(205, 20, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(255, 20, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(300, 15, self.width, self.height)]

        if direction == 'up':
            self.image = up_animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:

                self.game.attack_sound.play()
                Projectile(
                    self.game,
                    self.rect.centerx,
                    self.rect.centery,
                    self.game.player.facing
                )
                self.kill()
        if direction == 'down':
            self.image = down_animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.game.attack_sound.play()
                Projectile(
                    self.game,
                    self.rect.centerx,
                    self.rect.centery,
                    self.game.player.facing
                )
                self.kill()
        if direction == 'left':
            self.image = left_animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.game.attack_sound.play()
                Projectile(
                    self.game,
                    self.rect.centerx,
                    self.rect.centery,
                    self.game.player.facing
                )
                self.kill()
        if direction == 'right':
            self.image = right_animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                self.game.attack_sound.play()
                Projectile(
                    self.game,
                    self.rect.centerx,
                    self.rect.centery,
                    self.game.player.facing
                )
                self.kill()

class Projectile(pygame.sprite.Sprite):

    SPEED = 5

    def __init__(self, game, x, y, direction):


        self.game = game
        self._layer = PLAYER_LAYER
        self.direction = direction

        self.groups = self.game.all_sprites, self.game.projectiles
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Animation
        self.frames = self.game.projectile_frames
        print(self.frames[0].get_size())
        self.animation_index = 0
        self.animation_speed = 0.25

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        # Movement
        self.dx = 0
        self.dy = 0

        if direction == "up":
            self.dy = -self.SPEED

        elif direction == "down":
            self.dy = self.SPEED

        elif direction == "left":
            self.dx = -self.SPEED

        elif direction == "right":
            self.dx = self.SPEED

    def update(self):

        self.animate()



        self.rect.x += self.dx
        self.rect.y += self.dy

        hits = pygame.sprite.spritecollide(self, self.game.doors, True)

        if hits:
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.enemies, True):
            self.kill()

        if pygame.sprite.spritecollide(self, self.game.blocks, False):
            self.kill()


    def animate(self):

        self.image = self.frames[int(self.animation_index)]

        self.animation_index += self.animation_speed

        if self.animation_index >= len(self.frames):
            self.animation_index = 0



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
        self.groups = (
            self.game.all_sprites,
            self.game.doors,
            self.game.blocks,  # <-- add this
        )
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(224, 354, TILESIZE *2, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Stair(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER + 1

        self.groups = self.game.all_sprites, self.game.stairs
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(
            225,        # sprite x
            415,        # sprite y
            TILESIZE,   # width
            TILESIZE    # height
        )

        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
