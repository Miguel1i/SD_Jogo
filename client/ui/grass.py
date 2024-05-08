import pygame
from ui import GRASS_A, GRASS_B, GRASS_C, GRASS_D
import random


class Grass(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int, size: int, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(self.random_pattern())
        initial_size = self.image.get_size()
        size_rate = size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x, pos_y), self.image.get_size())

    def get_size(self):
        return self.new_size

    @staticmethod
    def random_pattern():
        patterns = [GRASS_A, GRASS_B, GRASS_C, GRASS_D]
        return random.choice(patterns)
