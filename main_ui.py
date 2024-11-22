""" 
Programmer: Kemar Wilson
Date written: October 27, 2024
"""
import random
import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
import sys

from shipplacement import Ship, draw_grid, draw_ships, create_game_logic, ROWS, COLS, CELL_SIZE

# Define color constants for UI elements
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
RED = (255, 0, 0)    # Color for a hit
GREEN = (0, 255, 0)  # Color for a miss
CELL_SIZE = 30  # Smaller cell size for better grid alignment


ships = 0

# Load background images for different game screens
bg = pygame.image.load("images/bg.png")
bg2 = pygame.image.load("images/bg2.png")
bg3 = pygame.image.load("images/bg3.png")
bg4 = pygame.image.load("images/bg4.png")
bg5 = pygame.image.load("images/bg5.png")

def display_text(screen, text, position, font_size=24, color=WHITE):
    """
    Renders text onto the Pygame screen.

    Args:
        screen: Pygame screen to render the text on.
        text: The string to display.
        position: Tuple (x, y) for the text position.
        font_size: Font size for the text.
        color: Color of the text.
    """
    font = pygame.font.SysFont("Courier", font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def transition_popup(screen, message, duration=3000):
    """
    Displays a transition popup message for a brief duration.

    Args:
        screen: Pygame screen to render the message.
        message: The text to display.
        duration: Duration in milliseconds to display the popup.
    """
    screen.fill(BLUE)
    display_text(screen, message, (300, 300), font_size=36)
    pygame.display.flip()
    pygame.time.wait(duration)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ 
    Create a surface with the specified text written on it.
    
    Args:
        text: The text to display.
        font_size: Size of the font.
        text_rgb: Color of the text in RGB format.
        bg_rgb: Background color in RGB format.
    
    Returns:
        A surface with the rendered text.
    """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True) # Load a system font
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb) # Render the text
    return surface.convert_alpha() # Return the surface with alpha transparency

class UIElement(Sprite):
    """ 
    Represents a user interface element that can be added to a display surface.
    
    Attributes:
        mouse_over: Indicates if the mouse is hovering over the element.
        images: Holds the default and highlighted images for the UI element.
        rects: Holds the rectangles for the default and highlighted images.
        action: Stores the action associated with the button when clicked.
    """

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        """
        Initializes the UI element with specified attributes.
        
        Args:
            center_position: Tuple (x, y) for the center position of the element.
            text: Text to display on the button.
            font_size: Font size for the text.
            bg_rgb: Background color for the button.
            text_rgb: Text color for the button.
            action: Action associated with this button (e.g., game state change).
        """
        self.mouse_over = False  # Initialize mouse_over state

        # Create images for the button in normal and highlighted states
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]  # Store button images
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]  # Create rectangles for the button images

        self.action = action  # Store the action associated with the button
        super().__init__()  # Initialize the base Sprite class

    @property
    def image(self):
        """ Returns the image to be drawn, based on mouse hover state. """
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        """ Returns the rectangle for the image to be drawn, based on mouse hover state. """
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ 
        Updates the mouse_over state and returns the button's action if clicked.
        
        Args:
            mouse_pos: Current position of the mouse.
            mouse_up: Indicates if the mouse button was released.
        """
        if self.rect.collidepoint(mouse_pos):  # Check if the mouse is over the button
            self.mouse_over = True  # Set mouse_over to True
            if mouse_up:  # If the mouse button is released
                return self.action  # Return the associated action
        else:
            self.mouse_over = False  # Reset mouse_over if not hovering

    def draw(self, surface):
        """ Draws the UI element onto the given surface. 
        
        Args:
            surface: The surface onto which the UI element will be drawn.
        """
        surface.blit(self.image, self.rect)  # Draw the current image at its rectangle position

def main():
    """ Main function to initialize pygame and manage game states. """
    pygame.init()  # Initialize all imported pygame modules

    screen = pygame.display.set_mode((1000, 700))  # Wider window
  # Set the display window size
    game_state = GameState.TITLE  # Initialize the game state to TITLE

    while True:  # Main game loop
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)  # Display title screen and get new state

        if game_state == GameState.NEWGAME:
            game_state = game_mode(screen)  # Start a new game mode
            
        if game_state == GameState.AIMODE:
            game_state = ai_mode(screen)  # Start AI mode
        
        if game_state == GameState.HUMAN:
            # Call the human_mode function and return to TITLE after it ends
            human_mode(screen)
            game_state = GameState.TITLE  # Return to title screen after the game ends

        if game_state == GameState.EASYSHIPS:
            game_state = human_mode(screen)  # Start AI easy mode
        
        if game_state == GameState.MEDIUMSHIPS:
            game_state = human_mode(screen)  # Start AI medium mode
        
        if game_state == GameState.HARDSHIPS:
            game_state = human_mode(screen)  # Start AI hard mode

        if game_state == GameState.QUIT:
            pygame.quit()  # Quit pygame and exit
            return


