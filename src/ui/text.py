import pygame
from src.ui.color import Color

class Text:

    def font(size: int, family="Helvetica") -> pygame.font.Font:
        pygame.font.init()
        return pygame.font.SysFont(family, size)
    
    DEFAULT_FONT = font(20)


class Label:
    __slots__ = ("window", "image", "rect", "font", "text",
                 "xmin", "ymin", "width", "height")

    def __init__(self, window: pygame.Surface, text: str, xcenter: int, ycenter: int, font_size: int) -> None:
        self.window = window
        self.text = text
        self.font = Text.font(font_size)
        self.image = self.font.render(text, True, Color.WHITE)
        self.rect = self.image.get_rect(center=(xcenter, ycenter))
        # _, _, self.width, self.height = self.image.get_rect()
        # self.rect = pygame.Rect(xmin, ymin, self.width, self.height)

    def draw(self):
        self.window.blit(self.image, self.rect)

