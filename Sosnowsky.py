from Plant import Plant

class Sosnowsky(Plant):
    def __init__(self, world, position_y, position_x, age):
        super(Sosnowsky, self).__init__('sosnowsky', world, 10, 0, position_y, position_x, age)

    def breed(self, y, x):
        return Sosnowsky(self.world, y, x, 0)

    def collision(self, atacker, y, x):
        if atacker.specie_enum != 'cyber_sheep':
            self.world.comment_list.append(f"{atacker.specie_enum} eats sosnowsky and dies")
            self.world.remove_organism(self)
            self.world.grid[y][x] = None

            self.world.remove_organism(atacker)
            self.world.grid[atacker.position_y][atacker.position_x] = None
        else:
            self.world.remove_organism(self)
            self.world.grid[y][x] = None

            self.world.grid[y][x] = atacker
            self.world.grid[atacker.prev_y][atacker.prev_x] = None