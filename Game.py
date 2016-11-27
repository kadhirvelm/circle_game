#!/usr/bin/env python3

from circle_game.Controller import Controller
from circle_game.Player import Player, PlayerThread
import pygame


class MainGameFrame:
    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 2024))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.FRAMES_PER_SECOND = 200
        self.players = []
        self.rendered_players = []
        self.players_threads = []
        self.running = True
        self.WINDOW_DIMENSION = {'x': 1000, 'y': 1000}
        self.background = pygame.image.load('images/field.png')
        self.player_size = (pygame.image.load('images/player1_1.png')).get_rect()

    def start_game(self):
        self.change_player_threads(True)
        while self.running:
            self.clock.tick(self.FRAMES_PER_SECOND)
            self.screen.fill((0, 0, 0))
            for player in self.players:
                self.screen.blit(player.image, (player.rect.x, player.rect.y))
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
        self.rendered_players.append(pygame.sprite.RenderPlain(player))
        self.repopulate_player_threads()

    def repopulate_player_threads(self):
        del self.players_threads[:]
        for player in self.players:
            self.players_threads.append(PlayerThread(player, player.player_num, self))

    def check_field(self, new_position, axis):
        if -45 < new_position < (self.WINDOW_DIMENSION[axis] - 15):
            return True
        return False

    def check_player(self, player_num, new_rect):
        for player in self.players:
            if player.player_num == player_num:
                continue
            if player.rect.colliderect(new_rect):
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




