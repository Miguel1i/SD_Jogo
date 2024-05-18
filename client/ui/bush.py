import pygame
from ui import BUSH


class Bush(pygame.sprite.Sprite):
    """
    Classe que representa um arbusto no jogo.

    Atributos:
        image (Surface): A imagem do arbusto.
        rect (Rect): A área retangular do arbusto.
        new_size (tuple): O novo tamanho do arbusto.
        acc (int): A aceleração do arbusto.

    Métodos:
        get_size: tuple - obtém o tamanho do arbusto
    """

    def __init__(self, pos_x: int, pos_y: int, acc: int, size: int, *groups):
        super().__init__(*groups)
        self.image: pygame.Surface = pygame.image.load(BUSH)
        initial_size: tuple = self.image.get_size()
        size_rate: float = size / initial_size[0]
        self.new_size: tuple = (int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image: pygame.Surface = pygame.transform.scale(self.image, self.new_size)
        self.rect: pygame.Rect = pygame.rect.Rect((pos_x, pos_y), self.image.get_size())
        self.acc: int = acc

    def get_size(self) -> tuple:
        """
        Obtém o tamanho do arbusto.
        :return: tuple
        """
        return self.new_size
