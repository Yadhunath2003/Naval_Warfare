import pygame
from game_state import GameState, title_screen, game_mode, ai_mode, select_number_of_boats
from shipplacement import main as ship_placement_main, ship_placement_complete
from naval_warfare_game import NavalWarfareGame

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
CELL_SIZE = 40
MARGIN = 50
GRID_SIZE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (106, 159, 181)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def draw_grid(screen, board, offset_x, offset_y, hide_ships=False):
    """
    Draw the game grid, showing hits, misses, and optionally hiding ships.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(offset_x + x * CELL_SIZE, offset_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

            if board.grid[y][x] == -1:  # Miss
                pygame.draw.circle(screen, BLUE, rect.center, 5)
            elif board.grid[y][x] == 2:  # Hit
                pygame.draw.line(screen, RED, rect.topleft, rect.bottomright, 2)
                pygame.draw.line(screen, RED, rect.topright, rect.bottomleft, 2)
            elif board.grid[y][x] > 0 and not hide_ships:  # Ship
                pygame.draw.rect(screen, GREEN, rect.inflate(-5, -5))


def main():
    """ Main function to initialize pygame and manage game states. """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Naval Warfare")
    game_state = GameState.TITLE  # Initialize the game state to TITLE
    game = None

    while game_state != GameState.QUIT:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        elif game_state == GameState.NEWGAME:
            game_state = game_mode(screen)

        elif game_state == GameState.AIMODE:
            game_state = ai_mode(screen)

        elif game_state in [GameState.HUMAN, GameState.EASYSHIPS, GameState.MEDIUMSHIPS, GameState.HARDSHIPS]:
            selected_boats = select_number_of_boats(screen)

            if selected_boats > 0:
                # Transition to ship placement
                ship_placement_main()

                # Wait for Play button
                if ship_placement_complete(screen):  # Wait for Play button to be clicked
                    print("Transitioning to gameplay...")  # Debugging log
                    # Initialize the Naval Warfare Game
                    game = NavalWarfareGame(player_name="Player 1")
                    player_ships = [
                        (5, "horizontal", (0, 0)),
                        (4, "vertical", (2, 2)),
                        (3, "horizontal", (5, 5)),
                        (3, "vertical", (7, 0)),
                        (2, "horizontal", (8, 8)),
                    ]
                    game.place_player_ships(player_ships)

                    # Transition to gameplay state
                    game_state = GameState.PLAYING

        elif game_state == GameState.PLAYING:
            print("Entering gameplay state...")  # Debugging log
            running = True
            while running:
                screen.fill(BLACK)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game_state = GameState.QUIT
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if game.current_turn == "Player":
                            # Get grid coordinates for player attack
                            mouse_x, mouse_y = event.pos
                            grid_x = (mouse_x - MARGIN) // CELL_SIZE
                            grid_y = (mouse_y - MARGIN) // CELL_SIZE
                            if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                                game.process_turn(grid_x, grid_y)  # Player's turn logic

                # Check if it's AI's turn and let AI play automatically
                if game.current_turn == "AI" and not game.game_over:
                    game.process_turn()  # AI's turn logic

                # Draw grids for player and AI
                draw_grid(screen, game.player_board, MARGIN, MARGIN)  # Player's grid
                draw_grid(screen, game.ai_board, WINDOW_WIDTH // 2 + MARGIN, MARGIN, hide_ships=True)  # AI's grid

                # Display game over message
                if game.game_over:
                    font = pygame.font.Font(None, 36)
                    text = font.render(f"Game Over! Winner: {game.winner}", True, RED)
                    screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2))
                    pygame.display.flip()
                    pygame.time.wait(3000)  # Wait 3 seconds before returning to title
                    running = False
                    game_state = GameState.TITLE

                pygame.display.flip()
                pygame.time.Clock().tick(30)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

