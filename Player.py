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

        self.image = pygame.image.load('images/banana.png')
        self.input = input_method  # type: Controller
        self.currX = 0
        self.currY = 0
        self.player_num = player_num
        self.latest_press = None