#!/usr/bin/env python3

from circle_game.Controller import Controller
from circle_game.ControllerPlayer import ControllerPlayer, ControllerPlayerThread
import pygame

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1000
FRAMES_PER_SECOND = 200
MARGINS = 50


class MainGameFrame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.players = []
        self.rendered_players = []
        self.players_threads = []
        self.running = True
        self.background = pygame.image.load('images/field.png')
        self.player_size = (pygame.image.load('images/player1_1.png')).get_rect()

    def start_game(self):
        self.change_player_threads(True)
        while self.running:
            self.clock.tick(FRAMES_PER_SECOND)
            self.screen.fill((0, 0, 0))
            for player in self.rendered_players:
                player.draw(self.screen)
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
            self.players_threads.append(ControllerPlayerThread(player, player.player_num, self))

    def movement_allowed(self, player_num, pos_dirs):
        new_rect = self.players[player_num].rect.move(pos_dirs[0], pos_dirs[1])
        return self.check_in_field(new_rect) and self.check_player_collide(player_num, new_rect)

    def check_in_field(self, new_rect):
        return self.screen.get_rect().contains(new_rect)

    def check_player_collide(self, player_num, new_rect):
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
            window.add_player(ControllerPlayer(index, Controller(paths[index])))
    else:
        raise TypeError("Window is not of type MainWindow")


if __name__ == '__main__':
    initialize_game()




