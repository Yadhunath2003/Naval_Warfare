from player import Player
from ship import Ship

class Game:

    def __init__(self):
        # (TODO) set the fleet type for the game (1 ship fleet, 2 ship fleet, etc.) // Anakha Completed 9/12
        self.fleet_options = {
            1: [Ship(1)],
            2: [Ship(1), Ship(2)],
            3: [Ship(1), Ship(2), Ship(3)],
            4: [Ship(1), Ship(2), Ship(3), Ship(4)],
            5: [Ship(1), Ship(2), Ship(3), Ship(4), Ship(5)]
        }
        self.fleet_type = None

        


    # method to run game, position boats, loop, turn alternating until win
    def play(self):
        # prompt for fleet type
        chosen_fleet = None
        while chosen_fleet is None:
            try:
                fleet_type = int(input("Choose a fleet type (1, 2, 3, 4, or 5): "))
                if fleet_type in self.fleet_options:
                    chosen_fleet = self.fleet_options[fleet_type]
                    chosen_fleet_copy = self.fleet_options[fleet_type]
                    self.fleet_type = fleet_type
                else:
                    print("Invalid fleet type. Please choose 1, 2, 3, 4, or 5.")
            except ValueError:
                print("Invalid input. Please enter a number (1, 2, 3, 4, or 5).")
            
        self.players = [Player("Player 1", chosen_fleet), Player("Player 2", chosen_fleet_copy)]

        # set opponent
        self.players[0].set_opponent(self.players[1])
        self.players[1].set_opponent(self.players[0])

        # place fleets
        self.players[0].place_fleet()
        self.players[1].place_fleet()

        input("All ships in place. Players...are you ready? Press enter to begin the battle!")

        # game loop
        game_over = False # will handle take_turn() boolean result (True if game won, False if game continues)
        current_player_index = 0 # keeps track of which players turn it is

        while not game_over:
            current_player = self.players[current_player_index] # start with players[0]

            game_over = current_player.take_turn(self.fleet_type) # call take turn and assign to game_over

            if not game_over: # continue game if take_turn() returns false
                current_player_index = 1 - current_player_index # switch to next player's turn
        
        print(f"Game over... {self.players[current_player_index].player_name} wins!")




