"""
UI.py
A simple graphical user interface for a naval warfare game with multiple screens, including a title screen, mode selection screen, and a placeholder gameplay screen.

Programmer: Kemar Wilson and Sanketh Reddy
Date Created: 27 October 2024
Last Revised: 27 October 2024
Revision Author: Sanketh Reddy

Summary:
- Initial creation of UI with title screen and button navigation.
- Added background image and hover effects on buttons.
- Modified button styles to remove background color on title screen for specific buttons.
- Updated font to Arial for cross-platform compatibility.

Preconditions:
- Pygame library must be installed.
- Background image ('bg.png') must be present in the 'images' directory.
- This code assumes a basic familiarity with Python and Pygame for the user to understand modifications.

Acceptable Inputs:
- Mouse clicks for button interactions.
- Image file format for the background (e.g., PNG).

Unacceptable Inputs:
- Non-standard font names or missing images (may lead to FileNotFoundError or default font fallback).

Postconditions:
- Successfully loads title screen, mode selection screen, and gameplay placeholder screen.
- Allows users to navigate between screens via mouse clicks.

Return Values:
- None. The program runs in an event loop until explicitly closed.

Error and Exception Conditions:
- FileNotFoundError: Occurs if 'bg.png' is missing from the specified directory.
- pygame.error: Could occur if display mode is set incorrectly or other Pygame resources are missing.

Side Effects:
- Opens a graphical window and utilizes system resources for display and processing.
- Event handling can modify internal state based on user interactions.

Invariants:
- Game state values remain within predefined Enum states.
- Screen dimensions and color values remain consistent throughout runtime.

Known Faults:
- Currently None.
"""

import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum

# Define color constants for consistent UI appearance
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

# Load Background Image
# Preconditions: 'bg.png' file exists in the 'images' directory.
# Postconditions: Image is loaded as a background.
bg = pygame.image.load("images/bg.png")

def create_surface_with_text(text, font_size, text_rgb, bg_rgb=None):
    """ 
    Returns a surface with text rendered on it. 
    Preconditions: Font should be available on the system.
    Postconditions: Returns a Pygame surface with rendered text.
    
    Parameters:
    - text: str - Text to render on the surface.
    - font_size: int - Size of the font.
    - text_rgb: tuple - RGB color for the text.
    - bg_rgb: tuple (optional) - RGB color for background; if None, text is transparent.

    Returns:
    - surface: Pygame surface with rendered text.
    """
    font = pygame.freetype.SysFont("Arial", font_size, bold=True)
    # Render text with optional background color
    if bg_rgb:
        surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    else:
        surface, _ = font.render(text=text, fgcolor=text_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    """ 
    A UI element representing a clickable button with hover effects.
    
    Parameters:
    - center_position: tuple - Coordinates for the center of the button.
    - text: str - Text displayed on the button.
    - font_size: int - Font size of the text.
    - text_rgb: tuple - RGB color for the text.
    - action: Enum - Game state to transition to upon clicking.
    - bg_rgb: tuple (optional) - RGB color for background; if None, button is transparent.
    """
    def __init__(self, center_position, text, font_size, text_rgb, action=None, bg_rgb=None):
        # Initialize button states
        self.mouse_over = False  # Tracks if the mouse is over the button

        # Create button images for normal and hover states
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )
        highlighted_image = create_surface_with_text(
            text=text, font_size=int(font_size * 1.2), text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # Store images and rectangles for rendering
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]
        self.action = action  # State transition upon click
        super().__init__()

    @property
    def image(self):
        """ Returns current image based on hover state. """
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        """ Returns current rectangle based on hover state. """
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        """ 
        Update hover state and check for click actions.
        
        Parameters:
        - mouse_pos: tuple - Current mouse position.
        - mouse_up: bool - True if the left mouse button was released.
        
        Returns:
        - action (Enum): The action associated with the button if clicked.
        """
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action  # Trigger button's action if clicked
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws the button on the provided surface. """
        surface.blit(self.image, self.rect)

class GameState(Enum):
    """ Enum representing possible game states. """
    QUIT = -1
    TITLE = 0
    MODE_SELECTION = 1
    NEWGAME = 2

def main():
    """ Main game loop controlling state transitions. """
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Set display size
    game_state = GameState.TITLE  # Initial game state

    while True:
        # Check the current game state and call the relevant screen function
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)
        elif game_state == GameState.MODE_SELECTION:
            game_state = mode_selection_screen(screen)
        elif game_state == GameState.NEWGAME:
            game_state = play_level(screen)
        elif game_state == GameState.QUIT:
            pygame.quit()  # Exit the game
            return

def title_screen(screen):
    """ Displays the title screen with 'Start' and 'Quit' buttons. """
    start_btn = UIElement(center_position=(400, 400), font_size=35, text_rgb=WHITE, text="Start", action=GameState.MODE_SELECTION, bg_rgb=None)
    quit_btn = UIElement(center_position=(400, 440), font_size=35, text_rgb=WHITE, text="Quit", action=GameState.QUIT, bg_rgb=None)
    buttons = [start_btn, quit_btn]

    while True:
        # Event handling for quit and mouse click
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.blit(bg, (0, 0))  # Draw background

        # Draw each button and check for actions
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

def mode_selection_screen(screen):
    """ Displays the mode selection screen with buttons for game modes. """
    human_vs_human_btn = UIElement(center_position=(400, 300), font_size=30, text_rgb=WHITE, bg_rgb=BLUE, text="Human vs Human", action=GameState.NEWGAME)
    human_vs_ai_btn = UIElement(center_position=(400, 350), font_size=30, text_rgb=WHITE, bg_rgb=BLUE, text="Human vs AI", action=GameState.NEWGAME)
    back_btn = UIElement(center_position=(400, 400), font_size=30, text_rgb=WHITE, bg_rgb=BLUE, text="Back to Main Menu", action=GameState.TITLE)
    buttons = [human_vs_human_btn, human_vs_ai_btn, back_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.blit(bg, (0, 0))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

def play_level(screen):
    """ Placeholder screen for gameplay with a 'Return to Main Menu' button. """
    return_btn = UIElement(center_position=(140, 570), font_size=20, text_rgb=WHITE, bg_rgb=BLUE, text="Return to Main Menu", action=GameState.TITLE)

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(BLUE)

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
