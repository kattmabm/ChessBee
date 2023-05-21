import pygame
from src.ui.components import BoardComponent
from src.ui.color import Color
from src.ui.window import Window

# WINDOW = pygame.display.set_mode(Window.SIZE)
# pygame.display.set_caption(Window.TITLE)

# def draw_window():
#     WINDOW.fill(Color.BLACK)
#     pygame.display.update()

def main():
    board = BoardComponent()

    # clock = pygame.time.Clock()
    # run = True
    # while run:
    #     clock.tick(Window.FPS)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #     draw_window()
    # pygame.quit()


if __name__ == "__main__":
    main()