import pygame
import sys
from naval_warfare_game import GamePlay
from player import Player

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1100, 600
GRID_SIZE = 10
CELL_SIZE = 30
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
LIGHT_GREY = (200, 200, 200)
GRID_SPACING = 10  # Spacing between the two grids
GREEN = (0, 255, 0)

def draw_grid(window, offset_x, offset_y):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(
                window,
                WHITE,
                pygame.Rect(offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )

def draw_board(window, board, offset_x, offset_y, hide_ships=True):
    for y, row in enumerate(board.grid):
        for x, cell in enumerate(row):
            if cell == "X":  # Hit
                pygame.draw.rect(
                    window,
                    RED,
                    pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )
            elif cell == "O":  # Miss
                pygame.draw.rect(
                    window,
                    BLUE,
                    pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )
            elif not hide_ships and cell != 0:  # Ship cell
                pygame.draw.rect(
                    window,
                    GREEN,
                    pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )

def draw_scorecard(window, font, player1, player2, offset_x, offset_y):
    score_texts = [
        f"Player 1: Hits {len(player1.hits)} Misses {len(player1.misses)}",
        f"Player 2: Hits {len(player2.hits)} Misses {len(player2.misses)}"
    ]
    for i, text in enumerate(score_texts):
        text_surface = font.render(text, True, BLACK)
        window.blit(text_surface, (offset_x, offset_y + i * 30))

def display_turn(window, font, player_name):
    text = f"{player_name}'s Turn"
    text_surface = font.render(text, True, BLACK)
    window.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, 10))

def game_loop(game):
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Battleship Gameplay")
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and game.current_player.name == "Player 1":
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = (mouse_x - (450 + GRID_SPACING)) // CELL_SIZE  # Adjust offset for opponent's grid
                grid_y = mouse_y // CELL_SIZE

                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    result = game.process_turn(grid_x, grid_y)
                    if not result["valid"]:
                        print(result["message"])
                    elif game.game_over:
                        print(f"Game Over! {game.winner} wins!")
                        running = False

        window.fill(LIGHT_GREY)

        # Draw Player 1's grid
        draw_grid(window, 50, 50)
        draw_board(window, game.player1.board, 50, 50, hide_ships=False)

        # Draw Player 2's grid (opponent) with spacing
        draw_grid(window, 450 + GRID_SPACING, 50)
        draw_board(window, game.player2.board, 450 + GRID_SPACING, 50)

        display_turn(window, font, game.current_player.name)
        draw_scorecard(window, font, game.player1, game.player2, 50, 600)

        pygame.display.flip()