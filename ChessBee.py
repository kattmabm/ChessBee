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
                squares = [square for rank in BOARD.squares
                           for square in rank
                           if square.rect.collidepoint(pos)]
                if not squares:
                    continue
                square_component = squares[0]
                if square_component.selected:
                    BOARD.clear_colors()
                    continue
                BOARD.clear_colors()
                square = BOARD.board.square_at(square_component.rank, square_component.file)
                if square.piece and square.piece.color is BOARD.board.current_turn:
                    BOARD.select_square_at(square.rank, square.file)
                    moves = BOARD.board.get_legal_moves(square)
                    for move in moves:
                        BOARD.hl_square_at(move.rank, move.file)
        draw_window()
    pygame.quit()


if __name__ == "__main__":
    main()