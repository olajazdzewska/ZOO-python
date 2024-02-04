from Organism import Organism
from random import randint
class Plant(Organism):

    def __init__(self, specie_enum, world, strength, initiative, position_y, position_x, age):
        super(Plant, self).__init__(specie_enum, world, strength, initiative, position_y, position_x, age)



    def action(self):
        x = self.position_x
        y = self.position_y

        self.prev_x = x
        self.prev_y = y

        random_no = randint(0, 3)
        prob_of_sow = randint(0, 3)
        if prob_of_sow < 1:
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

            if self.is_cell_valid(self.proposed_y, self.proposed_x):
                if self.is_cell_occupied(self.proposed_y, self.proposed_x):
                    pass
                    # self.breed(self.proposed_y, self.proposed_x)
                else:
                    self.breed(self.proposed_y, self.proposed_x)
                    self.world.grid[self.proposed_y][self.proposed_x] = self.breed(self.proposed_y, self.proposed_x)
            else:
                self.action()