from Animal import Animal
from random import randint

class Antelope(Animal):
    def __init__(self, world, position_y, position_x, age):
        super(Antelope, self).__init__('antelope', world, 4, 4, position_y, position_x, age)


    def breed(self, y, x):
        return Antelope(self.world, y, x, 0)

    def collision(self, atacker, y, x):
        probability = randint(0, 1)
        if probability == 0:
            self.world.comment_list.append(f"antelope escapes")
            self.action()

            self.world.grid[y][x] = None
            atacker.set_yx(y, x)
            self.world.grid[y][x] = atacker
            self.world.grid[atacker.prev_y][atacker.prev_x] = None
        else:
            if self.strength > atacker.strength:
                self.world.comment_list.append(f"{atacker.specie_enum} is defeated")
                self.world.grid[atacker.position_y][atacker.position_x] = None
                self.world.remove_organism(atacker)
            else:
                self.world.comment_list.append(f"{atacker.specie_enum} wins over {self.specie_enum}")
                self.world.remove_organism(self)
                self.world.grid[y][x] = None
                atacker.set_yx(y, x)
                self.world.grid[y][x] = atacker
                self.world.grid[atacker.prev_y][atacker.prev_x] = None


    def action(self):
        x = self.position_x
        y = self.position_y

        self.prev_x = x
        self.prev_y = y

        random_no = randint(0, 7)
        if random_no == 0:
            self.proposed_x = x + 2
            self.proposed_y = y
        elif random_no == 1:
            self.proposed_x = x - 2
            self.proposed_y = y
        elif random_no == 2:
            self.proposed_x = x
            self.proposed_y = y + 2
        elif random_no == 3:
            self.proposed_x = x
            self.proposed_y = y - 2
        elif random_no == 4:
            self.proposed_x = x - 1
            self.proposed_y = y - 1
        elif random_no == 5:
            self.proposed_x = x + 1
            self.proposed_y = y - 1
        elif random_no == 6:
            self.proposed_x = x - 1
            self.proposed_y = y + 1
        elif random_no == 7:
            self.proposed_x = x + 1
            self.proposed_y = y + 1

        if self.is_cell_valid(self.proposed_y, self.proposed_x):
            if self.is_cell_occupied(self.proposed_y, self.proposed_x):

                self.check_collision(self.proposed_y, self.proposed_x)
            else:
                if self.is_sosnowsky_nearby(self.proposed_y, self.proposed_x):
                    self.world.remove_organism(self)
                    self.world.grid[y][x] = None
                else:
                    self.set_yx(self.proposed_y, self.proposed_x)
                    self.world.grid[self.proposed_y][self.proposed_x] = self.world.grid[y][x]
                    self.world.grid[y][x] = None
        else:
            self.action()