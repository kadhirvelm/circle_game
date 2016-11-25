#!/usr/bin/env python3
import _thread
import threading

import pygame

from circle_game.Controller import Controller

STANDARD_MOVEMENT = 1


class Player:
    def __init__(self, player_num, input_method):
        """
        :param input_method: Controller
        """
        if type(input_method) is not Controller:
            raise TypeError("Input method for player is not of type controller")

        self.player_num = player_num
        self.image = pygame.image.load(self.player_dict(player_num))
        self.input = input_method  # type: Controller
        self.currX = 400 * player_num
        self.currY = 100 * player_num
        self.latest_press = None

    @staticmethod
    def player_dict(num):
        return {0: 'images/player1_1.png',
                1: 'images/player2_1.png',
                2: 'images/player1_2.png',
                3: 'images/player2_2.png'}[num]


class PlayerThread(threading.Thread):
    def __init__(self, player, name, screen):
        threading.Thread.__init__(self)
        self.player = player
        self.name = name
        self.screen = screen
        self.running = True
        self.moving = True
        self.moving_thread = None

    def run(self):
        self.moving_thread = MovementThread(['', ''], self.player, self.screen)
        self.moving_thread.start()
        while self.running:
            self.__adjust_input()

    def stop(self):
        self.running = False
        self.moving_thread.stop()
        self.moving_thread = None

    def __adjust_input(self):
        controller_read = self.player.input.read()
        self.moving_thread.update_movement(controller_read['thumpad'])


class MovementThread(threading.Thread):

    def __init__(self, movement, player, screen):
        threading.Thread.__init__(self)
        self.movement = movement
        self.player = player
        self.screen = screen
        self.moving = True
        self.running = False

    def is_running(self):
        return self.running

    def run(self):
        self.running = True
        while self.moving:
            self.__adjust_player_position()

    def __adjust_player_position(self):
        values = {'E': STANDARD_MOVEMENT, 'W': -STANDARD_MOVEMENT,
                  'N': -STANDARD_MOVEMENT, 'S': STANDARD_MOVEMENT,
                  '': 0}
        self.player.currX += values[self.movement[0]]
        self.player.currY += values[self.movement[1]]
        self.screen.blit(self.player.image, (self.player.currX, self.player.currY))

    def update_movement(self, movement):
        self.movement = movement

    def stop(self):
        self.moving = False
