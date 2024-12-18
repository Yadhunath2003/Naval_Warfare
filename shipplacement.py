import pygame
from game_logic import GameBoard
import sys
from game_state import select_number_of_boats
from player import Player, AIPlayer

# Constants
ROWS, COLS = 10, 10
CELL_SIZE = 40
WINDOW_WIDTH = 800  # Resized window width for game window
WINDOW_HEIGHT = 600  # Resized window height for game window
GRID_COLOR = (255, 255, 255)
HOVER_COLOR = (255, 255, 0, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GREY = (200, 200, 200)
GREEN = (0, 255, 0)

# Ship Placement Class
class Ship:
    def __init__(self, length, orientation, position, image):
        self.length = length
        self.orientation = orientation
        self.position = position
        self.image = image
        self.coordinates = self.calculate_coordinates()
        self.selected = False

    def calculate_coordinates(self):
        """
        Calculate ship coordinates based on its length, orientation, and starting position.
        """
        x, y = self.position
        coordinates = []
        for i in range(self.length):
            if self.orientation == 'horizontal':
                coordinates.append((x + i, y))
            elif self.orientation == 'vertical':
                coordinates.append((x, y + i))
        return coordinates

    def is_within_bounds(self):
        """
        Check if the ship is within the grid bounds.
        """
        for x, y in self.coordinates:
            if not (0 <= x < COLS and 0 <= y < ROWS):
                return False
        return True

    def move(self, new_position):
        """
        Move the ship to a new position and update coordinates.
        """
        self.position = new_position
        self.coordinates = self.calculate_coordinates()

    def rotate(self):
        """
        Rotate the ship and update coordinates.
        """
        self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'
        self.coordinates = self.calculate_coordinates()

def draw_grid(window, rows, cols, cell_size, offset=(0, 0)):
    """
    Draw the grid lines for the ship placement area.
    """
    start_x, start_y = offset
    for row in range(rows + 1):
        pygame.draw.line(window, GRID_COLOR, (start_x, start_y + row * cell_size),
                         (start_x + cols * cell_size, start_y + row * cell_size), 1)
    for col in range(cols + 1):
        pygame.draw.line(window, GRID_COLOR, (start_x + col * cell_size, start_y),
                         (start_x + col * cell_size, start_y + rows * cell_size), 1)

def draw_ships(window, ships, cell_size, offset=(0, 0)):
    """
    Draw all ships on the grid.
    """
    start_x, start_y = offset
    for ship in ships:
        rotated_image = pygame.transform.scale(ship.image, (cell_size * ship.length, cell_size))
        if ship.orientation == 'vertical':
            rotated_image = pygame.transform.rotate(rotated_image, 90)
        window.blit(rotated_image, (start_x + ship.position[0] * cell_size, start_y + ship.position[1] * cell_size))

def create_game_logic(rows, cols):
    """
    Create a grid logic representation for the ship placement area.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def ship_placement_main(player, selected_boats, is_player1=True):
    if not is_player1 and player.name == "AI":  # AI-specific logic
        ship_lengths = [5, 4, 3, 2, 1][:selected_boats]
        print(f"{player.name} is placing ships in the backend...")
        player.board.randomly_place_ships(ship_lengths)
        print(f"{player.name}'s ship placement complete.")
        return
    
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"{player.name}'s Ship Placement")

    # Background Image
    background_image = pygame.image.load("images/bg4.png").convert()
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Initialize Player's Board
    board = player.board

    # Ship Images
    ship_image = pygame.image.load("images/ship.png").convert_alpha()
    ship_image = pygame.transform.scale(ship_image, (CELL_SIZE, CELL_SIZE))

    # Placeholder Text for Player
    font = pygame.font.Font(None, 36)

    # Buttons
    button_font = pygame.font.Font(None, 28)
    confirm_button = pygame.Rect(WINDOW_WIDTH - 300, WINDOW_HEIGHT - 50, 120, 40)
    next_button = pygame.Rect(WINDOW_WIDTH - 300, WINDOW_HEIGHT - 100, 120, 40)
    play_button = pygame.Rect(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50, 120, 40)

    # Initialize Ship Placement
    ships = [
        Ship(5, "horizontal", (COLS + 1, 0), ship_image),
        Ship(4, "horizontal", (COLS + 1, 2), ship_image),
        Ship(3, "horizontal", (COLS + 1, 4), ship_image),
        Ship(2, "horizontal", (COLS + 1, 6), ship_image),
        Ship(1, "horizontal", (COLS + 1, 8), ship_image),
    ]

    boats_placed = 0
    selected_ship = None
    dragging = False
    confirm_active = False
    next_active = False
    play_button_active = False

    # Game Loop
    running = True
    while running:
        window.blit(background_image, (0, 0))  # Draw Background

        # Draw Player Placeholder Text
        player_text = f"{player.name}'s base"
        text_surface = font.render(player_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 20))
        window.blit(text_surface, text_rect)

        # Draw Grid
        draw_grid(window, ROWS, COLS, CELL_SIZE, offset=(CELL_SIZE, CELL_SIZE))

        # Draw Ships
        draw_ships(window, ships, CELL_SIZE)

        # Draw Confirm Button
        pygame.draw.rect(window, GREEN if boats_placed == selected_boats else LIGHT_GREY, confirm_button)
        confirm_text = button_font.render("Confirm", True, BLACK)
        window.blit(confirm_text, (confirm_button.x + 20, confirm_button.y + 10))

        # Draw Next Button
        pygame.draw.rect(window, GREEN if next_active else LIGHT_GREY, next_button)
        next_text = button_font.render("Next", True, BLACK if next_active else (150, 150, 150))
        window.blit(next_text, (next_button.x + 20, next_button.y + 10))

        # Draw Play Button
        pygame.draw.rect(window, GREEN if play_button_active else LIGHT_GREY, play_button)
        play_text = button_font.render("Play", True, BLACK if play_button_active else (150, 150, 150))
        window.blit(play_text, (play_button.x + 35, play_button.y + 10))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Confirm Button Logic
                if confirm_button.collidepoint(mouse_x, mouse_y) and boats_placed == selected_boats:
                    for ship in ships:
                        valid = board.place_ship(ship.length, ship.orientation, ship.position)
                        if not valid:
                            print(f"Invalid placement for ship {ship.length}.")
                            break
                    print(f"{player.name} confirmed their ship placement.")
                    confirm_active = False
                    if is_player1:
                        next_active = True  # Enable Next for Player 1
                    else:
                        play_button_active = True  # Enable Play for Player 2
                    # Display updated board
                    board.display_ship_placements()

                # Next Button Logic
                elif next_button.collidepoint(mouse_x, mouse_y) and next_active:
                    print("Transitioning to Player 2's base...")
                    running = False  # Exit for Player 2's placement

                # Play Button Logic
                elif play_button.collidepoint(mouse_x, mouse_y) and play_button_active:
                    print("Starting the game!")  # Transition to gameplay
                    running = False
                else:
                    # Check if a ship is clicked for dragging
                    for ship in ships:
                        ship_rect = pygame.Rect(
                            ship.position[0] * CELL_SIZE, ship.position[1] * CELL_SIZE,
                            CELL_SIZE * ship.length if ship.orientation == 'horizontal' else CELL_SIZE,
                            CELL_SIZE if ship.orientation == 'horizontal' else CELL_SIZE * ship.length,
                        )
                        if ship_rect.collidepoint(mouse_x, mouse_y):
                            selected_ship = ship
                            dragging = True
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_ship:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = min(max(mouse_x // CELL_SIZE, 0), COLS - (1 if selected_ship.orientation == 'horizontal' else selected_ship.length))
                    grid_y = min(max(mouse_y // CELL_SIZE, 0), ROWS - (selected_ship.length if selected_ship.orientation == 'vertical' else 1))
                     # Try placing the ship in its new position
                    previous_coordinates = selected_ship.coordinates.copy()

                    selected_ship.move((grid_x, grid_y))

                    # Check if placement is invalid (out of bounds or overlapping)
                    if not selected_ship.is_within_bounds() or any(
                        coord in other_ship.coordinates for other_ship in ships if other_ship != selected_ship for coord in selected_ship.coordinates):
                        # Reset ship if out of bounds or overlapping
                        selected_ship.move((COLS + 1, ships.index(selected_ship) * 2))

                    selected_ship.selected = True
                    selected_ship = None
                    dragging = False

                # Dynamically calculate boats_placed
                boats_placed = sum(
                    all(0 <= x < COLS and 0 <= y < ROWS for x, y in ship.coordinates)
                    for ship in ships
                )
                confirm_active = boats_placed == selected_boats

            elif event.type == pygame.MOUSEMOTION and dragging and selected_ship:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = min(max(mouse_x // CELL_SIZE, 0), COLS - (1 if selected_ship.orientation == 'horizontal' else selected_ship.length))
                grid_y = min(max(mouse_y // CELL_SIZE, 0), ROWS - (selected_ship.length if selected_ship.orientation == 'vertical' else 1))
                selected_ship.move((grid_x, grid_y))

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and selected_ship:
                    selected_ship.rotate()

        pygame.display.flip()



