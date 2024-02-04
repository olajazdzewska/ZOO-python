from enum import Enum
from Dir import Dir
from Comment import Comment
from typing import List



specie_enum = {
    'human': 'H',
    'wolf': 'W',
    'sheep': 'S',
    'cyber_sheep': 'C',
    'fox': 'F',
    'turtle': 'T',
    'antelope': 'A',
    'grass': '~',
    'sow_thistle': 't',
    'sosnowsky': 's',
    'belladonna': 'b',
    'guarana': 'g'
}
class Organism:


    def __init__(self, specie_enum, world, strength, initiative, position_y, position_x, age):
        self.specie_enum = specie_enum
        self.world = world
        self.strength = strength
        self.initiative = initiative
        self.position_x = position_x
        self.position_y = position_y
        self.age = age
        self.is_alive = True
        self.prev_x = -1
        self.prev_y = -1
        self.proposed_x = -1
        self.proposed_y = -1

    def get_species(self):
        return self.specie_enum

    def set_x(self, x):
        self.position_x = x

    def set_y(self, y):
        self.position_y = y

    def set_yx(self, y, x):
        self.position_y = y
        self.position_x = x
        self.world.grid[y][x] = self

    def set_is_alive(self, value):
        self.is_alive = value

    def get_initiative(self):
        return self.initiative

    def get_age(self):
        return self.age

    def is_cell_valid(self, y, x):
        if x >= self.world.width or x<0 or y >= self.world.height or y<0:
            return False
        else:
            return True

    def is_cell_occupied(self, y, x):
        if self.world.grid[y][x] == None:
            return False
        else:
            return True


    def is_sosnowsky_nearby(self, y, x):
        if self.is_cell_valid(y, x+1):
            if self.world.grid[y][x+1] != None and self.world.grid[y][x+1].specie_enum == 'sosnowsky':
                return True
        elif self.is_cell_valid(y, x-1):
            if self.world.grid[y][x-1] != None and self.world.grid[y][x-1].specie_enum == 'sosnowsky':
                return True
        elif self.is_cell_valid(y+1, x):
            if self.world.grid[y+1][x] != None and self.world.grid[y+1][x].specie_enum == 'sosnowsky':
                return True
        elif self.is_cell_valid(y-1, x):
            if self.world.grid[y-1][x] != None and self.world.grid[y-1][x].specie_enum == 'sosnowsky':
                return True
        else:
            return False

    def check_action(self, dir):
        self.x = self.position_x
        self.y = self.position_y
        if dir == 'up':
            self.proposed_x = self.x
            self.proposed_y = self.y - 1
        elif dir == 'left':
            self.proposed_x = self.x - 1
            self.proposed_y = self.y
        elif dir == 'right':
            self.proposed_x = self.x + 1
            self.proposed_y = self.y
        elif dir == 'down':
            self.proposed_x = self.x
            self.proposed_y = self.y + 1
        else:
            pass

    def collision(self, atacker, y, x):
        if self.strength > atacker.strength:
            self.world.comment_list.append(f"{atacker.specie_enum} is defeated ")
            self.world.grid[atacker.position_y][atacker.position_x] = None
            self.world.remove_organism(atacker)
        else:
            self.world.comment_list.append(f"{atacker.specie_enum} wins over {self.specie_enum}")
            self.world.remove_organism(self)
            self.world.grid[y][x] = None
            atacker.set_yx(y, x)
            self.world.grid[y][x] = atacker
            self.world.grid[atacker.prev_y][atacker.prev_x] = None

    def check_collision(self, y, x):
        victim = self.world.grid[y][x]
        atacker = self

        if victim != None and atacker != None and victim.is_alive and atacker.is_alive:
            if atacker.specie_enum != victim.specie_enum:
                self.world.comment_list.append(f"{atacker.specie_enum} attacked {victim.specie_enum}")
                # Comment.add_comment(atacker.specie_enum + " attacked " + victim.specie_enum)
                victim.collision(atacker, y, x) #TODO

            else:
                if self.world.is_empty_cell_on_grid():
                    self.world.comment_list.append(f" breed of {victim.specie_enum}")
                    self.put_newborn(victim.position_x, victim.position_y, atacker.position_x, atacker.position_y)

                else:
                    self.world.comment_list.append("there is no empty place for newborn to be put")


    def nearest_free_cell(self, x, y):
        # position = []
        # position[0] = -1
        # position[1] = -1

        if self.is_cell_valid(y, x+1) and self.world.grid[y][x+1] is None:
            # position[0] = y
            # position[1] = x+1
            return [y, x+1]
        elif self.is_cell_valid(y, x-1) and self.world.grid[y][x-1] is None:
            # position[0] = y
            # position[1] = x-1
            return [y, x-1]
        elif self.is_cell_valid(y+1, x) and self.world.grid[y+1][x] is None:
            # position[0] = y+1
            # position[1] = x
            return [y+1, x]
        elif self.is_cell_valid(y-1, x) and self.world.grid[y-1][x] is None:
            # position[0] = y-1
            # position[1] = x
            return [y-1, x]
        else:
            # position[0] = -1
            # position[1] = -1
            return [-1, -1]

    def put_newborn(self, x1, y1, x2, y2):
        new_position = self.nearest_free_cell(x1, y1)
        if new_position[0] == -1 and new_position[1] == -1:
            new_position = self.nearest_free_cell(x2, y2)
            if new_position[0] == -1 and new_position[1] == -1:
                self.world.comment_list.append("there is no empty place for newborn to be put")
            else:
                # TODO blad z breedem?
                self.breed(new_position[0], new_position[1])
                self.world.grid[new_position[0]][new_position[1]] = self.breed(new_position[0], new_position[1])
        else:
            self.breed(new_position[0], new_position[1])
            self.world.grid[new_position[0]][new_position[1]] = self.breed(new_position[0], new_position[1])


    def breed(self, param, param1):
        pass

    def special_ability(self):
        new_strength = 10
        self.strength = new_strength
