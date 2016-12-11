#!/usr/bin/env python3
import pygame

MINMAX_MOVEMENT_FACTOR = 4
MOVE_DIRECTIONS = {'E': 1, 'W': -1,
                'N': -1, 'S': 1,
                '': 0}


MIN_MOVEMENT = .004
MAX_MOVEMENT = .01
ACCELERATE_FACTOR = 1.1
BRAKE_FACTOR = 1.2

class KeyboardPlayer(pygame.sprite.Sprite):
    def __init__(self, player_num):
        pygame.sprite.Sprite.__init__(self)
        self.player_num = player_num
        self.image = pygame.image.load(self.player_dict(player_num))
        self.rect = self.image.get_rect()

    def read(self):
        """Given input data, should return some array of buttons currently pressed."""
        values = {0: 'Released', 1: 'A', 2: 'B', 4: 'X', 8: 'Y', 16: 'LT', 32: 'RT'}
        

        def return_button_value():
            if 'buttons' in output.keys():
                output["buttons"].append(values[int(math.pow(2, curr_number))])
            else:
                output['buttons'] = [values[int(math.pow(2, curr_number))]]

        events = pygame.event.get()
        print(events);
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return 'N'
                if event.key == pygame.K_DOWN:
                    return 'S'
                if event.key == pygame.K_RIGHT:
                    return 'E'
                if event.key == pygame.K_LEFT:
                    return 'W'

        def return_ns(value):
            if value > 63:
                return 'S'
            elif value < 63:
                return 'N'
            else:
                return ''

        # output = {}
        # binary_buttons = bin(data[2])[2:]
        # curr_number = 0
        # for integer in binary_buttons[::-1]:
        #     if int(integer) == 1:
        #         return_button_value()
        #     curr_number += 1
        # if 'buttons' not in output.keys():
        #     output['buttons'] = values[0]

        # output['thumpad'] = [return_we(data[0]), return_ns(data[1])]
        # return output

    def sprint(self, on):
        if on:
            self.standard_movement = MAX_MOVEMENT if self.standard_movement >= MAX_MOVEMENT else self.standard_movement * ACCELERATE_FACTOR
        else:
            self.standard_movement = MIN_MOVEMENT if self.standard_movement <= MIN_MOVEMENT else self.standard_movement / BRAKE_FACTOR

    def update_rect(self, delta_x, delta_y):
        self.position['x'] += delta_x
        self.position['y'] += delta_y
        self.rect.x = self.position['x']
        self.rect.y = self.position['y']

    @staticmethod
    def player_dict(num):
        return {0: 'images/player1_1.png',
                1: 'images/player2_1.png',
                2: 'images/player1_2.png',
                3: 'images/player2_2.png'}[num]


# class PlayerThread(threading.Thread):
#     def __init__(self, player, name, main_game_frame):
#         threading.Thread.__init__(self)
#         self.player = player
#         self.name = name
#         self.game_frame = main_game_frame
#         self.running = True
#         self.moving = True
#         self.moving_thread = None

#     def run(self):
#         self.moving_thread = MovementThread(['', ''], self.player, self.game_frame)
#         self.moving_thread.start()
#         while self.running:
#             self.__adjust_input()

#     def stop(self):
#         self.running = False
#         self.moving_thread.stop()
#         self.moving_thread = None

#     def __adjust_input(self):
#         controller_read = self.player.input.read()
#         self.moving_thread.update_movement(controller_read['thumpad'])
#         self.player_buttons(controller_read['buttons'])

#     def player_buttons(self, button_reads):
#         if 'A' in button_reads:
#             self.player.sprint(True)
#         else:
#             self.player.sprint(False)


# class MovementThread(threading.Thread):
#     def __init__(self, movement, player, game_frame):
#         threading.Thread.__init__(self)
#         self.movement = movement
#         self.player = player
#         self.game_frame = game_frame
#         self.moving = True
#         self.running = False

#     def is_running(self):
#         return self.running

#     def run(self):
#         self.running = True
#         while self.moving:
#             self.__adjust_player_position()

#     def __adjust_player_position(self):
#         standard_movement = self.player.standard_movement
#         x_dir = MOVE_DIRECTIONS[self.movement[0]]
#         y_dir = MOVE_DIRECTIONS[self.movement[1]]

#         if self.game_frame.check_player(self.player.player_num, [x_dir, y_dir]):
#             delta_x = x_dir * standard_movement
#             delta_y = y_dir * standard_movement
#             self.player.update_rect(delta_x, delta_y)

#     def update_movement(self, movement):
#         self.movement = movement

#     def stop(self):
#         self.moving = False

