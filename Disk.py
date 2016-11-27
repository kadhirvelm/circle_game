import pygame
import math
import random
import threading

FRAMES_PER_SECOND = 60
MIN_MOVEMENT = 0.0001
ACCELERATE_FACTOR = 1.05


class Disk(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images/disk.png')
        self.rect = self.image.get_rect()
        self.position = {'x': 0.0, 'y': 0.0}
        self.force_set_disk(300, 300)
        self.energy = 10
        self.game = game
        self.holder = None
        self.hand = 'Left'
        self.update_movement(200, 200)
        self.throwing = {'x': 0, 'y': 0}

    def claim_disk(self, player):
        if self.holder is None:
            self.stop_movement()
            self.holder = player
            self.update_rect()

    def drop_disk(self):
        self.holder = None

    def switch_hands(self, hand):
        """Permitted values: 'Left' and 'Right'. """
        self.hand = hand

    def throw_center(self):
        self.energy = 30000
        self.position['x'] = self.rect.x
        self.position['y'] = self.rect.y
        delta_x = (self.game.center_field['x'] + random.randint(-20, 20)) - self.rect.x
        delta_y = (self.game.center_field['y'] + random.randint(-20, 20)) - self.rect.y
        magnitude = (math.hypot(delta_x, delta_y)) * 25
        self.throwing['x'] = delta_x/magnitude
        self.throwing['y'] = delta_y/magnitude

    def stop_movement(self):
        if self.holder is not None:
            self.holder.throwing_disk = False
            self.holder = None
        self.throwing = {'x': 0, 'y': 0}
        self.energy = 0
        if self.game.distance_from_center(self.rect) <= 125:
            self.force_set_disk(300, 300)

    def update_rect(self):
        if self.holder is not None:
            try:
                if self.hand == 'Left':
                    self.rect.center = (self.holder.rect.x - 10, self.holder.rect.y + 55)
                elif self.hand == 'Right':
                    self.rect.center = (self.holder.rect.x + 120, self.holder.rect.y + 55)
            except AttributeError:
                print("Holder is none")

    def update_movement(self, delta_x, delta_y):
        if self.energy > 0:
            self.position['x'] += delta_x / (30000/self.energy)
            self.position['y'] += delta_y / (30000/self.energy)
            tempRect = self.rect.copy()
            tempRect.x = self.position['x']
            tempRect.y = self.position['y']
            if self.holder is not None:
                if self.game.throw_allowed(self.holder.player_num, tempRect):
                    self.rect.x = self.position['x']
                    self.rect.y = self.position['y']
                    self.energy -= 1
                else:
                    self.stop_movement()
        else:
            self.stop_movement()

    def force_set_disk(self, x, y):
        self.position['x'] = x
        self.position['y'] = y
        self.rect.x = x
        self.rect.y = y

    def collides_with_rect(self, rect):
        return self.rect.colliderect(rect)


class DiskMovementThread(threading.Thread):
    def __init__(self, movement, disk, game):
        threading.Thread.__init__(self)
        self.movement = movement
        self.disk = disk
        self.game = game
        self.moving = True
        self.standard_movement = 0.01

    def run(self):
        while self.moving:
            self.__adjust_frisbee_position()

    def __adjust_frisbee_position(self):
        temp_rect = self.disk.rect.move(self.standard_movement, self.standard_movement)
        if self.game.check_in_field(temp_rect):
            self.disk.update_movement(self.standard_movement, self.standard_movement)
        else:
            self.disk.stop_movement()

    def stop(self):
        self.moving = False
