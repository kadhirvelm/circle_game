#!/usr/bin/env python3

from circle_game.Controller import Controller
from circle_game.Player import Player
import pygame
import time
import _thread


class MainWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 1024))

        self.clock = pygame.time.Clock()
        self.delta = self.clock.tick(60)
        self.players = []
        self.running = 1

    def start_game(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            for player in self.players:
                _thread.start_new_thread(self.__adjust_input, (player, ))
                # create a thread for each player
                # execute each thread separately, repeatedly instead of calling on new threads
                self.screen.blit(player.image, (player.currX, player.currY))
            pygame.display.flip()

    def add_player(self, player):
        self.players.append(player)

    @staticmethod
    def __adjust_input(player):
        def read_input(read):
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


def initialize_game():
    main_window = MainWindow()
    add_players(main_window)
    main_window.start_game()


def add_players(window):
    if type(window) is MainWindow:
        paths = Controller.return_microsoft_paths()
        for index in range(len(paths)):
            window.add_player(Player(index, Controller(paths[index])))
    else:
        raise TypeError("Window is not of type MainWindow")


if __name__ == '__main__':
    initialize_game()