def title_screen(screen):
    """ Display the title screen with start and quit buttons. """
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,  # Action for starting a new game
    )
    quit_btn = UIElement(
        center_position=(400, 440),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,  # Action for quitting the game
    )

    buttons = [start_btn, quit_btn]  # Store buttons in a list

    while True:  # Main loop for the title screen
        mouse_up = False
        for event in pygame.event.get():  # Check for events
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True  # Mouse button released
        screen.blit(bg, (0, 0))  # Draw background image

        for button in buttons:  # Update and draw each button
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)  # Update button state
            if ui_action is not None:  # If the button was clicked
                return ui_action  # Return the action associated with the button
            button.draw(screen)  # Draw the button

        pygame.display.flip()  # Update the display

def game_mode(screen):
    """ Display the game mode selection with buttons. """
    return_btn = UIElement(
        center_position=(80, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="RETURN",
        action=GameState.TITLE,  # Action to return to the title screen
    )
    
    ai_btn = UIElement(
        center_position=(400, 370),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="AI",
        action=GameState.AIMODE,  # Action to enter AI mode
    )
    human_btn = UIElement(
        center_position=(400, 410),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="HUMAN",
        action=GameState.HUMAN,  # Action to enter human mode
    )

    buttons = [ai_btn, human_btn]  # Store the game mode buttons in a list


    while True:  # Main loop for game mode screen
        mouse_up = False
        for event in pygame.event.get():  # Check for events
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True  # Mouse button released
        screen.blit(bg2, (0, 0))  # Draw background for game mode

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)  # Update return button state
        if ui_action is not None:  # If the return button was clicked
            return ui_action  # Return the action associated with the button
        return_btn.draw(screen)  # Draw the return button
        
        for button in buttons:  # Update and draw each game mode button
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)  # Update button state
            if ui_action is not None:  # If a button was clicked
                return ui_action  # Return the action associated with the button
            button.draw(screen)  # Draw the button

        pygame.display.flip() 
def ai_mode(screen):
    """ Display AI difficulty options with buttons. """
    return_btn = UIElement(
        center_position=(80, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="RETURN",
        action=GameState.NEWGAME,  # Action to return to the game mode
    )
    
    easy_btn = UIElement(
        center_position=(400, 340),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="EASY",
        action=GameState.EASYSHIPS,  # Action to enter human mode (for now, needs to be updated)
    )
    medium_btn = UIElement(
        center_position=(400, 380),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="MEDIUM",
        action=GameState.MEDIUMSHIPS,  # Action to enter human mode (for now, needs to be updated)
    )
    hard_btn = UIElement(
        center_position=(400, 420),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="HARD",
        action=GameState.HARDSHIPS,  # Action to enter human mode (for now, needs to be updated)
    )
    
    buttons = [easy_btn, medium_btn, hard_btn]  # Store difficulty buttons in a list
    
    while True:  # Main loop for AI mode screen
        mouse_up = False
        for event in pygame.event.get():  # Check for events
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True  # Mouse button released
        screen.blit(bg3, (0, 0))  # Draw background for AI mode
        
        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)  # Update return button state
        if ui_action is not None:  # If the return button was clicked
            return ui_action  # Return the action associated with the button
        return_btn.draw(screen)  # Draw the return button
        
        for button in buttons:  # Update and draw each difficulty button
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)  # Update button state
            if ui_action is not None:  # If a button was clicked
                return ui_action  # Return the action associated with the button
            button.draw(screen)  # Draw the button
        
        pygame.display.flip()  # Update the display

def human_mode(screen):
    """
    Manages the game loop for human vs. human mode.
    """

    # Initialize grids and scores
    player1_grid = create_game_logic(ROWS, COLS)
    player2_grid = create_game_logic(ROWS, COLS)
    player1_score = [0, 0]  # [Hits, Misses]
    player2_score = [0, 0]  # [Hits, Misses]

    # Randomly place ships for demonstration purposes
    for _ in range(5):
        player1_grid[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)] = 1
        player2_grid[random.randint(0, ROWS - 1)][random.randint(0, COLS - 1)] = 1

    current_player = 1  # Player 1 starts the game
    print(f"Current player: {current_player}")

    while True:
        if current_player == 1:
            # Player 1 attacks Player 2
            attack_page(screen, player1_grid, player2_grid, player1_score, player2_score, current_player)
            # Check if Player 1 wins
            if all(cell != 1 for row in player2_grid for cell in row):
                transition_popup(screen, "Player 1 Wins!", 3000)
                break
            # Transition to Player 2's turn
            transition_popup(screen, "Player 2's Turn")
            current_player = 2
        else:
            # Player 2 attacks Player 1
            attack_page(screen, player2_grid, player1_grid, player2_score, player1_score, current_player)
            # Check if Player 2 wins
            if all(cell != 1 for row in player1_grid for cell in row):
                transition_popup(screen, "Player 2 Wins!", 3000)
                break
            # Transition to Player 1's turn
            transition_popup(screen, "Player 1's Turn")
            current_player = 1



