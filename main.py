from turtledemo.sorting_animate import Block

import pygame
from pygame.examples.aliens import Player

from sprites import *
from config import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet("img/character_sheet.png")
        self.terrain_spritesheet = Spritesheet("img/Dungeon_Tileset_at.png")

    def createTilemap(self):
        for i, row in enumerate(tilemap):

            print(i, row)
            for j, column in enumerate(row):
                Ground(self, j, i)

                if column == "B":

                    TopBlock(self, j, i)

                if column == "P":
                    Player(self, j, i)
                if column == "D":
                    Door(self, j, i)



    def new(self):
        # Inicializa o jogo

        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()


    def events(self):
        #game loop events - define os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        #atualiza os quadros
        self.all_sprites.update()

    def draw(self):
        #game loop draw - desenha os quadros
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop - define o loop principal
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass
g = Game()
g.intro_screen()
g.new()
image_to_load = pygame.image.load("img/single_char.png").convert_alpha()
print(image_to_load.get_size())
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()

