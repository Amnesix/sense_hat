#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Jeu du serpent...
#
# Appuyer sur le bouton central du joystick pour démarrer une nouvelle partie.
# Utiliser le joystick pour diriger le serpent.
# Manger le plus de nourriture possible...
#

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep
from signal import pause
from random import randint
from threading import Timer

t = (64, 64, 64)
s = (0, 64, 0)
n = (0, 0, 64)
p = [(64, 0, 0) for _ in range(64)]

def clamp(val, min_val=0, max_val=7):
    return min(max_val, max(min_val, val))


def rotate(val):
    return (val+8)%8


class Jeu:

    def __init__(self, sense):
        self.sense = sense
        self.sense.stick.direction_up = self.move_up
        self.sense.stick.direction_down = self.move_down
        self.sense.stick.direction_left = self.move_left
        self.sense.stick.direction_right = self.move_right
        self.sense.stick.direction_middle = self.push_button
        self.dx = self.dy = 0
        self.en_cours = False
        self.sense.clear()

    def move_up(self, event):
        if event.action == ACTION_PRESSED:
            self.dy = -1
            self.dx = 0

    def move_down(self, event):
        if event.action == ACTION_PRESSED:
            self.dy = 1
            self.dx = 0

    def move_left(self, event):
        if event.action == ACTION_PRESSED:
            self.dx = -1
            self.dy = 0

    def move_right(self, event):
        if event.action == ACTION_PRESSED:
            self.dx = 1
            self.dy = 0

    def push_button(self, event):
        if not self.en_cours:
            self.en_cours = True
            self.x = randint(0, 7)
            self.y = randint(0, 7)
            self.serpent = [(self.x, self.y)]
            self.dx = self.dy = 0
            self.duree = .5
            self.sense.set_pixel(self.x, self.y, (0, 64, 0))
            self.bouffe = False
            self.run()

    def run(self):
        if not self.bouffe:
            while True:
                self.nx = randint(0, 7)
                self.ny = randint(0, 7)
                if (self.nx, self.ny) not in self.serpent:
                    break
            self.bouffe = True
        self.sense.clear()
        self.x = rotate(self.x+self.dx)
        self.y = rotate(self.y+self.dy)
        if (self.x, self.y) in self.serpent and self.dx + self.dy != 0:
            self.en_cours = False
            self.sense.show_message("SCORE %d"%len(self.serpent), 0.05,
                               text_colour=(64, 64, 0), back_colour=(64, 0, 0))
            return
        self.serpent.append((self.x, self.y))
        if self.x == self.nx and self.y == self.ny:
            self.bouffe = False
        else:
            self.serpent.pop(0)
        self.sense.set_pixel(self.nx, self.ny, n)
        if len(self.serpent) > 1:
            for i in self.serpent[:-1]:
                self.sense.set_pixel(i[0], i[1], s)
        self.sense.set_pixel(self.x, self.y, t)
        self.duree*=.995
        Timer(self.duree, self.run).start()


jeu = Jeu(SenseHat())

try:
    pause()
except KeyboardInterrupt:
    print("Terminé !")
