import pygame
from game_state import GameState, title_screen, game_mode, ai_mode, select_number_of_boats
from shipplacement import main as ship_placement_main
from player import Player

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

            if selected_boats > 0:  # Ensure the user selects a valid number of ships
                # Step 2: Initialize Players
                player1 = Player(name="Player 1")
                player2 = Player(name="Player 2")

                # Step 3: Player 1 places ships
                print(f"Player 1 placing {selected_boats} ships...")
                ship_placement_main(player1, selected_boats, is_player1=True)

                # Step 4: Player 2 places ships
                print(f"Player 2 placing {selected_boats} ships...")
                ship_placement_main(player2, selected_boats, is_player1=False)

                # Debugging: Display the boards
                print("Player 1's Board:")
                player1.board.display_grid()

                print("Player 2's Board:")
                player2.board.display_grid()

                # Step 5: Transition to the title screen or gameplay loop
                game_state = GameState.TITLE  # Placeholder: Redirect to title after placement

        pygame.display.flip()

if __name__ == "__main__":
    main()

