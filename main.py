import pygame
from game_state import GameState, title_screen, game_mode, ai_mode, select_number_of_boats, get_selectedAIMode
from shipplacement import ship_placement_main
from player import Player
from naval_warfare_game import GamePlay
from frontend_game_board import game_loop

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

        elif game_state in [GameState.HUMAN]:
            # Step 1: Select the number of boats
            selected_boats = select_number_of_boats(screen)
            selected_ai_mode = get_selectedAIMode()
            print(f"Selected AI mode main: {selected_ai_mode}")  # Debugging output

            # AI Mode selected
            if selected_ai_mode > 0:
                if isinstance(selected_boats, GameState):
                    game_state = selected_boats  # Transition to the selected game state
                    continue  # Skip further processing and loop back to handle new state

                if selected_boats > 0:  # Ensure the user selects a valid number of ships
                    # Step 2: Initialize Players
                    player1 = Player(name="Player 1")
                    ai_player = Player(name="AI")

                    print(f"Player 1 placing {selected_boats} ships...")
                    ship_placement_main(player1, selected_boats, is_player1=True)

                    print(f"AI is placing {selected_boats} ships...")
                    ship_placement_main(ai_player, selected_boats, is_player1=False)

                    print("Player 1's Board:")
                    player1.board.display_grid()

                    # Optional: Debugging AI board placement
                    print("AI's Board (Hidden in actual gameplay):")
                    ai_player.board.display_grid()

                    # Step 3: Transition to gameplay loop
                    print("Starting the game!")
                    game = GamePlay(player1, ai_player, mode="PvAI")
                    game_loop(game)

            # Player vs Player Mode
            elif selected_ai_mode <= 0:

                if isinstance(selected_boats, GameState):
                    game_state = selected_boats  # Transition to the selected game state
                    continue  # Skip further processing and loop back to handle new state

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

                    # Step 5: Transition to gameplay loop
                    mode = "PvAI" if game_state == GameState.AIMODE else "PvP"
                    game = GamePlay(player1, player2, mode=mode)
                    game_loop(game)

        pygame.display.flip()

if __name__ == "__main__":
    main()