def attack_page(screen, player_grid, opponent_grid, player_score, opponent_score, current_player):
    GRID_WIDTH = COLS * CELL_SIZE
    GRID_HEIGHT = ROWS * CELL_SIZE
    screen_width = 800
    spacing = 50

    player_grid_offset = (spacing, spacing)
    opponent_grid_offset = (screen_width - GRID_WIDTH - 2 * spacing, spacing)

    running = True
    text_message = ""

    while running:
        screen.fill(BLUE)

        # Debug: Highlight grid areas
        pygame.draw.rect(
            screen, (255, 255, 255),  # White border
            (opponent_grid_offset[0], opponent_grid_offset[1], GRID_WIDTH, GRID_HEIGHT), 2
        )
        pygame.draw.rect(
            screen, (255, 255, 255),  # White border
            (player_grid_offset[0], player_grid_offset[1], GRID_WIDTH, GRID_HEIGHT), 2
        )

        # Draw Player Grid
        draw_grid(screen, ROWS, COLS, CELL_SIZE, offset=player_grid_offset)
        for x in range(ROWS):
            for y in range(COLS):
                if player_grid[x][y] == 1:
                    pygame.draw.rect(
                        screen, (0, 0, 255),
                        (player_grid_offset[0] + y * CELL_SIZE, player_grid_offset[1] + x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
                elif player_grid[x][y] == 2:
                    pygame.draw.circle(
                        screen, GREEN,
                        (player_grid_offset[0] + y * CELL_SIZE + CELL_SIZE // 2,
                         player_grid_offset[1] + x * CELL_SIZE + CELL_SIZE // 2),
                        10
                    )
                elif player_grid[x][y] == 3:
                    pygame.draw.circle(
                        screen, RED,
                        (player_grid_offset[0] + y * CELL_SIZE + CELL_SIZE // 2,
                         player_grid_offset[1] + x * CELL_SIZE + CELL_SIZE // 2),
                        10
                    )

        # Draw Opponent Grid
        draw_grid(screen, ROWS, COLS, CELL_SIZE, offset=opponent_grid_offset)
        for x in range(ROWS):
            for y in range(COLS):
                if opponent_grid[x][y] == 2:  # Miss
                    pygame.draw.circle(
                        screen, GREEN,
                        (opponent_grid_offset[0] + y * CELL_SIZE + CELL_SIZE // 2,
                         opponent_grid_offset[1] + x * CELL_SIZE + CELL_SIZE // 2),
                        10
                    )
                elif opponent_grid[x][y] == 3:  # Hit
                    pygame.draw.circle(
                        screen, RED,
                        (opponent_grid_offset[0] + y * CELL_SIZE + CELL_SIZE // 2,
                         opponent_grid_offset[1] + x * CELL_SIZE + CELL_SIZE // 2),
                        10
                    )

        # Display grids and messages
        display_text(screen, "Your Base", (player_grid_offset[0] + GRID_WIDTH // 2 - 50, 20))
        display_text(screen, "Opponent Base", (opponent_grid_offset[0] + GRID_WIDTH // 2 - 50, 20))
        if text_message:
            display_text(screen, text_message, (screen_width // 2 - 100, GRID_HEIGHT + 100), font_size=24)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x = (x - opponent_grid_offset[0]) // CELL_SIZE
                grid_y = (y - opponent_grid_offset[1]) // CELL_SIZE

                print(f"Mouse clicked at: ({x}, {y}) -> Grid position: ({grid_x}, {grid_y})")

                if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
                    if opponent_grid[grid_y][grid_x] == 0:  # Miss
                        opponent_grid[grid_y][grid_x] = 2
                        player_score[1] += 1
                        text_message = "Miss!"
                    elif opponent_grid[grid_y][grid_x] == 1:  # Hit
                        opponent_grid[grid_y][grid_x] = 3
                        player_score[0] += 1
                        text_message = "Hit!"
                    print(f"Updated opponent_grid: {opponent_grid}")
                    pygame.time.wait(1000)  # Pause for clarity
                    running = False
                else:
                    text_message = "Click inside the opponent's grid!"

        if all(cell != 1 for row in opponent_grid for cell in row):
            display_text(screen, f"Player {current_player} Wins!", (300, 300), font_size=36, color=RED)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False







class GameState(Enum):
    QUIT = -1            # Enumeration for quitting the game
    TITLE = 0            # Enumeration for title screen state
    NEWGAME = 1          # Enumeration for starting a new game
    AIMODE = 2           # Enumeration for AI mode
    HUMAN = 3            # Enumeration for human player mode
    EASYSHIPS = 4
    MEDIUMSHIPS = 5
    HARDSHIPS = 6
    

if __name__ == "__main__":
    main();  # Entry point of the program, starts the main function.