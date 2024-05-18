import pygame
from ui import GRASS_A, GRASS_B, GRASS_C, GRASS_D
import random


class Grass(pygame.sprite.Sprite):
    """
    Classe que representa a erva no jogo.

    Atributos:
        image (Surface): A imagem da erva.
        rect (Rect): A área retangular da erva.
        new_size (tuple): O novo tamanho da erva.

    Métodos:
        get_size: tuple - obtém o tamanho da erva
        random_pattern: str - obtém um padrão aleatório
    """

    def __init__(self, pos_x: int, pos_y: int, size: int, *groups):
        """
        Inicializa um objeto Grass.
        :param pos_x: int - A coordenada x da posição da erva.
        :param pos_y: int - A coordenada y da posição da erva.
        :param size: int - O tamanho da erva.
        :param groups: Group - Argumento opcional que contém o(s) Grupo(s) ao qual este sprite pertence.
        """
        super().__init__(*groups)
        self.image: pygame.Surface = pygame.image.load(self.random_pattern())
        initial_size: tuple = self.image.get_size()
        size_rate: float = size / initial_size[0]
        self.new_size: tuple = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image: pygame.Surface = pygame.transform.scale(self.image, self.new_size)
        self.rect: pygame.Rect = pygame.rect.Rect((pos_x, pos_y), self.image.get_size())

    def get_size(self) -> tuple:
        """
        Obtém o tamanho da erva.
        :return:
        """
        return self.new_size

    @staticmethod
    def random_pattern() -> str:
        """
        Obtém um padrão aleatório.
        :return: None
        """
        patterns = [GRASS_A, GRASS_B, GRASS_C, GRASS_D]
        return random.choice(patterns)
