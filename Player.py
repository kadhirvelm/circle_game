#!/usr/bin/env python3
import threading
import pygame

from circle_game.Controller import Controller


class Player(pygame.sprite.Sprite):
    def __init__(self, player_num, input_method):
        pygame.sprite.Sprite.__init__(self)
        if type(input_method) is not Controller:
            raise TypeError("Input method for player is not of type controller")
        self.player_num = player_num
        self.image = pygame.image.load(self.player_dict(player_num))
        self.input = input_method  # type: Controller
        self.position = {'x': 400 * player_num, 'y': 100 * player_num}
        self.latest_press = None
        self.standard_movement = 3
        self.rect = self.image.get_rect()

    def sprint(self, on):
        if on:
            self.standard_movement = 6
        else:
            self.standard_movement = 3

    def update_rect(self):
        self.rect = self.rect.move(self.position['x'], self.position['y'])
        self.rect.center = (self.position['x'], self.position['y'])

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
        values = {'E': standard_movement, 'W': -standard_movement,
                  'N': -standard_movement, 'S': standard_movement,
                  '': 0}
        temp_x = self.player.position['x'] + values[self.movement[0]]
        temp_y = self.player.position['y'] + values[self.movement[1]]
        if self.game_frame.check_player(self.player.player_num, temp_x, temp_y):
            if self.game_frame.check_field(temp_x, 'x'):
                self.player.position['x'] = temp_x
            if self.game_frame.check_field(temp_y, 'y'):
                self.player.position['y'] = temp_y
        self.game_frame.screen.blit(self.player.image,
                                    (self.player.position['x'], self.player.position['y']))

    def update_movement(self, movement):
        self.movement = movement

    def stop(self):
        self.moving = False
