import pygame
import sys
from naval_warfare_game import GamePlay
from player import Player
from end_game import scorecard_screen

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

def draw_board(window, board, offset_x, offset_y, show_ships=False):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == 'X':  # Hit
                pygame.draw.rect(window, RED, pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == 'O':  # Miss
                pygame.draw.rect(window, BLUE, pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == 'S' and show_ships:  # Ship
                pygame.draw.rect(window, GREEN, pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(window, WHITE, pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def draw_scorecard(window, font, player1, player2, offset_x, offset_y):
    """
    Render the scorecard showing player hits and misses.
    """
    score_texts = [
        f"Player 1: Hits {len(player1.hits)} Misses {len(player1.misses)}",
        f"Player 2: Hits {len(player2.hits)} Misses {len(player2.misses)}"
    ]
    for i, text in enumerate(score_texts):
        text_surface = font.render(text, True, LIGHT_GREY)
        window.blit(text_surface, (offset_x, offset_y + i * 30))


def display_turn(window, font, player_name):
    text = f"{player_name}'s Turn"
    text_surface = font.render(text, True, LIGHT_GREY)
    window.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, 10))


def game_loop(game):
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Battleship Gameplay")
    font = pygame.font.Font(None, 36)

    background_image = pygame.image.load("images/bg4.png").convert()
    background_image = pygame.transform.scale(background_image, (1100, 600))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if game.current_player == game.player1:
                    offset_x, offset_y = 450 + GRID_SPACING, 50
                else:
                    offset_x, offset_y = 50, 50

                grid_x = (mouse_x - offset_x) // CELL_SIZE
                grid_y = (mouse_y - offset_y) // CELL_SIZE

                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    result = game.process_turn(grid_x, grid_y)
                    if not result["valid"]:
                        print(result["message"])
                    elif game.game_over:
                        print(f"Game Over! {game.winner} wins!")
                        running = False
                    # Gather game statistics
                        player1_accuracy = (len(game.player1.hits) / (len(game.player1.hits) + len(game.player1.misses))) * 100 if len(game.player1.hits) + len(game.player1.misses) > 0 else 0
                        player2_accuracy = (len(game.player2.hits) / (len(game.player2.hits) + len(game.player2.misses))) * 100 if len(game.player2.hits) + len(game.player2.misses) > 0 else 0
                        game_stats = {
                            'player1_hits': len(game.player1.hits),
                            'player1_misses': len(game.player1.misses),
                            'player2_hits': len(game.player2.hits),
                            'player2_misses': len(game.player2.misses),
                            'turns': game.turns,
                            'player1_turns': game.player1_turns,  # Player 1's turns
                            'player2_turns': game.player2_turns,  # Player 2's turns
                            'player1_accuracy': player1_accuracy,
                            'player2_accuracy': player2_accuracy,
                            'winner': game.winner
                        }
                        scorecard_screen(game_stats, "images/bg4.png")  # Transition to scorecard screen
                else:
                    print("Click outside valid grid area.")

        # Draw background
        window.blit(background_image, (0, 0))

        # Draw Player 1's grid
        draw_grid(window, 50, 50)
        draw_board(window, game.player1.board.grid, 50, 50, show_ships=(game.current_player == game.player1))

        # Draw Player 2's grid
        draw_grid(window, 450 + GRID_SPACING, 50)
        draw_board(window, game.player2.board.grid, 450 + GRID_SPACING, 50, show_ships=(game.current_player == game.player2))

        # Display the current player's turn
        display_turn(window, font, game.current_player.name)

        # Draw the scorecard
        draw_scorecard(window, font, game.player1, game.player2, 50, 450)

        pygame.display.flip()

