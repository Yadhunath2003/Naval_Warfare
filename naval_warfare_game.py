from game_logic import GameBoard
from ai import AIPlayer

class NavalWarfareGame:
    def __init__(self, player_name, ai_difficulty="Medium"):
        # Initialize boards
        self.player_board = GameBoard()
        self.ai_board = GameBoard()

        # Initialize players
        self.human_player = player_name
        self.ai_player = AIPlayer(difficulty=ai_difficulty, num_boats=5)

        # Place AI ships
        self.ai_board.randomly_place_ships([5, 4, 3, 3, 2])  # Standard ship sizes

        # Game state
        self.current_turn = "Player"
        self.game_over = False
        self.winner = None

    def place_player_ships(self, ships):
        """
        Accepts a list of ships to place on the player's board.
        Each ship is a tuple of (length, orientation, start_position).
        """
        for length, orientation, start_position in ships:
            placed = self.player_board.place_ship(length, orientation, start_position)
            if not placed:
                raise ValueError(f"Invalid placement for ship of length {length} at {start_position}")

    def check_victory(self, board):
        """
        Check if all ships on a board are sunk.
        """
        for ship in board.ships:
            if any(board.grid[y][x] > 0 for x, y in ship["coordinates"]):  # Ship part still afloat
                return False
        return True

    def process_turn(self, x=None, y=None):
        if self.current_turn == "Player":
            if self.ai_board.grid[y][x] in [-1, 2]:  # Invalid move
                print("You already attacked this location. Try again.")
                return False

            hit = self.ai_board.attack(x, y)  # Updates AI's board
            print("Hit!" if hit else "Miss!")
            if self.check_victory(self.ai_board):
                self.game_over = True
                self.winner = "Player"
                return True

            # Switch to AI's turn
            self.current_turn = "AI"

        elif self.current_turn == "AI":
            # AI selects a move
            ai_x, ai_y = self.ai_player.make_move(self.player_board)  # AI chooses where to attack
            hit = self.player_board.attack(ai_x, ai_y)  # AI attacks the player's board
            print(f"AI attacks ({ai_x}, {ai_y}): {'Hit!' if hit else 'Miss!'}")

            if self.check_victory(self.player_board):
                self.game_over = True
                self.winner = "AI"
                return True

            # Switch back to Player's turn
            self.current_turn = "Player"

