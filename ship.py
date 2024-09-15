class Ship:
    def __init__(self, size):
        self.size = size
        self.x = None
        self.y = None
        self.orientation = None

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_orientation(self, orientation):
        self.orientation = orientation
