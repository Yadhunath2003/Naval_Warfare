import pygame
import sys

# GRID SET
ROWS, COLS = 10, 10
CELL_SIZE = 40
GRID_COLOR = (255, 255, 255)
HOVER_COLOR = (255, 255, 0, 100)

# SHIP PLACEMENT
class Ship:
    def __init__(self, name, length, orientation, position, image):
        self.name = name
        self.length = length
        self.orientation = orientation
        self.position = position
        self.image = image
        self.coordinates = self.calculate_coordinates()

    def calculate_coordinates(self):  # CHECK SHIP COORDS
        x, y = self.position
        coordinates = []
        for i in range(self.length):
            if self.orientation == 'horizontal':
                coordinates.append((x + i, y))
            elif self.orientation == 'vertical':
                coordinates.append((x, y + i))
        return coordinates

    def is_within_bounds(self):  # BOUNDARY CHECK
        for x, y in self.coordinates:
            if not (0 <= x < COLS and 0 <= y < ROWS):
                return False
        return True

    def move(self, new_position):  # SHIP POSITION
        self.position = new_position
        self.coordinates = self.calculate_coordinates()

    def toggle_orientation(self):  # TOGGLE ORIENTATION
        self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal'
        self.coordinates = self.calculate_coordinates()

def draw_grid(window, rows, cols, cell_size, offset=(0, 0)):  # DRAW GRID
    start_x, start_y = offset
    for row in range(rows + 1):
        pygame.draw.line(window, GRID_COLOR, (start_x, start_y + row * cell_size), (start_x + cols * cell_size, start_y + row * cell_size), 1)
    for col in range(cols + 1):
        pygame.draw.line(window, GRID_COLOR, (start_x + col * cell_size, start_y), (start_x + col * cell_size, start_y + rows * cell_size), 1)

def draw_ships(window, ships, cell_size, offset=(0, 0)):  # DRAW SHIPS
    start_x, start_y = offset
    for ship in ships:
        for i, (x, y) in enumerate(ship.coordinates):
            rotated_image = ship.image
            if ship.orientation == 'vertical':
                rotated_image = pygame.transform.rotate(ship.image, 90)
            window.blit(rotated_image, (start_x + x * cell_size, start_y + y * cell_size))

def size_selection_panel(window, font, cell_size, orientation):  # SIZE SELECTION PANEL
    sizes = [5, 4, 3, 2, 1]
    button_rects = []
    for i, size in enumerate(sizes):
        text = font.render(f'Size {size}', True, (255, 255, 255))
        rect = pygame.Rect((COLS + 2) * cell_size, (i + 1) * cell_size, cell_size * 2, cell_size)
        window.blit(text, rect.topleft)
        pygame.draw.rect(window, (200, 200, 200), rect, 2)
        button_rects.append((rect, size))

    # Orientation toggle button with dynamic width
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

    # BACKGROUND SPRITE IMAGE
    background_image = pygame.image.load("images/bg4.png").convert()
    background_image = pygame.transform.scale(background_image, (window_width, window_height))

    # SHIP SPRITE IMAGE
    ship_image = pygame.image.load("images/ship.png").convert_alpha()
    ship_image = pygame.transform.scale(ship_image, (CELL_SIZE, CELL_SIZE))

    # INITIAL SHIP SETTINGS
    ships = []
    selected_ship = None
    selected_size = None  # No ship size selected initially
    selected_orientation = "horizontal"
    dragging = False

    font = pygame.font.Font(None, 24)
    button_rects = []

    # GAME LOOP
    running = True
    while running:
        window.blit(background_image, (0, 0))  # BACKGROUND

        # Draw selection panel for ship sizes and orientation
        button_rects, orientation_rect = size_selection_panel(window, font, CELL_SIZE, selected_orientation)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check for clicks on size buttons
                for rect, size in button_rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_size = size  # Set selected size
                        selected_ship = None  # Deselect any ship to place a new one
                        break
                
                # Check for clicks on the orientation toggle
                if orientation_rect.collidepoint(mouse_x, mouse_y):
                    # Toggle orientation of selected ship, or change default orientation if none selected
                    if selected_ship:
                        selected_ship.toggle_orientation()
                    else:
                        selected_orientation = 'vertical' if selected_orientation == 'horizontal' else 'horizontal'

                # Check if selecting an existing ship for dragging
                for ship in ships:
                    ship_rect = pygame.Rect(ship.position[0] * CELL_SIZE, ship.position[1] * CELL_SIZE,
                                            CELL_SIZE * ship.length if ship.orientation == 'horizontal' else CELL_SIZE,
                                            CELL_SIZE if ship.orientation == 'horizontal' else CELL_SIZE * ship.length)
                    if ship_rect.collidepoint(mouse_x, mouse_y):
                        selected_ship = ship
                        dragging = True
                        break
                else:
                    # Create a new ship with the selected size and orientation if no existing ship is selected
                    if selected_size is not None:
                        new_ship = Ship("Custom Ship", selected_size, selected_orientation, (COLS + 1, 2), ship_image)
                        ships.append(new_ship)
                        selected_ship = new_ship  # Select the new ship for potential dragging
                        selected_size = None  # Reset selected size after placing the ship

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_ship:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE
                    selected_ship.move((grid_x, grid_y))
                    dragging = False

            elif event.type == pygame.MOUSEMOTION and dragging and selected_ship:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
                selected_ship.move((grid_x, grid_y))

        # DRAW
        draw_grid(window, ROWS, COLS, CELL_SIZE, offset=(CELL_SIZE, CELL_SIZE))
        draw_ships(window, ships, CELL_SIZE)

        pygame.display.flip()

if __name__ == "__main__":
    main()
