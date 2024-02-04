import os.path
import random
from typing import List, Union

from Organism import Organism
from Sosnowsky import Sosnowsky
from Antelope import Antelope
from Belladonna import Belladonna
from Cyber_sheep import Cyber_sheep
from Fox import Fox
from Grass import Grass
from Guarana import Guarana
from Sheep import Sheep
from Sow_thistle import Sow_thistle
from Turtle import Turtle
from Wolf import Wolf
from Human import Human


class World:

    is_human_alive = True
    humanSA = False
    SA_can_be_activated = True
    human_SA_ture = 1
    SA_is_activated = False
    prev_human_strength = 5
    cooldown = 0
    width = None
    height = None
    grid: List[List[Union[Organism, None]]] = [[]]
    organism_arr: List = []
    human_arr: List = []
    ture = 0
    comment_list = []

    def __init__(self, height, width):
        self.width = width
        self.height = height
        self.grid = [[None for i in range(self.height)] for j in range(self.width)]
        self.key_pressed = ''
        self.comment_list = []


    def is_empty_cell_on_grid(self) -> bool:  # to avoid infinite recursion
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] is None:
                    return True
        return False

    def create_org_at_pos(self, specie: Organism, y, x):
        specie.set_yx(y, x)


    def null_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = None

    def random_cell_generator(self, specie: Organism):
        x = random.randint(0, self.width-1)
        y = random.randint(0, self.height-1)
        if self.grid[y][x] is None:
            self.create_org_at_pos(specie, y, x)
        else:
            if self.is_empty_cell_on_grid():
                self.random_cell_generator(specie)



    def collect_human(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] is not None and self.grid[i][j].specie_enum == 'human':
                    self.human_arr.append(self.grid[i][j])

    def sort(self):
       # for i in range(len(self.organism_arr)):
        self.organism_arr = sorted(self.organism_arr, key=lambda x: (x.get_initiative, x.get_age))

    def collect_org_from_grid(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] is not None and self.grid[i][j].specie_enum != 'human':
                    self.organism_arr.append(self.grid[i][j])

    def remove_organism(self, specie: Organism):
        self.grid[specie.position_y][specie.position_x] = None
        specie.set_is_alive(False)
        if specie.specie_enum == 'human':
            self.human_arr.clear()
            self.is_human_alive = False

    def create_organisms(self):
        self.random_cell_generator(Sheep(self, -1, -1, 2))
        self.random_cell_generator(Sheep(self, -1, -1, 4))

        self.random_cell_generator(Cyber_sheep(self, -1, -1, 7))
        self.random_cell_generator(Cyber_sheep(self, -1, -1, 1))

        self.random_cell_generator(Fox(self, -1, -1, 3))
        self.random_cell_generator(Fox(self, -1, -1, 8))

        self.random_cell_generator(Turtle(self, -1, -1, 3))
        self.random_cell_generator(Turtle(self, -1, -1, 7))

        self.random_cell_generator(Antelope(self, -1, -1, 8))
        self.random_cell_generator(Antelope(self, -1, -1, 4))

        self.random_cell_generator(Wolf(self, -1, -1, 2))
        self.random_cell_generator(Wolf(self, -1, -1, 5))

        self.random_cell_generator(Grass(self, -1, -1, 7))

        self.random_cell_generator(Guarana(self, -1, -1, 2))

        self.random_cell_generator(Sow_thistle(self, -1, -1, 9))

        self.random_cell_generator(Belladonna(self, -1, -1, 4))

        self.random_cell_generator(Sosnowsky(self, -1, -1, 9))

        self.random_cell_generator(Human(self, -1, -1, 3))



    def make_turn(self):
        self.ture += 1
        self.organism_arr.clear()
        self.collect_org_from_grid()

        if self.humanSA and self.SA_can_be_activated and self.is_human_alive:
            self.SA_is_activated = True
            prev_strength = self.prev_human_strength
            new_strength = self.human_arr[0].strength
            if new_strength != prev_strength:
                self.comment_list.append(f"Specal ability activated. Human's strength equals: {new_strength}")
                new_strength -= 1
                self.human_arr[0].strength = new_strength
                self.human_SA_ture += 1

            if new_strength == prev_strength:
                self.humanSA = False
                self.SA_can_be_activated = False
                self.SA_is_activated = False
                self.cooldown = 0
                self.human_SA_ture = 0

        if self.SA_can_be_activated is False:
            self.cooldown += 1
            if self.cooldown == 5:
                self.SA_can_be_activated = True
                self.human_SA_ture = 1

        for i in range(len(self.organism_arr)):
            if self.organism_arr[i].is_alive is True:
                self.organism_arr[i].action()

        for i in range(len(self.organism_arr)):
            if self.organism_arr[i].is_alive is False:
                 self.organism_arr[i] = None

    def save(self):
        file = open("save.txt", "w")
        file.write(str(self.width) + " " + str(self.height) + " " + str(len(self.organism_arr)) + " " + str(self.ture)
                   + " " + str(self.is_human_alive) + " " + str(self.prev_human_strength) + "\n")
        if self.is_human_alive:
            file.write(str(self.human_arr[0].position_y) + " " + str(self.human_arr[0].position_x) + " " +
                       str(self.human_arr[0].strength) + " " + str(self.human_arr[0].age) + " " + str(self.humanSA) + " "+
                       str(self.cooldown) + " " + str(self.human_SA_ture) + " " + str(self.SA_is_activated) + " " +
                       str(self.SA_can_be_activated) + "\n")
        for it in self.organism_arr:
            if it is not None:
                file.write(str(it.specie_enum) + " " + str(it.position_y) + " " + str(it.position_x) + " " + str(it.age) + "\n")
        print("saved successfully")
        file.close()

    def load(self):
        if os.path.isfile("save.txt"):
            file = open("save.txt", "r")
            data = file.readline()
            print(data)
            data = data.split(' ')
            print(data)
            new_height = int(data[0])
            new_width = int(data[1])

            tmp_world = World(new_height, new_width)

            array_len = int(data[2])
            new_ture = int(data[3])
            # new_is_human_alive = bool(data[4])
            new_prev_strength = int(data[5])

            tmp_world.ture = new_ture
            tmp_world.is_human_alive = True if data[4] == 'True' else False
            tmp_world.prev_human_strength = new_prev_strength

            if tmp_world.is_human_alive:
                data = file.readline()
                data = data.split(' ')
                pos_y = int(data[0])
                pos_x = int(data[1])
                new_strength = int(data[2])
                new_age = int(data[3])
                # humanSA = data[4]
                tmp_world.humanSA = True if 'True' in data[4] else False
                cooldown = int(data[5])
                tmp_world.cooldown = cooldown
                humanSATure = int(data[6])
                tmp_world.human_SA_ture = humanSATure
                # SAisActivated = data[7]
                tmp_world.SA_is_activated = True if 'True' in data[7] else False
                 # SAcanBeActivated = data[8]
                tmp_world.SA_can_be_activated = True if 'True' in data[8] else False

                tmp_world.create_org_at_pos(Human(tmp_world, pos_y, pos_x, new_age), pos_y, pos_x)
                tmp_world.grid[pos_y][pos_x].strength = new_strength

            # for line in file:
                # if data[0] == '':
                #     continue
            while data := file.readline():
                # data = file.readline()
                data = data.split(' ')
                o = data[0]
                y = int(data[1])
                x = int(data[2])
                age = int(data[3])

                if o == 'wolf':
                    tmp_world.create_org_at_pos(Wolf(tmp_world, y, x, age), y, x)
                elif o == 'sheep':
                    tmp_world.create_org_at_pos(Sheep(tmp_world, y, x, age), y, x)
                elif o == 'cyber_sheep':
                    tmp_world.create_org_at_pos(Cyber_sheep(tmp_world, y, x, age), y, x)
                elif o == 'fox':
                    tmp_world.create_org_at_pos(Fox(tmp_world, y, x, age), y, x)
                elif o == 'turtle':
                    tmp_world.create_org_at_pos(Turtle(tmp_world, y, x, age), y, x)
                elif o == 'antelope':
                    tmp_world.create_org_at_pos(Antelope(tmp_world, y, x, age), y, x)
                elif o == 'grass':
                    tmp_world.create_org_at_pos(Grass(tmp_world, y, x, age), y, x)
                elif o == 'sow_thistle':
                    tmp_world.create_org_at_pos(Sow_thistle(tmp_world, y, x, age), y, x)
                elif o == 'sosnowsky':
                    tmp_world.create_org_at_pos(Sosnowsky(tmp_world, y, x, age), y, x,)
                elif o == 'belladonna':
                    tmp_world.create_org_at_pos(Belladonna(tmp_world, y, x, age), y, x)
                elif o == 'guarana':
                    tmp_world.create_org_at_pos(Guarana(tmp_world, y, x, age), y, x)
                else:
                    continue
                # self.window.printBoard()
            file.close()
            return tmp_world
        else:
            print("File doesnt exist!")

