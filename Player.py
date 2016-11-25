#!/usr/bin/env python3
import pygame
from circle_game.Controller import Controller
import threading


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

    def run(self):
        while self.running:
            self.__adjust_input(self.screen, self.player)
        print("Exiting out of --> " + str(self.name))

    def stop(self):
        self.running = False

    @staticmethod
    def __adjust_input(screen, player):
        def read_input(read):
            print("Player " + player.player_num + " --> " + str(read))
            if read == 'A':
                player.currX += 1
            elif read == 'B':
                player.currX -= 1
            elif read == 'X':
                player.currY += 1
            elif read == 'Y':
                player.currY -= 1

        if type(player) is not Player:
            raise TypeError("Adjusting non-Player type")
        read = player.input.read()
        read_input(read)
        screen.blit(player.image, (player.currX, player.currY))
