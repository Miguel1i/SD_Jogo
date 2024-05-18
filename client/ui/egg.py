import pygame


class Egg(pygame.sprite.DirtySprite):
    """
    Classe que representa um ovo no jogo.

    Atributos:
        size (int): O tamanho do ovo.
        image (Surface): A imagem do ovo.
        rect (Rect): A área retangular do ovo.
        new_size (tuple): O novo tamanho do ovo.
        value (int): O valor do ovo.
        egg_id (int): O id do ovo.
        pos (tuple): A posição do ovo.

    Métodos:
        get_id: int - obtém o id do ovo
        get_pos: tuple - obtém a posição do ovo
        get_value: int - obtém o valor do ovo
        get_size: tuple - obtém o tamanho do ovo
        update: None - atualiza o ovo
    """

    def __init__(self, pos_x: int, pos_y: int, size: int, skin: str, egg_id: int, value: int, *groups):
        super().__init__(*groups)
        self.size: int = size
        self.image: pygame.Surface = pygame.image.load(skin)
        initial_size: tuple = self.image.get_size()
        size_rate: float = size / initial_size[0]
        self.new_size: tuple = (int(initial_size[0] * size_rate), int(initial_size[1] * size_rate))
        self.image: pygame.Surface = pygame.transform.scale(self.image, self.new_size)
        self.rect: pygame.Rect = pygame.rect.Rect((pos_x * size, pos_y * size), self.image.get_size())
        self.value: int = value
        self.egg_id: int = egg_id
        self.pos: tuple = (pos_x, pos_y)

    def get_id(self) -> int:
        """
        Obtém o id do ovo
        :return: int: id do ovo
        """
        return self.egg_id

    # def get_pos(self) -> tuple[int, int]:
    #     """
    #     Obtém a posição do ovo
    #     :return: tuple: posição do ovo
    #     """
    #     return self.pos
    #
    # def get_value(self) -> int:
    #     """
    #     Obtém o valor do ovo
    #     :return: int: valor do ovo
    #     """
    #     return self.value
    #
    # def get_size(self) -> tuple[int, int]:
    #     """
    #     Obtém o tamanho do ovo
    #     :return: tuple: tamanho do ovo
    #     """
    #     return self.new_size
    #
    # def update(self, game: object, cs: object):
    #     """
    #     Atualiza o ovo, mantendo-o visível
    #     :param game:
    #     :param cs:
    #     :return:
    #     """
    #     # Keep visible
    #     self.dirty = 1
