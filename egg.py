import pygame
from constants import EGG_POSITIVE
from gamemech import GameMech


class Egg(pygame.sprite.DirtySprite):
    def __init__(self, pos_x: int, pos_y: int, size: int, skin: str, id: int, *groups):
        super().__init__(*groups)
        self.size = size
        self.image = pygame.image.load(skin)
        initial_size = self.image.get_size()
        size_rate = size / initial_size[0]
        self.new_size = (int(initial_size[0] * size_rate), int(initial_size[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * size, pos_y * size), self.image.get_size())
        self.value = 1
        self.id = id
        self.pos = (pos_x, pos_y)

    def get_id(self):
        return self.id

    def get_pos(self):
        return self.pos

    def get_value(self):
        return self.value

    def get_size(self):
        return self.new_size

    def update(self, game: object, gm: GameMech):
        # Keep visible
        self.dirty = 1
