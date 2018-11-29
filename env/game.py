# This code is modified from: https://github.com/nikolockenvitz/2048/blob/master/2048.py
from random import randint
import numpy as np


def format_state(state):
    res = []
    for i in state:
        if i == 0:
            res.append(0)
        else:
            res.append(np.log2(i) / 10)
    return np.array(res)


class Game:
    """
    Class Game
    This class implements the backend including following important functions:
     - move(direction)
        0 - move north / up
        1 - move east  / right
        2 - move south / down
        3 - move west  / left
     - readHighScore()
     - writeHighScore()
     - newGame()
     - isFinished()
    """
    def __init__(self):
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.n_features = 16
        # define probability of fours when random numbers appear (in percent)
        self.probability4 = 10

        # initialize a new game
        self.new_game()

    def new_game(self):
        # initialize/reset field and values
        self.init_field()
        self.init_values()

    def init_values(self):
        """
        This function initializes all variables which are necessary beside
        the field / numbers.
        """
        self.score = 0  # max: 3932164
        self.round = 0

    def init_field(self):
        """
        This function creates an empty field and inserts two random numbers.
        """
        self.field = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        self.insert_rand_num()
        self.insert_rand_num()

    def move(self, direction):
        """
        This function implements the fundamental part of the game.
        It moves and merges the tiles in passed direction.
        Direction has to be 0,1,2,3 (N,E,S,W)
        When move was successful (something changed/merged) a new number
        will be inserted, round will be incremented, highscore updated and
        True will be returned.
        """
        new = [self.__move_up,
               self.__move_right,
               self.__move_down,
               self.__move_left
               ][direction]()

        if self.field != new:
            self.field = new
            self.insert_rand_num()
            self.round += 1
            return True
        return False

    def __move_up(self):
        new = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for x in range(0, 4):
            # 1. get list without empty fields for each column (just numbers)
            values = []
            for y in range(0, 4):
                if self.field[y][x] != 0:
                    values.append(self.field[y][x])
            # 2. merge
            i = 0
            while i < len(values)-1:
                if values[i] == values[i+1]:
                    values[i] *= 2
                    self.score += values[i]
                    del values[i+1]
                i += 1
            # 3. fill numbers in new field
            y = 0
            for number in values:
                new[y][x] = number
                y += 1
        return new

    def __move_left(self):
        new = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for y in range(0, 4):
            # 1. get list without empty fields for each row (just numbers)
            values = []
            for x in range(0, 4):
                if self.field[y][x] != 0:
                    values.append(self.field[y][x])
            # 2. merge
            i = 0
            while i < len(values) - 1:
                if values[i] == values[i+1]:
                    values[i] *= 2
                    self.score += values[i]
                    del values[i+1]
                i += 1
            # 3. fill numbers in new field
            x = 0
            for number in values:
                new[y][x] = number
                x += 1
        return new

    def __move_down(self):
        new = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],[0, 0, 0, 0]]
        for x in range(0, 4):
            # 1. get list without empty fields for each column (just numbers)
            values = []
            for y in range(3, -1, -1):
                if self.field[y][x] != 0:
                    values.append(self.field[y][x])
            # 2. merge
            i = 0
            while i < len(values)-1:
                if values[i] == values[i+1]:
                    values[i] *= 2
                    self.score += values[i]
                    del values[i+1]
                i += 1
            # 3. fill numbers in new field
            y = 3
            for number in values:
                new[y][x] = number
                y -= 1
        return new

    def __move_right(self):
        new = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for y in range(0, 4):
            # 1. get list without empty fields for each row (just numbers)
            values = []
            for x in range(3, -1, -1):
                if self.field[y][x] != 0:
                    values.append(self.field[y][x])
            # 2. merge
            i = 0
            while i < len(values)-1:
                if values[i] == values[i+1]:
                    values[i] *= 2
                    self.score += values[i]
                    del values[i+1]
                i += 1
            # 3. fill numbers in new field
            x = 3
            for number in values:
                new[y][x] = number
                x -= 1
        return new

    def insert_rand_num(self):
        """
        This function inserts 2 or 4 at random field (must be free).
        Empty fields are numbered from 1 to n from top left to bottom right
        corner. A random number decides which of these fields is chosen. The
        functions loops through the field line by line and counts number of
        empty fields to find chosen field. Which number has to be inserted
        will be decided by randomness again (using previously defined
        probabilty for a 4). At the end coordinates of field where new number
        was inserted will be returned.
        """
        nulls = self.get_num_null_values()
        if nulls == 0:
            return False
        r = randint(1, nulls)
        counter0 = 0
        for y in range(4):
            for x in range(4):
                if self.field[y][x] == 0:
                    counter0 += 1
                    if r == counter0:
                        if randint(1, 100) <= self.probability4:
                            self.field[y][x] = 4
                        else:
                            self.field[y][x] = 2
                        return y, x

    def get_num_null_values(self):
        """
        This function returns number of empty fields
        """
        num = 0
        for row in self.field:
            for number in row:
                if number == 0:
                    num += 1
        return num

    def is_finished(self):
        """
        This functions returns whether game is finshed or not.
        A game is finished when no more move can be done. This is obviously
        not the case when there are empty fields (at least one). A move is
        also possible when some adjacent fields have same values and can be
        merged (Von Neumann neighborhood).
        """
        if self.get_num_null_values() == 0:
            # every field is filled, now check for possible merging
            for y in range(0, 4):
                for x in range(0, 4):
                    if x != 3:
                        if self.field[y][x] == self.field[y][x+1]:
                            return False  # merging is possible
                    if y != 3:
                        if self.field[y][x] == self.field[y+1][x]:
                            return False  # merging is possible
            return True
        else:
            # some empty fields
            return False

    def reset(self):
        self.new_game()
        return format_state(np.array(self.field).flatten())

    def step(self, action):
        old_field = self.field
        old_score = self.score
        self.move(action)
        new_score = self.score
        done = self.is_finished()
        s_ = np.array(self.field).flatten()

        # compute reward
        change_score = new_score - old_score
        if old_field != self.field:
            if change_score == 0:
                reward = 0
            else:
                reward = np.log2(change_score) / 8
        else:
            reward = -0.5

        if done:
            reward -= 1

        return format_state(s_), reward, done

    def show(self):
        """
        This show function prints current game status and is only used
        for debugging.
        """
        # get max number
        maxnum = 0
        for row in self.field:
            for number in row:
                maxnum = max(maxnum, number)
        maxlen = len(str(maxnum))
        # print
        for row in self.field:
            for number in row:
                if number:
                    print(" "*(maxlen-len(str(number)))+str(number), end=" ")
                else:
                    print(" "*maxlen, end=" ")
            print("")

