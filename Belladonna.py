from Plant import Plant

class Belladonna(Plant):
    def __init__(self, world, position_y, position_x, age):
        super(Belladonna, self).__init__('belladonna', world, 99, 0, position_y, position_x, age)

    def breed(self, y, x):
        return Belladonna(self.world, y, x, 0)

    def collision(self, atacker, y, x):
        self.world.comment_list.append(f"{atacker.specie_enum} eats belladonna and dies")
        self.world.remove_organism(self)  # belladonna is eaten
        self.world.grid[y][x] = None

        self.world.remove_organism(atacker)
        self.world.grid[atacker.position_y][atacker.position_x] = None
