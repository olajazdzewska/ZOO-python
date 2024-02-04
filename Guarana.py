from Plant import Plant

class Guarana(Plant):
    def __init__(self, world, position_y, position_x, age):
        super(Guarana, self).__init__('guarana', world, 0, 0, position_y, position_x, age)

    def breed(self, y, x):
        return Guarana(self.world, y, x, 0)

    def collision(self, atacker, y, x):
        atacker.strength += 3
        self.world.comment_list.append(f"{atacker.specie_enum} eats guarana and its strength = {atacker.strength}")

        self.world.remove_organism(self)
        self.world.grid[y][x] = None
        atacker.set_yx(y, x)
        self.world.grid[y][x] = atacker
        self.world.grid[atacker.prev_y][atacker.prev_x] = None