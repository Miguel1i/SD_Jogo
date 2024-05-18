import pygame
from client.stub.client_stub import ClientStub


class SecondPlayer(pygame.sprite.DirtySprite):
    """
    Classe Player que representa um jogador no jogo.

    Atributos:
        size (int): O tamanho do jogador.
        image (Surface): A imagem do jogador.
        rect (Rect): A área retangular do jogador.
        pos (tuple): A posição do jogador.
        id (int): O id do jogador.
        name (str): O nome do jogador.
        score (int): A pontuação do jogador.
        skin (str): A skin do jogador.

    Métodos:
        get_size: tuple - obtém o tamanho do jogador
        get_id: int - obtém o id do jogador
        get_name: str - obtém o nome do jogador
        get_pos: tuple - obtém a posição do jogador
        set_rect: None - define a posição do jogador
        update: None - atualiza a posição do jogador
    """

    def __init__(self, pos_x: int, pos_y: int, size: int, player_id: int, name: str, skin: str,
                 *groups):
        """
        Inicializa um objeto Player.

        Args:
            pos_x (int): A coordenada x da posição do jogador.
            pos_y (int): A coordenada y da posição do jogador.
            size (int): O tamanho do jogador.
            id (int): O id do jogador.
            name (str): O nome do jogador.
            skin (str): A skin do jogador.
            groups (Group): Argumento opcional que contém o(s) Grupo(s) ao qual este sprite pertence.
        """
        super().__init__(*groups)
        self.size: int = size
        self.image: pygame.Surface = pygame.image.load(skin)
        initial_size: tuple[int, int] = self.image.get_size()
        size_rate: float = size / initial_size[0]
        self.new_size: tuple[int, int] = (
            int(self.image.get_size()[0] * size_rate), int(self.image.get_size()[1] * size_rate))
        self.image: pygame.Surface = pygame.transform.scale(self.image, self.new_size)
        self.rect: pygame.Rect = pygame.rect.Rect((pos_x * size, pos_y * size), self.image.get_size())
        self.pos: tuple[int, int] = (pos_x, pos_y)
        self.player_id: int = player_id
        self.name: str = name

    def get_size(self) -> tuple[int, int]:
        """
        Obtém o tamanho do jogador.

        Retorna:
            tuple: O tamanho do jogador.
        """
        return self.new_size

    def get_id(self) -> int:
        """
        Obtém o id do jogador.

        Retorna:
            int: O id do jogador.
        """
        return self.player_id

    def get_name(self) -> str:
        """
        Obtém o nome do jogador.

        Retorna:
            str: O nome do jogador.
        """
        return self.name

    def get_pos(self) -> tuple[int, int]:
        """
        Obtém a posição do jogador.

        Retorna:
            tuple: A posição do jogador.
        """
        return self.pos

    def set_rect(self, pos: list) -> None:
        self.rect.x = pos[0] * self.size
        self.rect.y = pos[1] * self.size

    def update(self, game: object, cs: ClientStub) -> None:
        """
        Atualiza a posição do jogador com base nas teclas pressionadas.

        Args:
            game (object): O objeto do jogo.
            cs (ClientStub): O stub do cliente.
        """
        # Mantém visível
        self.dirty: int = 1
