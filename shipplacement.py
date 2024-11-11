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