from typing import List, Any

import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    global width, rows

    def __init__(self, start, dirx=1, diry=0, col=(255, 0, 0)):
        self.pos = start
        self.dirx = dirx
        self.diry = diry
        self.color = col

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface, eyes=False):
        dis = width // rows
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circlemiddle = (i * dis + centre - radius, j * dis + 8)
            circlemiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circlemiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circlemiddle2, radius)


class Had(object):
    global width, rows
    body = []
    turns = {}

    def __init__(self, col: tuple, pos: tuple):
        self.col = col
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:  # pohyb hada a zmena jeho smeru podle klavesy
                if event.key == pygame.K_LEFT:
                    if self.dirx == 1 and self.diry == 0:  # chci znemoznit moznost macknout opacnou klavesu (byla by
                        # instantni porhra a z gameplay hlediska by to bylo frustujici
                        continue
                    self.dirx = -1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    break
                elif event.key == pygame.K_RIGHT:
                    if self.dirx == -1 and self.diry == 0:
                        continue
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    break
                elif event.key == pygame.K_UP:
                    if self.dirx == 0 and self.diry == 1:
                        continue
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    break
                elif event.key == pygame.K_DOWN:
                    if self.dirx == 0 and self.diry == -1:
                        continue
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                    break
        for i, c in enumerate(self.body):  # zajisteni aby vsechny ostatni hadovy casti udelali stejny pohyb
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:  # + "overflow" pokud se dostanu mimo grid
                if c.dirx == -1 and c.pos[0] <= 0:
                    c.pos = (rows - 1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.diry == 1 and c.pos[1] >= rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.diry == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], rows - 1)
                else:
                    c.move(c.dirx, c.diry)

    def reset(self, pos):  # for future implementation
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    def addcube(self):
        tail = self.body[-1]  # kde je posledni kostka hada
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:  # podle toho kam se had pohybuje chci pridat kostu
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
                c.draw(surface, True)  # pokud je to "hlava" hada tak chci oci
            else:
                c.draw(surface)


def drawgrid(w: int, r: int, surface):
    sizebtw = w // r

    x: int = 0
    y: int = 0
    for i in range(r):
        x += sizebtw
        y += sizebtw

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def spawnapple(r, item):
    positions = item.body
    while True:
        x = random.randrange(r)
        y = random.randrange(r)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # overeni ze apple se nespawne na hadovi
            continue
        else:
            break
    return x, y


def message(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)


def refreshwindow(surface):
    global width, rows, h, apple
    surface.fill((0, 0, 0))
    h.draw(surface)
    apple.draw(surface)
    drawgrid(width, rows, surface)
    pygame.display.update()


def main():
    global width, rows, h, apple, speed, beep
    width = 500
    rows = 20
    #  load music
    pygame.mixer.init(22050, -16, 2, 256)
    pygame.mixer.music.load("Project_snake_files\soundtrack.wav")
    pygame.mixer.music.play(-1)
    beep = pygame.mixer.Sound("Project_snake_files\puap.wav")
    gameover = pygame.mixer.Sound("Project_snake_files\game_over.wav")
    window = pygame.display
    win = window.set_mode((width, width))
    window.set_caption("Snake 0.61")
    h = Had((255, 0, 0), (10, 10))
    h.addcube()
    apple = Cube(spawnapple(rows, h), col=(0, 255, 0))
    flag = True
    speed = 10
    tick = 120
    clock = pygame.time.Clock()

    while flag:
        clock.tick(speed)
        h.move()
        if h.body[0].pos == apple.pos:  # růst hada
            pygame.mixer.Sound.play(beep)
            h.addcube()
            apple = Cube(spawnapple(rows, h), col=(0, 255, 0))
            speed += 1

        for x in range(len(h.body)):  # kouknout se jestli jsem nenaboural sám do sebe
            if h.body[x].pos in list(map(lambda z: z.pos, h.body[x + 1:])):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(gameover)
                message("You LOST!", "Game Over \n" + "Your score was: " + str(len(h.body)))
                flag = False

        refreshwindow(win)

    pass


main()
