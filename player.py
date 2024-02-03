from helper import BLACK, WHITE
class Player:
    def __init__(self, player_number):
        self.number = player_number
        self.color = BLACK if player_number == 1 else WHITE

    @property
    def symbol(self):
        return 2 if self.number == 1 else 3
    def opp_symbol(self):
        return 3 if self.number == 1 else 2
