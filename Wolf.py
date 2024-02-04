from Animal import Animal

class Wolf(Animal):
    def __init__(self, world, position_y, position_x, age):
        super(Wolf, self).__init__('wolf', world, 4, 4, position_y, position_x, age)

    def breed(self, y, x):
        return Wolf(self.world, y, x, 0)

