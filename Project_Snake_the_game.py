import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox


class Kostka(object):
    radky = 0
    w = 0

    def __init__(self, start, dirx=1, diry=0, col=(255, 0, 0)):
        pass

    def pohyb(self, x, y):
        pass

    def namaluj(self, povrch):
        pass


class Had(object):
    body = []
    turns = []

    def __init__(self, col, pos):
        self.col = col
        self.head = Kostka(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

    def reset(self, pos):
        pass

    def pridejKostu(self):
        pass

    def namaluj(self, povrch):
        pass


def namalujGrid(w, radky, povrch):
    sizebtw = w // radky

    x = 0
    y = 0
    for i in range(radky):
        x += sizebtw
        y += sizebtw

        pygame.draw.line(povrch, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(povrch, (255, 255, 255), (0, y), (w, y))


def refreshWindow(povrch):
    global width, radky
    povrch.fill((0, 0, 0))
    namalujGrid(width, radky, povrch)
    pygame.display.update()


def jablicko(radky, items):
    pass


def zprava(co, kontent):
    pass


def main():
    global width, radky
    width = 500
    radky = 20
    win = pygame.display.set_mode((width, width))
    h = Had((255, 0, 0), (10, 10))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        refreshWindow(win)

    pass


main()
