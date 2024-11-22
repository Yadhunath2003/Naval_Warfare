import pygame
import sys

# Constants
ROWS, COLS = 10, 10
CELL_SIZE = 40
WINDOW_WIDTH = COLS * CELL_SIZE + 200  # Resized window width for game window
WINDOW_HEIGHT = ROWS * CELL_SIZE + 100  # Resized window height for game window
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

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Naval Warfare - Ship Placement')

    # Background Image
    background_image = pygame.image.load("images/bg4.png").convert()
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Ship Images
    ship_image = pygame.image.load("images/ship.png").convert_alpha()
    ship_image = pygame.transform.scale(ship_image, (CELL_SIZE, CELL_SIZE))

    # Placeholder Text for Player
    font = pygame.font.Font(None, 36)
    player_text = "Player 1's base"

    # Confirm and Play Buttons
    button_font = pygame.font.Font(None, 28)
    confirm_button = pygame.Rect(WINDOW_WIDTH - 300, WINDOW_HEIGHT - 50, 120, 40)
    play_button = pygame.Rect(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50, 120, 40)
    play_button_active = False

    # Ship Placement Initialization with Different Sizes
    ships = [
        Ship(5, "horizontal", (COLS + 1, 0), ship_image),
        Ship(4, "horizontal", (COLS + 1, 2), ship_image),
        Ship(3, "horizontal", (COLS + 1, 4), ship_image),
        Ship(2, "horizontal", (COLS + 1, 6), ship_image),
        Ship(1, "horizontal", (COLS + 1, 8), ship_image)
    ]
    max_boats = len(ships)  # Allow placing all ships
    boats_placed = 0
    selected_ship = None
    dragging = False

    # Game Loop
    running = True
    while running:
        window.blit(background_image, (0, 0))  # Draw Background

        # Draw Player Placeholder Text
        text_surface = font.render(player_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, 20))
        window.blit(text_surface, text_rect)

        # Draw Grid
        draw_grid(window, ROWS, COLS, CELL_SIZE, offset=(CELL_SIZE, CELL_SIZE))

        # Draw Ships
        draw_ships(window, ships, CELL_SIZE)

        # Draw Confirm Button
        pygame.draw.rect(window, LIGHT_GREY, confirm_button)
        confirm_text = button_font.render("Confirm", True, BLACK)
        window.blit(confirm_text, (confirm_button.x + 20, confirm_button.y + 10))

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
                if confirm_button.collidepoint(mouse_x, mouse_y):
                    # Confirm Button Clicked
                    if boats_placed == max_boats:
                        play_button_active = True
                        message_surface = font.render("All boats placed!", True, GREEN)
                        message_rect = message_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                        window.blit(message_surface, message_rect)
                    else:
                        message_surface = font.render("Please place all ships before confirming!", True, (255, 0, 0))
                        message_rect = message_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                        window.blit(message_surface, message_rect)
                elif play_button_active and play_button.collidepoint(mouse_x, mouse_y):
                    # Play Button Clicked
                    print("Starting the game!")  # Placeholder for transitioning to gameplay
                else:
                    # Check if a ship is clicked
                    for ship in ships:
                        ship_rect = pygame.Rect(ship.position[0] * CELL_SIZE, ship.position[1] * CELL_SIZE,
                                                CELL_SIZE * ship.length if ship.orientation == 'horizontal' else CELL_SIZE,
                                                CELL_SIZE if ship.orientation == 'horizontal' else CELL_SIZE * ship.length)
                        if ship_rect.collidepoint(mouse_x, mouse_y):
                            if boats_placed < max_boats or ship.selected:
                                selected_ship = ship
                                dragging = True
                                break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_ship:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = min(max(mouse_x // CELL_SIZE, 0), COLS - (1 if selected_ship.orientation == 'horizontal' else selected_ship.length))
                    grid_y = min(max(mouse_y // CELL_SIZE, 0), ROWS - (selected_ship.length if selected_ship.orientation == 'vertical' else 1))
                    selected_ship.move((grid_x, grid_y))
                    if not selected_ship.is_within_bounds() or any(
                            coord in other_ship.coordinates for other_ship in ships if other_ship != selected_ship for coord in selected_ship.coordinates):
                        # Reset ship if out of bounds or overlapping
                        selected_ship.move((COLS + 1, ships.index(selected_ship) * 2))
                    else:
                        boats_placed += 1 if not selected_ship.selected else 0
                    selected_ship.selected = True
                    selected_ship = None
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging and selected_ship:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = min(max(mouse_x // CELL_SIZE, 0), COLS - (1 if selected_ship.orientation == 'horizontal' else selected_ship.length))
                grid_y = min(max(mouse_y // CELL_SIZE, 0), ROWS - (selected_ship.length if selected_ship.orientation == 'vertical' else 1))
                selected_ship.move((grid_x, grid_y))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and selected_ship:
                    selected_ship.rotate()

        pygame.display.flip()

if __name__ == "__main__":
    main()
