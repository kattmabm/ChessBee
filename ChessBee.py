# import pygame
from src.engine.board import Board
# import src.ui.color as color
# import src.ui.window as win

# WINDOW = pygame.display.set_mode(win.SIZE)
# pygame.display.set_caption(win.TITLE)

# def draw_window():
#     WINDOW.fill(color.BOARD_DARK)
#     pygame.display.update()

def main():
    b = Board()
    print()
    print("Setting up chess board")
    b.print_squares()

    # clock = pygame.time.Clock()
    # run = True
    # while run:
    #     clock.tick(win.FPS)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #     draw_window()
    # pygame.quit()


if __name__ == "__main__":
    main()