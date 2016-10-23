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

rouge = (96, 0, 0)
rouge_fonce = (48, 0, 0)
vert = (0, 96, 0)
vert_fonce = (0, 48, 0)
bleu = (0, 0, 96)
bleu_fonce = (0, 0, 96)
jaune = (96, 96, 0)
jaune_fonce = (48, 48, 0)
orange = (96, 48, 0)
majenta = (96, 0, 96)
cyan = (0, 96, 96)
blanc = (96, 96, 96)
noir = (0, 0, 0)


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
        self.sense.clear(orange)
        Timer(1, self.clear).start()

    def clear(self):
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
            self.sense.set_pixel(self.x, self.y, vert)
            self.bouffe = False
            self.score = 0
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
        if self.dx + self.dy != 0:
            if (self.x, self.y) in self.serpent:
                self.en_cours = False
                self.sense.show_message("SCORE %d"%self.score, 0.05,
                                        text_colour=jaune,
                                        back_colour=rouge_fonce)
                Timer(1, self.clear).start()
                return
            self.duree*=.995
            if self.duree < .1:
                self.duree = .1
        self.serpent.append((self.x, self.y))
        if self.x == self.nx and self.y == self.ny:
            self.bouffe = False
            self.score += 1
            if len(self.serpent) >= 20:
                self.serpent.pop(0)
        else:
            self.serpent.pop(0)
        self.sense.set_pixel(self.nx, self.ny, bleu)
        j = 0
        for i in range(len(self.serpent)-1, -1, -1):
            c = self.serpent[i]
            if j == 0:
                self.sense.set_pixel(c[0], c[1], vert)
            elif j%3 == 0:
                self.sense.set_pixel(c[0], c[1], vert_fonce)
            else:
                self.sense.set_pixel(c[0], c[1], jaune_fonce)
            j += 1
        #if len(self.serpent) > 1:
            #for i in self.serpent[:-1]:
                #self.sense.set_pixel(i[0], i[1], vert_fonce)
        #self.sense.set_pixel(self.x, self.y, vert)
        Timer(self.duree, self.run).start()


jeu = Jeu(SenseHat())

try:
    pause()
except KeyboardInterrupt:
    print("Terminé !")
sleep(.5)
SenseHat().clear()
