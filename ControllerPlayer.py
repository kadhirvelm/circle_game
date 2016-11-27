#!/usr/bin/env python3
import threading
import pygame

from circle_game.Controller import Controller

MINMAX_MOVEMENT_FACTOR = 4
MOVE_DIRECTIONS = {'E': 1, 'W': -1,
                'N': -1, 'S': 1,
                '': 0}


MIN_MOVEMENT = .004
MAX_MOVEMENT = .01
ACCELERATE_FACTOR = 1.1
BRAKE_FACTOR = 1.2


class ControllerPlayer(pygame.sprite.Sprite):
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
        self.has_disk = False
        self.throwing_disk = False

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


class ControllerPlayerThread(threading.Thread):
    def __init__(self, player, name, main_game):
        threading.Thread.__init__(self)
        self.player = player
        self.name = name
        self.game = main_game
        self.running = True
        self.moving = True
        self.moving_thread = None

    def run(self):
        self.moving_thread = ControllerMovementThread(['', ''], self.player, self.game)
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

        if 'B' in button_reads:
            self.deal_with_disk()

        if self.player.has_disk:
            if 'RT' in button_reads:
                self.player.has_disk = False
                self.player.throwing_disk = True
                self.game.disk.throw_center()
            elif 'X' in button_reads:
                self.game.disk.switch_hands('Left')
            elif 'Y' in button_reads:
                self.game.disk.switch_hands('Right')

    def deal_with_disk(self):
        if not self.player.has_disk:
            if self.game.disk.collides_with_rect(self.player.rect):
                self.player.has_disk = True
                self.game.disk.claim_disk(self.player)
        else:
            self.player.has_disk = False
            self.game.disk.drop_disk()


class ControllerMovementThread(threading.Thread):
    def __init__(self, movement, player, game):
        threading.Thread.__init__(self)
        self.movement = movement
        self.player = player
        self.game = game
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

        if self.game.movement_allowed(self.player.player_num, [x_dir, y_dir]):
            delta_x = x_dir * standard_movement
            delta_y = y_dir * standard_movement
            self.player.update_rect(delta_x, delta_y)
            if self.player.has_disk:
                self.game.disk.update_rect()
        if self.player.throwing_disk:
            self.game.disk.update_movement(self.game.disk.throwing['x'], self.game.disk.throwing['y'])

    def update_movement(self, movement):
        self.movement = movement

    def stop(self):
        self.moving = False
