import pygame
from game_state import GameState, title_screen, game_mode, ai_mode, select_number_of_boats
from shipplacement import main as ship_placement_main

def main():
    """ Main function to initialize pygame and manage game states. """
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Set the display window size
    game_state = GameState.TITLE  # Initialize the game state to TITLE

    while game_state != GameState.QUIT:  # Main game loop
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        elif game_state == GameState.NEWGAME:
            game_state = game_mode(screen)

        elif game_state == GameState.AIMODE:
            game_state = ai_mode(screen)

        elif game_state in [GameState.HUMAN, GameState.EASYSHIPS, GameState.MEDIUMSHIPS, GameState.HARDSHIPS]:
            # Step 1: Select the number of boats
            selected_boats = select_number_of_boats(screen)

            if selected_boats > 0:  # Ensure the user selects a valid number of boats
                # Step 2: Transition to the ship placement page
                ship_placement_main()

                # Once ship placement is done, return to title or proceed further
                game_state = GameState.TITLE  # Placeholder: Redirect to title after placement

        pygame.display.flip()

if __name__ == "__main__":
    main()

