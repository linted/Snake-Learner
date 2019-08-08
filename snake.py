#!/usr/bin/env python3

"""
Credit to engineer-man <github@engineerman.org> for original snake game code.
"""

import curses
import random

import QLearner


class snakeGame:
    def __init__(self, show=True):
        self.show = show
        screen = curses.initscr()
        curses.curs_set(0)
        self.screenHeight, self.screenWidth = screen.getmaxyx()
        self.window = curses.newwin(self.screenHeight, self.screenWidth, 0, 0)
        self.window.keypad(1)
        self.window.timeout(100)

        snk_x = self.screenWidth // 4
        snk_y = self.screenHeight // 2
        self.snake = [[snk_y, snk_x], [snk_y, snk_x - 1], [snk_y, snk_x - 2]]
        self.food = self.newFood(self.snake, self.screenHeight, self.screenWidth)

    @property
    def show(self):
        return self.__verbose

    @show.setter
    def show(self, value):
        if value:
            self.__verbose = True
        else:
            self.__verbose = False

    def play(self):
        if self.show:
            self.window.addch(*self.food, curses.ACS_PI)
        key = curses.KEY_RIGHT
        direction = 3
        while True:
            next_key = self.window.getch()
            key = key if next_key == -1 else next_key

            if key == curses.KEY_DOWN:
                direction = 0
            elif key == curses.KEY_UP:
                direction = 1
            elif key == curses.KEY_LEFT:
                direction = 2
            elif key == curses.KEY_RIGHT:
                direction = 3
            self.snake = self.moveSnake(
                self.snake, direction, self.food, self.screenHeight, self.screenWidth
            )
            self.updateMap()#direction)

    @staticmethod
    def newFood(snake, screenHeight, screenWidth):
        food = None
        while food is None:
            nf = [
                random.randint(1, screenHeight - 1),
                random.randint(1, screenWidth - 1),
            ]
            food = nf if nf not in snake else None
        return food

    @staticmethod
    def moveSnake(snake, direction, goal, height, width):
        new_head = [snake[0][0], snake[0][1]]

        if direction == 0:
            new_head[0] += 1
        elif direction == 1:
            new_head[0] -= 1
        elif direction == 2:
            new_head[1] -= 1
        elif direction == 3:
            new_head[1] += 1

        snake.insert(0, new_head)

        return snake

    def updateMap(self):

        if self.snake[0] == self.food:
            self.food = self.newFood(self.snake, self.screenHeight, self.screenWidth)
            if self.show:
                self.window.addch(*self.food, curses.ACS_PI)
        elif (
            self.snake[0][0] in [0, self.screenHeight]
            or self.snake[0][1] in [0, self.screenWidth]
            or self.snake[0] in self.snake[1:]
        ):
            raise Exception("Game Over")
        else:
            tail = self.snake.pop()
            if self.show:
                self.window.addch(*tail, " ")

        if self.show:
            self.window.addch(*self.snake[0], curses.ACS_CKBOARD)


if __name__ == "__main__":
    message = ""
    game = snakeGame()
    try:
        game.play()
    except Exception as e:
        message = str(e)
    finally:
        curses.endwin()
        print(message)
