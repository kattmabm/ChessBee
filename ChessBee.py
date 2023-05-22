import pygame
from src.ui.components import BoardComponent
from src.ui.color import Color
from src.ui.window import Window

WINDOW = pygame.display.set_mode(Window.SIZE)
pygame.display.set_caption(Window.TITLE)

BOARD = BoardComponent(WINDOW)

def draw_window():
    WINDOW.fill(Color.BLACK)
    BOARD.draw()
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(Window.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                square = [square for rank in BOARD.squares
                           for square in rank
                           if square.rect.collidepoint(pos)]
                if not square:
                    continue
                BOARD.clear_colors()
                loc = square[0].position
                BOARD.select_square((loc.rank, loc.file))
                if loc.piece:
                    moves = loc.piece.possible_moves(loc.rank, loc.file)
                    BOARD.hl_squares_g(moves)
                    captures = loc.piece.possible_captures(loc.rank, loc.file)
                    BOARD.hl_squares_r(captures)
        draw_window()
    pygame.quit()


if __name__ == "__main__":
    main()