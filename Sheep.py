from Animal import Animal

class Sheep(Animal):
    def __init__(self, world, position_y, position_x, age):
        super(Sheep, self).__init__('sheep', world, 4, 4, position_y, position_x, age)

    def breed(self, y, x):
        return Sheep(self.world, y, x, 0)