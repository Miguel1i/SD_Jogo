import pygame
from gamemech import GameMech


class Player(pygame.sprite.DirtySprite):

    def __init__(self, pos_x: int, pos_y: int, size: int, id: int, name: str, skin: str, *groups):
        super().__init__(*groups)
        self.size = size
        self.image = pygame.image.load(skin)
        initial_size = self.image.get_size()
        size_rate = size / initial_size[0]
        self.new_size = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.rect = pygame.rect.Rect((pos_x * size, pos_y * size), self.image.get_size())
        self.pos = (pos_x, pos_y)
        self.id = id
        self.name = name
        self.score = 0

    def get_size(self):
        return self.new_size

    def set_score(self, score: int):
        self.score += score

    def get_score(self):
        return self.score

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    def update(self, game: object, gm: GameMech):

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            new_pos = list(gm.execute(self.id, "LEFT"))
            self.pos = new_pos
            self.rect.x = new_pos[0] * self.size
            self.rect.y = new_pos[1] * self.size
        if key[pygame.K_RIGHT]:
            new_pos = list(gm.execute(self.id, "RIGHT"))
            self.pos = new_pos
            self.rect.x = new_pos[0] * self.size
            self.rect.y = new_pos[1] * self.size
        if key[pygame.K_UP]:
            new_pos = list(gm.execute(self.id, "UP"))
            self.pos = new_pos
            self.rect.x = new_pos[0] * self.size
            self.rect.y = new_pos[1] * self.size
        if key[pygame.K_DOWN]:
            new_pos = list(gm.execute(self.id, "DOWN"))
            self.pos = new_pos
            self.rect.x = new_pos[0] * self.size
            self.rect.y = new_pos[1] * self.size

        # Keep visible
        self.dirty = 1
