#!/usr/bin/env python3

'''
Credit to engineer-man <github@engineerman.org> for original snake game code.
'''

import curses
import random

import QLearner

screen = curses.initscr()
curses.curs_set(0)
sh, sw = screen.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

snk_x = sw//4
snk_y = sh//2
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]




def play():
    food = [sh//2, sw//2]
    w.addch(*food, curses.ACS_PI)

    key = curses.KEY_RIGHT
    direction = 3
    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        if snake[0][0] in [0, sh] or snake[0][1]  in [0, sw] or snake[0] in snake[1:]:
            curses.endwin()
            quit()
    

        if key == curses.KEY_DOWN:
            direction = 0
        elif key== curses.KEY_UP:
            direction = 1
        elif key == curses.KEY_LEFT:
            direction = 2
        elif key == curses.KEY_RIGHT:
            direction = 3

        move_snake(direction, food)



def move_snake(direction, goal):
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

    if snake[0] == goal:
        food = None
        while food is None:
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(*food, curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(*tail, ' ')

    w.addch(*snake[0], curses.ACS_CKBOARD)

if __name__ == "__main__":
    try:
        play()
    except:
        curses.endwin()
