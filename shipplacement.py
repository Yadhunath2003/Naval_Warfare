import pygame
import sys

# GRID SETTINGS
ROWS, COLS = 10, 10
CELL_SIZE = 40
GRID_COLOR = (255, 255, 255)
HOVER_COLOR = (255, 255, 0, 100)

class Ship:
    def __init__(self, name, length, orientation, position, image):
        self.name = name
        self.length = length
        self.orientation = orientation
        self.position = position
        self.image = image
        self.coordinates = self.calculate_coordinates()

    def calculate_coordinates(self):
        x, y = self.position
        coordinates = []
        for i in range(self.length):
            if self.orientation == 'horizontal':
                coordinates.append((x + i, y))
            elif self.orientation == 'vertical':
                coordinates.append((x, y + i))
        return coordinates

    def is_within_bounds(self):
        for x, y in self.coordinates:
            if not (0 <= x < COLS and 0 <= y < ROWS):
                return False
        return True

    def move(self, new_position):
        self.position = new_position
        self.coordinates = self.calculate_coordinates()

    def toggle_orientation(self):
        self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'
        self.coordinates = self.calculate_coordinates()

def draw_grid(window, rows, cols, cell_size, offset=(0, 0)):
    start_x, start_y = offset
    for row in range(rows + 1):
        pygame.draw.line(window, GRID_COLOR, (start_x, start_y + row * cell_size), (start_x + cols * cell_size, start_y + row * cell_size), 1)
    for col in range(cols + 1):
        pygame.draw.line(window, GRID_COLOR, (start_x + col * cell_size, start_y), (start_x + col * cell_size, start_y + rows * cell_size), 1)

def draw_ships(window, ships, cell_size, offset=(0, 0)):
    start_x, start_y = offset
    for ship in ships:
        for i, (x, y) in enumerate(ship.coordinates):
            rotated_image = ship.image
            if ship.orientation == 'vertical':
                rotated_image = pygame.transform.rotate(ship.image, 90)
            window.blit(rotated_image, (start_x + x * cell_size, start_y + y * cell_size))

def size_selection_panel(window, font, cell_size, orientation):
    sizes = [5, 4, 3, 2, 1]
    button_rects = []
    for i, size in enumerate(sizes):
        text = font.render(f'Size {size}', True, (255, 255, 255))
        rect = pygame.Rect((COLS + 2) * cell_size, (i + 1) * cell_size, cell_size * 2, cell_size)
        window.blit(text, rect.topleft)
        pygame.draw.rect(window, (200, 200, 200), rect, 2)
        button_rects.append((rect, size))

    # Orientation toggle button
    orientation_text = font.render(f'Orientation: {orientation}', True, (255, 255, 255))
    orientation_rect_width = orientation_text.get_width() + 10
    orientation_rect = pygame.Rect((COLS + 2) * cell_size, (len(sizes) + 2) * cell_size, orientation_rect_width, cell_size)
    window.blit(orientation_text, orientation_rect.topleft)
    pygame.draw.rect(window, (200, 200, 200), orientation_rect, 2)
    
    return button_rects, orientation_rect

def main():
    pygame.init()
    window_width = (COLS + 7) * CELL_SIZE
    window_height = (ROWS + 5) * CELL_SIZE
    window = pygame.display.set_mode((window_width, window_height), pygame.SRCALPHA)
    pygame.display.set_caption('Naval Warfare')

    # Prompt user for the number of ships (1-5)
    try:
        max_ships = int(input("Enter the number of ships to place (1-5): "))
        if not 1 <= max_ships <= 5:
            print("Please enter a number between 1 and 5.")
            pygame.quit()
            return
    except ValueError:
        print("Invalid input. Please enter a valid integer between 1 and 5.")
        pygame.quit()
        return

    # Background and ship image setup
    background_image = pygame.image.load("images/bg4.png").convert()
    background_image = pygame.transform.scale(background_image, (window_width, window_height))
    ship_image = pygame.image.load("images/ship.png").convert_alpha()
    ship_image = pygame.transform.scale(ship_image, (CELL_SIZE, CELL_SIZE))

    # Initial ship settings
    ships = []
    selected_ship = None
    selected_size = None  # No ship size selected initially
    selected_orientation = "horizontal"
    dragging = False
    font = pygame.font.Font(None, 24)

    running = True
    while running:
        window.blit(background_image, (0, 0))  # Draw background

        # Draw the selection panel
        button_rects, orientation_rect = size_selection_panel(window, font, CELL_SIZE, selected_orientation)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check for size selection clicks
                for rect, size in button_rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_size = size  # Set selected size
                        selected_ship = None  # Clear selection to place a new ship
                        break
                
                # Orientation toggle
                if orientation_rect.collidepoint(mouse_x, mouse_y):
                    if selected_ship:
                        selected_ship.toggle_orientation()
                    else:
                        selected_orientation = 'vertical' if selected_orientation == 'horizontal' else 'horizontal'

                # Check for dragging existing ships
                for ship in ships:
                    ship_rect = pygame.Rect(ship.position[0] * CELL_SIZE, ship.position[1] * CELL_SIZE,
                                            CELL_SIZE * ship.length if ship.orientation == 'horizontal' else CELL_SIZE,
                                            CELL_SIZE if ship.orientation == 'horizontal' else CELL_SIZE * ship.length)
                    if ship_rect.collidepoint(mouse_x, mouse_y):
                        selected_ship = ship
                        dragging = True
                        break
                else:
                    # Place a new ship if within fleet limit and size selected
                    if selected_size is not None and len(ships) < max_ships:
                        new_ship = Ship("Custom Ship", selected_size, selected_orientation, (COLS + 1, 2), ship_image)
                        ships.append(new_ship)
                        selected_ship = new_ship  # Select the new ship for potential dragging
                        selected_size = None  # Reset selected size after placing

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_ship:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE
                    selected_ship.move((grid_x, grid_y))
                    
                    # Check boundaries and collisions
                    if not selected_ship.is_within_bounds() or any(
                        coord in other_ship.coordinates for other_ship in ships if other_ship != selected_ship for coord in selected_ship.coordinates):
                        selected_ship.move((COLS + 1, ships.index(selected_ship) * 2))  # Reset position if invalid

                    dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging and selected_ship:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
                selected_ship.move((grid_x, grid_y))

        # Draw grid and ships
        draw_grid(window, ROWS, COLS, CELL_SIZE, offset=(CELL_SIZE, CELL_SIZE))
        draw_ships(window, ships, CELL_SIZE)

        pygame.display.flip()

if __name__ == "__main__":
    main()
