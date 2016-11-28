#!/usr/bin/env python3

import pygame
from Game import MainGame

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 900
FRAMES_PER_SECOND = 60
MARGINS = 50


class MainGameFrame:
    def __init__(self):
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.running = True
        self.background = pygame.image.load('images/field.png')
        self.game = MainGame(self.screen.get_rect(), self)

    def start_game(self):
        self.game.initialize_game()
        self.screen.blit(self.background, (0, 0))
        self.update_score()
        while self.running:
            self.clock.tick(FRAMES_PER_SECOND)
            self.game.game_objects.clear(self.screen, self.background)
            self.game.game_objects.draw(self.screen)
            pygame.display.flip()

    def update_score(self):
        text = pygame.font.Font('./VanillaExtractRegular.ttf', 25)
        score = text.render(("Red: " + str(self.game.score['Red']) + " Blue: " + str(self.game.score['Blue'])), 1, (255, 255, 255), self.background)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(score, (1250, 50))


def initialize_window():
    main_window = MainGameFrame()
    main_window.start_game()

if __name__ == '__main__':
    initialize_window()
