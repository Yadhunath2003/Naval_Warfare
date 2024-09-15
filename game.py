from player.py import Player

class Game:

    def __init__(self):
        # (TODO) set the fleet type for the game (1 ship fleet, 2 ship fleet, etc.)
        # these fleets should be the same but can't use the same variable because of Python list weirdness
        fleet1 = []
        fleet2 = []
        # create players
        self.players = [Player("Player 1", fleet1), Player("Player 2", fleet2)]
        
        # set opponent
    

    # method to run game, position boats, loop, turn alternating until win
    def play(self):
        # use methods from player (take_turn)
        pass

