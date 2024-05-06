import pygame
from client.stub.client_stub import ClientStub


class Player(pygame.sprite.DirtySprite):
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
        self.score: int = 0

    def get_size(self) -> tuple[int, int]:
        """
        Obtém o tamanho do jogador.

        Retorna:
            tuple: O tamanho do jogador.
        """
        return self.new_size

    def set_score(self, score: int) -> None:
        """
        Incrementa a pontuação do jogador.

        Args:
            score (int): A quantidade para incrementar a pontuação do jogador.
        """
        self.score += score

    def get_score(self) -> int:
        """
        Obtém a pontuação do jogador.

        Retorna:
            int: A pontuação do jogador.
        """
        return self.score

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

    def serialize(self):
        """
        Serialize the Player object into a dictionary containing only necessary attributes.
        """
        return {
            "player_id": self.player_id,
            "name": self.name,
            "pos": self.pos,
            "score": self.score
        }

    def deserialize(self, data):
        """
        Deserialize the dictionary data and update the Player object with received attributes.
        """
        self.player_id = data["player_id"]
        self.name = data["name"]
        self.pos = data["pos"]
        self.score = data["score"]

    def update(self, game: object, cs: ClientStub) -> None:
        """
        Atualiza a posição do jogador com base nas teclas pressionadas.

        Args:
            game (object): O objeto do jogo.
            gm (GameMech): O objeto de mecânica do jogo.
        """
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            new_pos: list[int] = list(cs.execute(self.player_id, "LEFT"))
            self.pos = new_pos
            self.rect.x = new_pos[0] * self.size
            self.rect.y = new_pos[1] * self.size
        if key[pygame.K_RIGHT]:
            new_pos: list[int] = list(cs.execute(self.player_id, "RIGHT"))
            self.pos = new_pos
            self.rect.x = new_pos[0] * self.size
            self.rect.y = new_pos[1] * self.size
        if key[pygame.K_UP]:
            new_pos: list[int] = list(cs.execute(self.player_id, "UP"))
            self.pos = new_pos
            self.rect.x = new_pos[0] * self.size
            self.rect.y = new_pos[1] * self.size
        if key[pygame.K_DOWN]:
            new_pos: list[int] = list(cs.execute(self.player_id, "DOWN"))
            self.pos = new_pos
            self.rect.x = new_pos[0] * self.size
            self.rect.y = new_pos[1] * self.size

        # Mantém visível
        self.dirty: int = 1
