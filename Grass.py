from Plant import Plant

class Grass(Plant):
    def __init__(self, world, position_y, position_x, age):
        super(Grass, self).__init__('grass', world, 0, 0, position_y, position_x, age)

    def breed(self, y, x):
        return Grass(self.world, y, x, 0)