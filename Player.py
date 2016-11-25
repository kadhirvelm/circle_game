#!/usr/bin/env python3
import pygame
from circle_game.Controller import Controller


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
        self.currX = 100 * player_num
        self.currY = 100 * player_num
        self.latest_press = None

    @staticmethod
    def player_dict(num):
        return {0: 'images/player1_1.png',
                1: 'images/player2_1.png',
                2: 'images/player1_2.png',
                3: 'images/player2_2.png'}[num]
