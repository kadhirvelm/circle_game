#!/usr/bin/env python3
import pygame

# should put all these final values in 1 file for both controller and keyboard player to access (maybe a super class Player that just has these final vars and the sprint/update movement functions)
MOVE_DIRECTIONS = {'E': 1, 'W': -1,
                'N': -1, 'S': 1,
                '': 0}
MIN_MOVEMENT = .004
MAX_MOVEMENT = .01

# though these ones might be different for keyboard/controller, need to test
MINMAX_MOVEMENT_FACTOR = 4
ACCELERATE_FACTOR = 1.1
BRAKE_FACTOR = 1.2



class KeyboardPlayer(pygame.sprite.Sprite):
    def __init__(self, player_num, main_game):
        pygame.sprite.Sprite.__init__(self)
        self.player_num = player_num
        self.game = main_game
        self.image = pygame.image.load(self.player_dict(player_num))
        self.rect = self.image.get_rect()
        self.standard_movement = 2 #TODO change this
        self.position = {'x' : 0, 'y' : 0} #TODO change this

    # in the future, for potentially 2 keyboard players, can use different keys based on player number, all key events are read at once
    def read(self):
        buttons = 0;
        x_dir = 0
        y_dir = 0
        events = pygame.event.get()
        for event in events:
            # need to deal with holding buttons, this only tracks when the button is pressed
            #   will most likely need some tracker for how often holding actually effects values (like only every 10th tick does the keydown matter, stops too rapid a change
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_dir =  1
                elif event.key == pygame.K_LEFT:
                    x_dir =  -1
                if event.key == pygame.K_UP:
                    y_dir = -1
                elif event.key == pygame.K_DOWN:
                    y_dir =  1

                if event.key == pygame.K_a:
                    buttons += 1
                if event.key == pygame.K_b:
                    buttons += 2
                if event.key == pygame.K_x:
                    buttons += 4
                if event.key == pygame.K_y:
                    buttons += 8
                if event.key == pygame.K_l:
                    buttons += 16
                if event.key == pygame.K_r:
                    buttons += 32
                # should change which keys used above based on keyboard location and what they do


        # untested if this actually moves keyboard player
        if self.game.movement_allowed(self.player_num, [x_dir, y_dir]):
            delta_x = x_dir * self.standard_movement
            delta_y = y_dir * self.standard_movement
            self.update_rect(delta_x, delta_y)

        # deal with buttons' actions here or in the if statments above (probably sohuld create different functions for each button and put it in the super class Player)
 

    # maybe use modifiers (like SHIFT key to tell to sprint)
    def sprint(self, on):
        if on:
            self.standard_movement = MAX_MOVEMENT if self.standard_movement >= MAX_MOVEMENT else self.standard_movement * ACCELERATE_FACTOR
        else:
            self.standard_movement = MIN_MOVEMENT if self.standard_movement <= MIN_MOVEMENT else self.standard_movement / BRAKE_FACTOR


    # this should be a standard method in the Player class
    def update_rect(self, delta_x, delta_y):
        self.position['x'] += delta_x
        self.position['y'] += delta_y
        self.rect.x = self.position['x']
        self.rect.y = self.position['y']

    # this should also be a standard method in the Player class
    @staticmethod
    def player_dict(num):
        return {0: 'images/player1_1.png',
                1: 'images/player2_1.png',
                2: 'images/player1_2.png',
                3: 'images/player2_2.png'}[num]
