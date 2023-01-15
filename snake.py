import random

import pygame
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    r = 20
    w = 500

    def __init__(self, start, dirx=1, diry=0, color=(255, 0, 0)):
        self.pos = start
        self.dirx = 1
        self.diry = 0
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface, eyes=False):
        dis = self.w // self.r
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirx == -1 and c.pos[0] <= 0:
                    c.pos = (c.r - 1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.r - 1:
                    c.pos = (0, c.pos[1])
                if c.diry == 1 and c.pos[1] >= c.r - 1:
                    c.pos = (c.pos[0], 0)
                elif c.diry == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.r - 1)
                else:
                    c.move(c.dirx, c.diry)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    def add(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))
        self.body[-1].dirx = dx
        self.body[-1].diry = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def snakefood(r, items):
    position = items.body
    while True:
        x = random.randrange(r)
        y = random.randrange(r)
        if len(list(filter(lambda z: z.pos == (x, y), position))) > 0:
            continue
        else:
            break
    return x, y


def drawgrid(w, r, surface):
    lines = w // r
    x, y = 0, 0
    for i in range(r):
        x += lines
        y += lines
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawwin(surface):
    global r, w, s, food
    surface.fill((0, 0, 0))
    s.draw(surface)
    food.draw(surface)
    drawgrid(w, r, surface)
    pygame.display.update()


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global w, r, s, food
    w = 500
    r = 20
    win = pygame.display.set_mode((w, w))
    pygame.display.set_caption("Snake")
    s = Snake((255, 0, 0), (10, 10))
    food = Cube(snakefood(r, s), color=(0, 0, 255))
    flag = True
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == food.pos:
            s.add()
            food = Cube(snakefood(r, s), color=(0, 0, 255))
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                message_box('You Lost!', 'Play again...')
                print('Score: ', len(s.body))
                s.reset((10, 10))
                break
        redrawwin(win)


if __name__ == "__main__":
    main()
