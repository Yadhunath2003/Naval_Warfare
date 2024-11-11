import pygame
import sys

# GRID SET
ROWS, COLS = 10, 10
CELL_SIZE = 40
GRID_COLOR = (255, 255, 255)
HOVER_COLOR = (255, 255, 0, 100)

#SHIP PLACEMENT
class Ship:
    def __init__(self, name, length, orientation, position, image):
        self.name = name
        self.length = length
        self.orientation = orientation
        self.position = position
        self.image = image
        self.coordinates = self.calculate_coordinates()
        self.selected = False

    def calculate_coordinates(self): #CHECK SHIP COORDS
        x, y = self.position
        coordinates = []
        for i in range(self.length):
            if self.orientation == 'horizontal':
                coordinates.append((x + i, y))
            elif self.orientation == 'vertical':
                coordinates.append((x, y + i))
        return coordinates

    def is_within_bounds(self):#BOUNDARY CHECK
        for x, y in self.coordinates:
            if not (0 <= x < COLS and 0 <= y < ROWS):
                return False
        return True

    def move(self, new_position):#sHIP POSITION
        self.position = new_position
        self.coordinates = self.calculate_coordinates()

    def rotate(self):
        self.orientation = 'vertical' if self.orientation == 'horizontal' else 'horizontal' #SHIP ROTATION
        self.coordinates = self.calculate_coordinates()

def draw_grid(window, rows, cols, cell_size, offset=(0, 0)): #DRAW GRID
    start_x, start_y = offset
    for row in range(rows + 1):
        pygame.draw.line(window, GRID_COLOR, (start_x, start_y + row * cell_size), (start_x + cols * cell_size, start_y + row * cell_size), 1)
    for col in range(cols + 1):
        pygame.draw.line(window, GRID_COLOR, (start_x + col * cell_size, start_y), (start_x + col * cell_size, start_y + rows * cell_size), 1)

def draw_ships(window, ships, cell_size, offset=(0, 0)): #DRAW SHIPS
    start_x, start_y = offset
    for ship in ships:
        for i, (x, y) in enumerate(ship.coordinates):
            rotated_image = ship.image
            if ship.orientation == 'vertical':
                rotated_image = pygame.transform.rotate(ship.image, 90)
            window.blit(rotated_image, (start_x + x * cell_size, start_y + y * cell_size))

def create_game_logic(rows, cols): #LOGIC GRID
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def main():
    pygame.init()
    window_width = (COLS + 5) * CELL_SIZE
    window_height = (ROWS + 5) * CELL_SIZE
    window = pygame.display.set_mode((window_width, window_height), pygame.SRCALPHA)
    pygame.display.set_caption('Naval Warfare')

    # BACKGROUND SPRITE IMAGE
    background_image = pygame.image.load("images/bg4.png").convert()
    background_image = pygame.transform.scale(background_image, (window_width, window_height))

    # SHIP SPRITE IMAGES
    ship_images = [
        pygame.image.load("images/ship.png").convert_alpha(),
        pygame.image.load("images/ship.png").convert_alpha(),
        pygame.image.load("images/ship.png").convert_alpha(),
        pygame.image.load("images/ship.png").convert_alpha(),
        pygame.image.load("images/ship.png").convert_alpha()
    ]

    # CHANGE IMAGE SIZES TO FIT
    ship_images = [pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE)) for img in ship_images]

    # SHIP INTIAL PLACEMENT, DRAG DROP
    ships = [
        Ship("Carrier", 5, "horizontal", (COLS + 1, i * 2), ship_images[i]) for i in range(5)
    ]

    selected_ship = None
    dragging = False

    # GAME LOOP
    running = True
    while running:
        window.blit(background_image, (0, 0))  # BACKGROUND

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for ship in ships:
                    ship_rect = pygame.Rect(ship.position[0] * CELL_SIZE, ship.position[1] * CELL_SIZE, CELL_SIZE * ship.length if ship.orientation == 'horizontal' else CELL_SIZE, CELL_SIZE if ship.orientation == 'horizontal' else CELL_SIZE * ship.length)
                    if ship_rect.collidepoint(mouse_x, mouse_y):
                        selected_ship = ship
                        dragging = True
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_ship:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE
                    selected_ship.move((grid_x, grid_y))
                    if not selected_ship.is_within_bounds() or any(coord in ship.coordinates for ship in ships if ship != selected_ship for coord in selected_ship.coordinates):
                        selected_ship.move((COLS + 1, ships.index(selected_ship) * 2))  # RESET
                    selected_ship = None
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging and selected_ship:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
                selected_ship.move((grid_x, grid_y))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and selected_ship:
                    selected_ship.rotate()

        # DRAW
        draw_grid(window, ROWS, COLS, CELL_SIZE, offset=(CELL_SIZE, CELL_SIZE))
        draw_ships(window, ships, CELL_SIZE)

        pygame.display.flip()

if __name__ == "__main__":
    main()
