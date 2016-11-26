#!/usr/bin/env python3

from circle_game.Controller import Controller
from circle_game.Player import Player, PlayerThread
import pygame
import math

PLAYER_SIZE = 300


class MainGameFrame:
    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 1024))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.FRAMES_PER_SECOND = 60
        self.players = []
        self.players_threads = []
        self.running = True
        self.WINDOW_DIMENSION = {'x': 1000, 'y': 1000}

    def start_game(self):
        self.change_player_threads(True)
        while self.running:
            self.clock.tick(self.FRAMES_PER_SECOND)
            self.screen.fill((0, 0, 0))
            for player in self.players:
                self.screen.blit(player.image, (player.position['x'], player.position['y']))
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
            self.players_threads.append(PlayerThread(player, player.player_num, self))
            self.screen.blit(player.image, (player.position['x'], player.position['y']))

    def check_field(self, new_position, axis):
        if -250 < new_position < self.WINDOW_DIMENSION[axis]:
            return True
        return False

    def check_player(self, player_num, new_position_x, new_position_y):
        for player in self.players:
            if player.player_num == player_num:
                continue
            delta_x = math.fabs(player.position['x'] - new_position_x)
            delta_y = math.fabs(player.position['y'] - new_position_y)
            if (delta_x <= PLAYER_SIZE) & (delta_y <= PLAYER_SIZE):
                return False
        return True


def initialize_game():
    main_window = MainGameFrame()
    add_players(main_window)
    main_window.start_game()


def add_players(window):
    if type(window) is MainGameFrame:
        paths = Controller.return_microsoft_paths()
        for index in range(len(paths)):
            window.add_player(Player(index, Controller(paths[index])))
    else:
        raise TypeError("Window is not of type MainWindow")


if __name__ == '__main__':
    initialize_game()




