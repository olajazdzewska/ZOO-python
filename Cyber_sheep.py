import math
from typing import List
from Animal import Animal
from random import randint

class Hogweeds:

    x = 0
    y = 0
    distance = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.distance = 9999

    def setdistance(self, org_x, org_y):
        self.distance = math.sqrt(pow(org_x - self.x, 2) + pow(org_y - self.y, 2))

class Cyber_sheep(Animal):

    def __init__(self, world, position_y, position_x, age):
        super(Cyber_sheep, self).__init__('cyber_sheep', world, 11, 4, position_y, position_x, age)

    def breed(self, y, x):
        return Cyber_sheep(self.world, y, x, 0)

    def action(self):
        sosnowsky_arr: List = []
        # closest_sosnowsky = None
        for i in range(len(self.world.organism_arr)):
            if self.world.organism_arr[i].specie_enum == 'sosnowsky':
                org = Hogweeds(self.world.organism_arr[i].position_x, self.world.organism_arr[i].position_y)
                org.setdistance(self.position_x, self.position_y)
                sosnowsky_arr.append(org)

        if len(sosnowsky_arr) == 0:
            random_no = randint(0, 3)
            if random_no == 0:
                self.proposed_x = self.position_x + 1
                self.proposed_y = self.position_y
            elif random_no == 1:
                self.proposed_x = self.position_x - 1
                self.proposed_y = self.position_y
            elif random_no == 2:
                self.proposed_x = self.position_x
                self.proposed_y = self.position_y + 1
            elif random_no == 3:
                self.proposed_x = self.position_x
                self.proposed_y = self.position_y - 1
        else:
            closest_sosnowsky = sosnowsky_arr[0]
            for i in range(len(sosnowsky_arr)):
                if sosnowsky_arr[i].distance < closest_sosnowsky.distance:
                    closest_sosnowsky = sosnowsky_arr[i]
            x = self.position_x
            y = self.position_y
            self.prev_x = x
            self.prev_y = y
            if abs(x - closest_sosnowsky.x) >= abs(y - closest_sosnowsky.y):
                if x > closest_sosnowsky.x:
                    self.proposed_x = x-1
                    self.proposed_y = y
                else:
                    self.proposed_x = x+1
                    self.proposed_y = y
            else:
                if y > closest_sosnowsky.y:
                    self.proposed_y = y-1
                    self.proposed_x = x
                else:
                    self.proposed_y = y + 1
                    self.proposed_x = x

        if self.is_cell_valid(self.proposed_y, self.proposed_x):
            if self.is_cell_occupied(self.proposed_y, self.proposed_x):

                self.check_collision(self.proposed_y, self.proposed_x)

            else:

                self.set_yx(self.proposed_y, self.proposed_x)
                self.world.grid[self.proposed_y][self.proposed_x] = self
                self.world.grid[self.prev_y][self.prev_x] = None
        else:
            self.action()

