#!/usr/bin/env python3

import pygame
import math
from Controller import Controller
from ControllerPlayer import ControllerPlayer, ControllerPlayerThread
from KeyboardPlayer import KeyboardPlayer
from Disk import Disk

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1000
FRAMES_PER_SECOND = 200
MARGINS = 50


class MainGame:
    def __init__(self, screen_rect, window):
        self.score = {'Red': 0, 'Blue': 0}
        self.players = []
        self.players_threads = []
        self.game_objects = []
        self.screen_rect = screen_rect
        self.window = window
        self.player_size = (pygame.image.load('images/player1_1.png')).get_rect()
        self.center_field = {'x': WINDOW_WIDTH / 2, 'y': WINDOW_HEIGHT / 2}
        self.disk = Disk(self)

    def initialize_game(self):
        self.add_players()
        self.repopulate_player_threads()
        self.change_player_threads(True)
        all_game_objects = self.players.copy()
        all_game_objects.append(self.disk)
        self.game_objects = pygame.sprite.RenderPlain(*all_game_objects)

    def add_players(self):
        self.players.append(KeyboardPlayer(0))
        paths = Controller.return_microsoft_paths()
        # for index in range(len(paths)):
        #     self.players.append(ControllerPlayer(index + 1, Controller(paths[index])))

    def repopulate_player_threads(self):
        del self.players_threads[:]
        for player in self.players:
            if type(player) is ControllerPlayer:
                self.players_threads.append(ControllerPlayerThread(player, player.player_num, self))

    def change_player_threads(self, on):
        if on:
            self.players[0].read()
        for player_thread in self.players_threads:
            try:
                if on:
                    player_thread.start()
                else:
                    player_thread.stop()
            except RuntimeError:
                self.repopulate_player_threads()
                self.change_player_threads(on)

    def movement_allowed(self, player_num, pos_dirs):
        """ Returns true if movement is allowed. """
        new_rect = self.players[player_num].rect.move(pos_dirs[0], pos_dirs[1])
        return self.check_in_field(new_rect) and self.check_player_collide(player_num, new_rect)

    def throw_allowed(self, player_num, rect):
        if self.distance_from_center(rect) <= 10:
            self.team_score(player_num)
        return self.screen_rect.contains(rect) and self.check_player_collide(player_num, rect)

    def check_in_field(self, new_rect):
        if self.distance_from_center(new_rect) <= 125:
            return False
        return self.screen_rect.contains(new_rect)

    def check_player_collide(self, player_num, new_rect):
        for player in self.players:
            if player.player_num == player_num:
                continue
            if player.rect.colliderect(new_rect):
                return False
        return True

    def distance_from_center(self, rect):
        return math.hypot(rect.center[0] - self.center_field['x'], rect.center[1] - self.center_field['y'])

    def team_score(self, player_num):
        self.disk.stop_movement()
        if player_num % 2 == 0:
            self.score['Red'] += 1
        else:
            self.score['Blue'] += 1
        self.window.update_score()
        self.disk.force_set_disk(300, 300)




