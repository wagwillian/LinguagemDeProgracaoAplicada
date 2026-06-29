from Button import *
from sprites import *
from config import *
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet("img/mage_sheet.png")
        self.terrain_spritesheet = Spritesheet("img/Dungeon_Tileset_at.png")
        self.enemy_spritesheet = Spritesheet("img/skeleton_movement.png")
        self.menu_background = pygame.image.load("img/title_screen.png").convert()

        # Ajusta a imagem para o tamanho da janela
        self.menu_background = pygame.transform.scale(
            self.menu_background,
            (WIN_WIDTH, WIN_HEIGHT)
        )

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
                if column == "E":
                    Enemy(self, j, i)



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

        title_font = pygame.font.Font("fonts/MedievalSharp-Regular.ttf", 64)
        subtitle_font = pygame.font.Font("fonts/MedievalSharp-Regular.ttf", 20)
        menu_font = pygame.font.Font("fonts/MedievalSharp-Regular.ttf", 28)

        iniciar = Button(220, 180, 200, 50, "Start Game", menu_font)
        instrucoes = Button(220, 245, 200, 50, "Instructions", menu_font)
        sobre = Button(220, 310, 200, 50, "About", menu_font)
        sair = Button(220, 375, 200, 50, "Exit", menu_font)

        while True:

            self.screen.blit(self.menu_background, (0, 0))

            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.set_alpha(110)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            title = "EPIC DUNGEON"

            shadow = title_font.render(title, True, (20, 20, 20))
            text = title_font.render(title, True, (255, 220, 80))

            rect = text.get_rect(center=(WIN_WIDTH // 2, 70))

            self.screen.blit(shadow, (rect.x + 4, rect.y + 4))
            self.screen.blit(text, rect)

            subtitle = subtitle_font.render(
                "Escape the Ancient Dungeon",
                True,
                (220, 220, 220)
            )

            self.screen.blit(
                subtitle,
                subtitle.get_rect(center=(WIN_WIDTH // 2, 120))
            )

            iniciar.draw(self.screen)
            instrucoes.draw(self.screen)
            sobre.draw(self.screen)
            sair.draw(self.screen)

            version = pygame.font.SysFont(None, 20).render(
                "Version 1.0",
                True,
                (170, 170, 170)
            )

            self.screen.blit(version, (10, 455))

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if iniciar.clicked(event):
                    return

                if instrucoes.clicked(event):
                    self.instructions_screen()

                if sobre.clicked(event):
                    self.about_screen()

                if sair.clicked(event):
                    pygame.quit()
                    sys.exit()

    def instructions_screen(self):

        title_font = pygame.font.Font("fonts/MedievalSharp-Regular.ttf", 42)
        menu_font = pygame.font.Font("fonts/MedievalSharp-Regular.ttf", 26)

        lines = [
            "Use the Arrow Keys to move.",
            "",
            "Avoid the skeletons.",
            "",
            "Find the exit door.",
            "",
            "Good luck, Wizard!",
            "",
            "Press ESC to return."
        ]

        while True:

            self.screen.fill((18, 18, 18))

            title = title_font.render("INSTRUCTIONS", True, (255, 215, 0))
            self.screen.blit(title, title.get_rect(center=(WIN_WIDTH // 2, 50)))

            y = 120

            for line in lines:
                text = menu_font.render(line, True, WHITE)
                self.screen.blit(text, text.get_rect(center=(WIN_WIDTH // 2, y)))
                y += 40

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return

    def about_screen(self):

        title_font = pygame.font.Font("fonts/MedievalSharp-Regular.ttf", 42)
        menu_font = pygame.font.Font("fonts/MedievalSharp-Regular.ttf", 24)

        lines = [

            "Dungeon Adventure",

            "",

            "Developed for",

            "Applied Programming",

            "",

            "Developer:",

            "Wagner W. Oliveira",

            "RU: 5297048",

            "",

            "Press ESC to return"

        ]

        while True:

            self.screen.fill((30, 20, 15))

            title = title_font.render("ABOUT", True, (255, 215, 0))
            self.screen.blit(title, title.get_rect(center=(WIN_WIDTH // 2, 50)))

            y = 120

            for line in lines:
                text = menu_font.render(line, True, WHITE)
                self.screen.blit(text, text.get_rect(center=(WIN_WIDTH // 2, y)))
                y += 35

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()

