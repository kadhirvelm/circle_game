#!/usr/bin/env python3

from circle_game.Controller import Controller
from circle_game.Player import Player, PlayerThread
import pygame
import _thread


class MainWindow:
    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 1024))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.delta = self.clock.tick(60)
        self.players = []
        self.players_threads = []
        self.running = True

    def start_game(self):
        self.change_player_threads(True)
        while self.running:
            pygame.display.flip()

    def change_player_threads(self, on):
        for player_thread in self.players_threads:
            try:
                if on:
                    player_thread.start()
                else:
                    player_thread.stop()
            except RuntimeError:
                self.repopulate_player_threads()
                self.change_player_threads(on)

    def add_player(self, player):
        self.players.append(player)
        self.repopulate_player_threads()

    def repopulate_player_threads(self):
        del self.players_threads[:]
        for player in self.players:
            self.players_threads.append(PlayerThread(player, player.player_num, self.screen))


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




