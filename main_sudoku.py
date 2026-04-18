import pygame, sys
from board import Board

def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 620))
    pygame.display.set_caption("Sudoku")
    state, board = "start", None

    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            if state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 400 <= y <= 450:
                        if 50 <= x <= 170: board, state = Board(540, 540, screen, "easy"), "game"
                        elif 210 <= x <= 330: board, state = Board(540, 540, screen, "medium"), "game"
                        elif 370 <= x <= 490: board, state = Board(540, 540, screen, "hard"), "game"
            
            elif state == "game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    res = board.click(x, y)
                    if res: board.select(*res)
                    if 550 <= y <= 590:
                        if 50 <= x <= 150: board.reset_to_original()
                        elif 220 <= x <= 320: state = "start"
                        elif 390 <= x <= 490: pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and board.selected_row > 0: board.select(board.selected_row-1, board.selected_col)
                    elif event.key == pygame.K_DOWN and board.selected_row < 8: board.select(board.selected_row+1, board.selected_col)
                    elif event.key == pygame.K_LEFT and board.selected_col > 0: board.select(board.selected_row, board.selected_col-1)
                    elif event.key == pygame.K_RIGHT and board.selected_col < 8: board.select(board.selected_row, board.selected_col+1)
                    
                    if pygame.K_1 <= event.key <= pygame.K_9: board.sketch(event.key - pygame.K_0)
                    if event.key == pygame.K_RETURN:
                        board.place_number(board.cells[board.selected_row][board.selected_col].sketched_value)
                        if board.is_full(): state = "win" if board.check_board() else "lose"

        if state == "start":
            font = pygame.font.Font(None, 60)
            screen.blit(font.render("Sudoku", True, (0,0,0)), (200, 150))
            for i, diff in enumerate(["EASY", "MEDIUM", "HARD"]):
                pygame.draw.rect(screen, (255, 165, 0), (50 + i*160, 400, 120, 50))
                screen.blit(pygame.font.Font(None, 30).render(diff, True, (255,255,255)), (70 + i*160, 415))
        elif state == "game":
            board.draw()
            for i, txt in enumerate(["RESET", "RESTART", "EXIT"]):
                pygame.draw.rect(screen, (255, 165, 0), (50 + i*170, 550, 100, 40))
                screen.blit(pygame.font.Font(None, 25).render(txt, True, (255,255,255)), (65 + i*170, 560))
        elif state in ["win", "lose"]:
            txt = "YOU WIN!" if state == "win" else "GAME OVER"
            screen.blit(pygame.font.Font(None, 80).render(txt, True, (0,0,0)), (130, 250))
            
        pygame.display.update()

if __name__ == "__main__": main()
