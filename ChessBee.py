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
                continue
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                squares = [square for rank in BOARD.squares
                           for square in rank
                           if square.rect.collidepoint(pos)]
                if not squares:
                    continue
                square_component = squares[0]
                BOARD.clear_colors()
                if square_component.selected:
                    continue
                rank = square_component.rank
                file = square_component.file
                square = BOARD.board.square_at(rank, file)
                if square_component.highlighted:
                    old_square = BOARD.selected_square_pos
                    # piece = old_square.piece
                    # print(f"Moving {piece.__class__.__name__} from {old_square} to {new_square}.")
                    BOARD.board.move_piece(old_square, square)
                    BOARD.board.change_turn()
                    continue
                if square.piece and square.piece.color is BOARD.board.current_turn:
                    BOARD.select_square_at(square.rank, square.file)
                    moves = BOARD.board.get_legal_moves(square)
                    for move in moves:
                        BOARD.hl_square_at(move.rank, move.file)
        draw_window()
    pygame.quit()


if __name__ == "__main__":
    main()