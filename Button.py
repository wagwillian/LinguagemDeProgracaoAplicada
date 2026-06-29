import pygame
from config import *

class Button:

    def __init__(self, x, y, width, height, text, font):

        self.rect = pygame.Rect(x, y, width, height)

        self.text = text
        self.font = font

        self.normal_color = (55, 55, 60)
        self.hover_color = (85, 85, 95)

        self.border_color = (180, 150, 40)
        self.hover_border = (255, 215, 80)

        self.text_color = (240, 240, 230)

    def draw(self, screen):

        mouse = pygame.mouse.get_pos()

        hover = self.rect.collidepoint(mouse)

        if hover:

            button = self.rect.inflate(8, 8)

            fill = self.hover_color
            border = self.hover_border

        else:

            button = self.rect

            fill = self.normal_color
            border = self.border_color

        shadow = button.move(4, 4)

        pygame.draw.rect(
            screen,
            (20, 20, 20),
            shadow,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            fill,
            button,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            border,
            button,
            width=3,
            border_radius=12
        )

        line = pygame.Rect(
            button.x + 6,
            button.y + 6,
            button.width - 12,
            2
        )

        pygame.draw.rect(
            screen,
            (160, 160, 160),
            line
        )

        text_shadow = self.font.render(
            self.text,
            True,
            (20, 20, 20)
        )

        text = self.font.render(
            self.text,
            True,
            self.text_color
        )

        shadow_rect = text_shadow.get_rect(center=(button.centerx + 2, button.centery + 2))
        text_rect = text.get_rect(center=button.center)

        screen.blit(text_shadow, shadow_rect)
        screen.blit(text, text_rect)

    def clicked(self, event):

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )