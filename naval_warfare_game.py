from game_logic import GameBoard
from player import Player

class GamePlay:
    def __init__(self, player1, player2, mode="PvP"):
        """
        Initialize the gameplay logic.
        mode: "PvP" for Player vs. Player, "PvAI" for Player vs. AI.
        """
        self.player1 = player1
        self.player2 = player2
        self.mode = mode
        self.current_player = player1
        self.opponent = player2
        self.winner = None
        self.game_over = False

    def attack(self, x, y):
        """
        Handle an attack on the opponent's board.
        """
        # Check if the cell has already been attacked
        if self.opponent.board.grid[y][x] in ["X", "O"]:
            return {"valid": False, "message": "Cell already attacked. Try again."}

        # Check for hit or miss
        if self.opponent.board.grid[y][x] != 0:  # Hit
            self.opponent.board.grid[y][x] = "X"
            self.current_player.hits.append((x, y))
            hit = True
        else:  # Miss
            self.opponent.board.grid[y][x] = "O"
            self.current_player.misses.append((x, y))
            hit = False

        return {"valid": True, "hit": hit, "message": "Hit!" if hit else "Miss!"}

    def check_victory(self):
        """
        Check if the opponent has lost all their ships.
        """
        for ship in self.opponent.board.ships:
            if any(self.opponent.board.grid[y][x] > 0 for x, y in ship["coordinates"]):
                return False
        self.winner = self.current_player.name
        self.game_over = True
        return True

    def switch_turns(self):
        """
        Switch the current player and opponent.
        """
        self.current_player, self.opponent = self.opponent, self.current_player

    def process_turn(self, x=None, y=None):
        """
        Process the current player's turn.
        For AI, make a move automatically.
        """
        if self.mode == "PvAI" and self.current_player == self.player2:
            # AI's turn
            x, y = self.player2.ai_player.make_move(self.player1.board)

        # Validate the move coordinates
        if x is None or y is None:
            return {"valid": False, "message": "Invalid coordinates."}

        # Perform the attack
        attack_result = self.attack(x, y)
        if not attack_result["valid"]:
            return attack_result

        # Check if the game is over
        if self.check_victory():
            return {"valid": True, "winner": self.winner, "message": f"{self.winner} wins!"}

        # Switch turns if the game isn't over
        self.switch_turns()
        return attack_result

    def reset_game(self):
        """
        Reset the game state for a new match.
        """
        self.current_player = self.player1
        self.opponent = self.player2
        self.winner = None
        self.game_over = False
        self.player1.board = GameBoard()
        self.player2.board = GameBoard()
from game_logic import GameBoard
from player import Player

class GamePlay:
    def __init__(self, player1, player2, mode="PvP"):
        """
        Initialize the gameplay logic.
        mode: "PvP" for Player vs. Player, "PvAI" for Player vs. AI.
        """
        self.player1 = player1
        self.player2 = player2
        self.mode = mode
        self.current_player = player1
        self.opponent = player2
        self.winner = None
        self.game_over = False

    def attack(self, x, y):
        """
        Handle an attack on the opponent's board.
        """
        # Check if the cell has already been attacked
        if self.opponent.board.grid[y][x] in ["X", "O"]:
            return {"valid": False, "message": "Cell already attacked. Try again."}

        # Check for hit or miss
        if self.opponent.board.grid[y][x] != 0:  # Hit
            self.opponent.board.grid[y][x] = "X"
            self.current_player.hits.append((x, y))
            hit = True
        else:  # Miss
            self.opponent.board.grid[y][x] = "O"
            self.current_player.misses.append((x, y))
            hit = False

        return {"valid": True, "hit": hit, "message": "Hit!" if hit else "Miss!"}

    def check_victory(self):
        """
        Check if the opponent has lost all their ships.
        """
        for ship in self.opponent.board.ships:
            if any(self.opponent.board.grid[y][x] > 0 for x, y in ship["coordinates"]):
                return False
        self.winner = self.current_player.name
        self.game_over = True
        return True

    def switch_turns(self):
        """
        Switch the current player and opponent.
        """
        self.current_player, self.opponent = self.opponent, self.current_player

    def process_turn(self, x=None, y=None):
        """
        Process the current player's turn.
        For AI, make a move automatically.
        """
        if self.mode == "PvAI" and self.current_player == self.player2:
            # AI's turn
            x, y = self.player2.ai_player.make_move(self.player1.board)

        # Validate the move coordinates
        if x is None or y is None:
            return {"valid": False, "message": "Invalid coordinates."}

        # Perform the attack
        attack_result = self.attack(x, y)
        if not attack_result["valid"]:
            return attack_result

        # Check if the game is over
        if self.check_victory():
            return {"valid": True, "winner": self.winner, "message": f"{self.winner} wins!"}

        # Switch turns if the game isn't over
        self.switch_turns()
        return attack_result

    def reset_game(self):
        """
        Reset the game state for a new match.
        """
        self.current_player = self.player1
        self.opponent = self.player2
        self.winner = None
        self.game_over = False
        self.player1.board = GameBoard()
        self.player2.board = GameBoard()
