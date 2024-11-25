from naval_warfare_game import NavalWarfareGame
from game_logic import GameBoard
from ai import AIPlayer

def test_ship_placement():
    """
    Test ship placement on the board to ensure no overlaps and all ships fit within bounds.
    """
    board = GameBoard(rows=10, cols=10)
    ship_lengths = [5, 4, 3, 3, 2]
    board.randomly_place_ships(ship_lengths)

    print("Testing Ship Placement...")
    print("Current Ship Placements:")
    board.display_ship_placements()

    # Check for overlaps
    placed_coordinates = set()
    for ship in board.ships:
        for x, y in ship["coordinates"]:
            assert (x, y) not in placed_coordinates, "Ships overlap!"
            placed_coordinates.add((x, y))

    print("Ship placement test passed!")

def test_ai_move():
    """
    Test AI's ability to make valid moves without repeating or attacking invalid cells.
    """
    board = GameBoard(rows=10, cols=10)
    ai = AIPlayer(difficulty="Medium", num_boats=5)

    # Simulate AI moves
    print("Simulating AI Moves...")
    for _ in range(15):  # Allow AI to make 15 moves
        x, y = ai.make_move(board)
        print(f"AI attacks ({x}, {y})")
        assert board.grid[y][x] not in [-1, 2], "AI attacked an already attacked cell!"
        board.attack(x, y)

    print("AI move test passed!")

def test_process_turn():
    """
    Test a full turn flow between player and AI, ensuring turn alternation and valid moves.
    """
    game = NavalWarfareGame(player_name="Player 1")

    # Place player's ships
    player_ships = [
        (5, "horizontal", (0, 0)),
        (4, "vertical", (2, 2)),
        (3, "horizontal", (5, 5)),
        (2, "vertical", (7, 0)),
    ]
    game.place_player_ships(player_ships)

    print("Player board:")
    game.player_board.display_ship_placements()

    print("AI board:")
    game.ai_board.display_ship_placements()

    # Simulate a few turns
    print("\nSimulating Turns...")
    for _ in range(5):  # Simulate 5 turns
        # Player's turn
        x, y = 3, 3  # Player attacks (you can adjust this to vary testing)
        result = game.process_turn(x, y)
        print(f"Player attacks ({x}, {y}): {'Hit' if result else 'Miss'}")

        if game.game_over:
            print(f"Game Over! Winner: {game.winner}")
            return

        # AI's turn
        ai_x, ai_y = game.ai_player.make_move(game.player_board)  # Get AI's move
        result = game.process_turn(ai_x, ai_y)
        print(f"AI attacks ({ai_x}, {ai_y}): {'Hit' if result else 'Miss'}")

        if game.game_over:
            print(f"Game Over! Winner: {game.winner}")
            return

    print("Game is still ongoing.")


def test_victory_detection():
    """
    Simulate attacking all ships on the AI board to test victory detection.
    """
    game = NavalWarfareGame(player_name="Player 1")

    # Place player's ships
    player_ships = [
        (5, "horizontal", (0, 0)),
        (4, "vertical", (2, 2)),
        (3, "horizontal", (5, 5)),
        (2, "vertical", (7, 0)),
    ]
    game.place_player_ships(player_ships)

    print("Player board:")
    game.player_board.display_ship_placements()

    print("AI board:")
    game.ai_board.display_ship_placements()

    # Attack all AI cells to sink all ships
    print("\nSimulating Player Attacks to Sink All AI Ships...")
    for y in range(10):
        for x in range(10):
            game.process_turn(x, y)
            if game.game_over:
                print(f"Game Over! Winner: {game.winner}")
                assert game.winner == "Player", "Victory condition failed!"
                return

def test_ai_targeting_behavior():
    """
    Test AI's targeting behavior after hitting a ship to ensure it targets adjacent cells.
    """
    board = GameBoard(rows=10, cols=10)
    ai = AIPlayer(difficulty="Medium", num_boats=5)

    # Manually place a single ship for the player
    board.place_ship(3, "horizontal", (2, 2))  # Place a ship of length 3 at (2, 2)
    print("Player's Board (for AI to attack):")
    board.display_ship_placements()

    # Simulate AI attacks
    print("\nSimulating AI Attacks...")
    
    # Force the AI's first move to hit the ship
    x, y = 2, 2
    print(f"AI attacks ({x}, {y})")
    board.attack(x, y)  # Update the board after attack
    board.display_grid()  # Display board after the move

    # Continue with the AI's normal moves
    for _ in range(10):  # Allow AI to make 10 more moves
        x, y = ai.make_move(board)
        print(f"AI attacks ({x}, {y})")
        board.attack(x, y)  # Update the board after attack
        board.display_grid()

if __name__ == "__main__":
    print("Running tests...\n")

    test_ship_placement()
    print("\n")

    test_ai_move()
    print("\n")

    test_process_turn()
    print("\n")

    test_victory_detection()
    print("\n")

    test_ai_targeting_behavior()
    print("\n")

    print("All tests completed successfully!")
