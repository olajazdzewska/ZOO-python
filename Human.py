from Animal import Animal
from Comment import Comment
class Human(Animal):
    def __init__(self, world, position_y, position_x, age):
        super(Human, self).__init__('human', world, 5, 4, position_y, position_x, age)

    def action(self):
        self.x1 = self.position_x
        self.y1 = self.position_y
        self.prev_x = self.x1
        self.prev_y = self.y1
        self.y2 = self.proposed_y
        self.x2 = self.proposed_x

        if self.is_cell_valid(self.y2, self.x2):
            if self.is_cell_occupied(self.y2, self.x2):
                self.check_collision(self.y2, self.x2)

            else:
                if self.is_sosnowsky_nearby(self.y2, self.x2):
                    self.world.remove_organism(self)
                    self.world.comment_list.append("human got too close to sosnowsky hogweed")
                    self.world.grid[self.y1][self.x1] = None
                else:
                    self.position_x = self.x2
                    self.position_y = self.y2
                    self.world.grid[self.y2][self.x2] = self
                    self.world.grid[self.y1][self.x1] = None