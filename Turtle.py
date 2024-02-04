from Animal import Animal

class Turtle(Animal):
    def __init__(self, world, position_y, position_x, age):
        super(Turtle, self).__init__('turtle', world, 2, 1, position_y, position_x, age)

    def breed(self, y, x):
        return Turtle(self.world, y, x, 0)

    def collision(self, atacker, y, x):
        if atacker.strength < 5:
            self.world.comment_list.append(f"turtle reflects attack of {atacker.specie_enum} ")
        else:
            self.world.comment_list.append(f"turle is defeated by {atacker.specie_enum}")
            self.world.remove_organism(self)
            self.world.grid[y][x] = None
            atacker.set_yx(y, x)
            self.world.grid[y][x] = atacker
            self.world.grid[atacker.prev_y][atacker.prev_y] = None
