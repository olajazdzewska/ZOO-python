from Animal import Animal
from random import randint
class Fox(Animal):
    def __init__(self, world, position_y, position_x, age):
        super(Fox, self).__init__('fox', world, 3, 7, position_y, position_x, age)

    def breed(self, y, x):
        return Fox(self.world, y, x, 0)

    def check_if_stronger(self, x, y):
        if self.world.grid[y][x] is None:
            return False
        if self.world.grid[y][x] is not None and self.world.grid[y][x].strength <= self.strength:
            return False
        else:
            return True

    def action(self):
        x = self.position_x
        y = self.position_y

        self.prev_x = x
        self.prev_y = y

        random_no = randint(0, 3)
        if random_no == 0:
            self.proposed_x = x + 1
            self.proposed_y = y
        elif random_no == 1:
            self.proposed_x = x - 1
            self.proposed_y = y
        elif random_no == 2:
            self.proposed_x = x
            self.proposed_y = y + 1
        elif random_no == 3:
            self.proposed_x = x
            self.proposed_y = y - 1

        if self.is_cell_valid(self.proposed_y, self.proposed_x) and self.check_if_stronger(self.proposed_x, self.proposed_y) is False:
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
