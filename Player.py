#!/usr/bin/env python3
import threading
import pygame
import math

from circle_game.Controller import Controller

MINMAX_MOVEMENT_FACTOR = 4
MOVE_DIRECTIONS = {'E': 1, 'W': -1,
                'N': -1, 'S': 1,
                '': 0}


MIN_MOVEMENT = .004
MAX_MOVEMENT = .01
ACCELERATE_FACTOR = 1.1
BRAKE_FACTOR = 1.2

class Player(pygame.sprite.Sprite):
    def __init__(self, player_num, input_method):
        pygame.sprite.Sprite.__init__(self)
        if type(input_method) is not Controller:
            raise TypeError("Input method for player is not of type controller")
        self.player_num = player_num
        self.image = pygame.image.load(self.player_dict(player_num))
        self.input = input_method  # type: Controller
        self.latest_press = None
        self.standard_movement = MIN_MOVEMENT
        self.position = {'x': 0.0, 'y': 0.0}
        self.rect = self.image.get_rect()
        self.update_rect(100 * player_num, 100 * player_num)

    def sprint(self, on):
        if on:
            self.standard_movement = MAX_MOVEMENT if self.standard_movement >= MAX_MOVEMENT else self.standard_movement * ACCELERATE_FACTOR
        else:
            self.standard_movement = MIN_MOVEMENT if self.standard_movement <= MIN_MOVEMENT else self.standard_movement / BRAKE_FACTOR

    def update_rect(self, delta_x, delta_y):
        self.position['x'] += delta_x
        self.position['y'] += delta_y
        self.rect.x = self.position['x']
        self.rect.y = self.position['y']

    @staticmethod
    def player_dict(num):
        return {0: 'images/player1_1.png',
                1: 'images/player2_1.png',
                2: 'images/player1_2.png',
                3: 'images/player2_2.png'}[num]


class PlayerThread(threading.Thread):
    def __init__(self, player, name, main_game_frame):
        threading.Thread.__init__(self)
        self.player = player
        self.name = name
        self.game_frame = main_game_frame
        self.running = True
        self.moving = True
        self.moving_thread = None

    def run(self):
        self.moving_thread = MovementThread(['', ''], self.player, self.game_frame)
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
        self.player_buttons(controller_read['buttons'])

    def player_buttons(self, button_reads):
        if 'A' in button_reads:
            self.player.sprint(True)
        else:
            self.player.sprint(False)


class MovementThread(threading.Thread):
    def __init__(self, movement, player, game_frame):
        threading.Thread.__init__(self)
        self.movement = movement
        self.player = player
        self.game_frame = game_frame
        self.moving = True
        self.running = False

    def is_running(self):
        return self.running

    def run(self):
        self.running = True
        while self.moving:
            self.__adjust_player_position()

    def __adjust_player_position(self):
        standard_movement = self.player.standard_movement
        x_dir = MOVE_DIRECTIONS[self.movement[0]]
        y_dir = MOVE_DIRECTIONS[self.movement[1]]

        if self.game_frame.check_player(self.player.player_num, [x_dir, y_dir]):
            delta_x = x_dir * standard_movement
            delta_y = y_dir * standard_movement
            self.player.update_rect(delta_x, delta_y)

    def update_movement(self, movement):
        self.movement = movement

    def stop(self):
        self.moving = False
