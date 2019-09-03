import os
import random
import argparse
import time
import sys

items = ['$', '&', '.', '#']
random.seed(time.time())


class Field:

    def __init__(self, update_time=0.5,
                 width=50, height=50, field_file='no'):
        if height > 50:
            print('Warning! Field can be too large for your screen!')
        if height < 1 or width < 1:
            print('Height and width must be at least 1!')
            exit(1)
        if update_time <= 0:
            print('Time of update must be bigger than 0!')
            exit(1)
        self.size = (height, width)
        self.field = [['.' for _1 in range(self.size[0])]
                      for _2 in range(self.size[1])]
        self.w = sys.platform.startswith('win')
        self.update_time = update_time
        self.field_file = field_file

    def clear_screen(self):
        if self.w:
            os.system('cls')
        else:
            os.system('clear')

    def render(self):
        for _1 in range(self.size[0]):
            for _2 in range(self.size[1]):
                print(self.field[_1][_2] + '  ', end='')
            print()

    def fill(self):
        if self.field_file == 'no':
            for _1 in range(self.size[0]):
                for _2 in range(self.size[1]):
                    self.field[_1][_2] = random.choice(items)
        else:
            try:
                self.field = [list(x) for x in
                              open(self.field_file.read(), 'r').split('\n')]
            except FileExistsError:
                print('There is no field file!')
                exit(1)
            except:
                print('Field file is unknown format or damaged!')
                exit(1)
            if (len(self.field) != self.size[0] or
                    len(self.field[0]) != self.size[1]):
                print('Size of field is not the same as given!')
                exit(1)

    def get_neighbours(self, i, j):
        vrs = [(1, 1), (1, 0), (1, -1), (0, 1),
               (0, -1), (-1, 1), (-1, 0), (-1, -1)]
        neighbours = []
        for px, py in vrs:
            if (0 <= i + px < self.size[0] and
                    0 <= j + py < self.size[1]):
                neighbours.append(self.field[i + px][j + py])
        return neighbours

    def change(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.field[i][j] == '#':
                    continue
                neighbours = self.get_neighbours(i, j)
                near_fish, near_shrimps = 0, 0
                for elem in neighbours:
                    if elem == '$':
                        near_fish += 1
                    elif elem == '&':
                        near_shrimps += 1
                if self.field[i][j] == '$':
                    if near_fish not in [2, 3]:
                        self.field[i][j] = '.'
                elif self.field[i][j] == '&':
                    if near_shrimps not in [2, 3]:
                        self.field[i][j] = '.'
                elif self.field[i][j] == '.':
                    if near_fish == 3:
                        self.field[i][j] = '$'
                    if near_shrimps == 3:
                        self.field[i][j] = '&'

    def run(self):
        self.fill()
        while True:
            self.clear_screen()
            self.render()
            self.change()
            time.sleep(self.update_time)


parser = argparse.ArgumentParser()
parser.add_argument('update_time',
                    help='float number which shows'
                         ' frequency of screen updating',
                    type=float)
parser.add_argument('width', help='width of the field in cells', type=int)
parser.add_argument('height', help='height of the field in cells', type=int)
parser.add_argument('field_file', help='path to file '
                                       'with your own start field.'
                                       'Write "no" for no field file'
                                       ' About format of this file '
                                       'you can read in description', type=str)
params = parser.parse_args()
f = Field(update_time=params.update_time,
          width=params.width,
          height=params.height,
          field_file=params.field_file)
f.run()
