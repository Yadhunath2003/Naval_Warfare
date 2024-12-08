import pygame
import sys
from enum import Enum
from ui import UIElement  # Import the button class

# Define color constants for UI elements
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
global ships_selected

# Load background images for different game screens
bg = pygame.image.load("images/bg.png")
bg2 = pygame.image.load("images/bg2.png")
bg3 = pygame.image.load("images/bg3.png")
bg4 = pygame.image.load("images/bg4.png")
bg5 = pygame.image.load("images/bg5.png")

class GameState(Enum):
    QUIT = -1            # Enumeration for quitting the game
    TITLE = 0            # Enumeration for title screen state
    NEWGAME = 1          # Enumeration for starting a new game
    AIMODE = 2           # Enumeration for AI mode
    HUMAN = 3            # Enumeration for human player mode

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Create a surface with the specified text written on it. """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

def title_screen(screen):
    """ Display the title screen with start and quit buttons. """
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 440),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(bg, (0, 0))  # Draw the title background

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()
        
def get_selectedAIMode():
    global selectedAIMode
    return selectedAIMode

def game_mode(screen):
    """ Display the game mode selection with buttons. """
    return_btn = UIElement(
        center_position=(80, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="RETURN",
        action=GameState.TITLE,
    )

    ai_btn = UIElement(
        center_position=(400, 370),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="AI",
        action=GameState.AIMODE,
    )
    human_btn = UIElement(
        center_position=(400, 410),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="HUMAN",
        action=GameState.HUMAN,
    )

    buttons = [ai_btn, human_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(bg2, (0, 0))  # Draw the background for game mode

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

selectedAIMode = 0

def ai_mode(screen):
    """ Display AI difficulty options with buttons. """
    return_btn = UIElement(
        center_position=(80, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="RETURN",
        action=GameState.NEWGAME,
    )

    easy_btn = UIElement(
        center_position=(400, 340),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="EASY",
        action=1,
    )
    medium_btn = UIElement(
        center_position=(400, 380),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="MEDIUM",
        action=2,
    )
    hard_btn = UIElement(
        center_position=(400, 420),
        font_size=40,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="HARD",
        action=3,
    )

    buttons = [easy_btn, medium_btn, hard_btn]
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(bg3, (0, 0))  # Draw the background for AI mode

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                global selectedAIMode
                selectedAIMode = ui_action  # Store the user's selection
                print(f"Selected AI Mode: {selectedAIMode}")
                return GameState.HUMAN
            button.draw(screen)

        pygame.display.flip()

def human_mode(screen):
    """ Display the human player options with a return button. """
    return_btn = UIElement(
        center_position=(80, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="RETURN",
        action=GameState.NEWGAME,
    )
    
    # Human Mode Buttons (e.g., Button for ships, difficulty levels, etc.)
    # Just an example here, you can modify with your own game logic
    buttons = []  # Add your buttons here for human mode
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.blit(bg4, (0, 0))  # Draw the background for human mode
        
        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

def select_number_of_boats(screen):
    """Display the screen to select the number of boats and record the selection."""
    # Define the return button
    return_btn = UIElement(
        center_position=(80, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="RETURN",
        action=GameState.NEWGAME,
    )

    # Define buttons for selecting the number of boats
    buttons = [
        UIElement(
            center_position=(300 + i * 50, 450),
            font_size=40,
            bg_rgb=BLUE,
            text_rgb=WHITE,
            text=str(i + 1),
            action=i + 1,  # Return the number of boats selected
        )
        for i in range(5)
    ]

    # Variable to store the user's choice
    selected_number_of_boats = None

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        # Draw the background
        screen.blit(bg4, (0, 0))

        # Handle return button
        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action == GameState.NEWGAME:  # Check if return button was clicked
            return GameState.NEWGAME  # Return the NEWGAME state
        return_btn.draw(screen)

        # Handle boat selection buttons
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                selected_number_of_boats = ui_action  # Record the selection
                print(selected_number_of_boats)
                return selected_number_of_boats  # Return the selected number of boats
            button.draw(screen)

        # Update the display
        pygame.display.flip()
