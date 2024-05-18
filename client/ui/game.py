import pygame
from ui import GAME_TICK, FONT, FONT_SIZE, WHITE, TRANSPARENT, \
    GAME_ICON, GAME_MUSIC, EGG_COLLECT, CHANNEL_MUSIC, CHANNEL_EGG
from ui.player import Player
import egg
import grass
import bush
from stub.client_stub import ClientStub
from second_player import SecondPlayer


class Game(object):
    """
    Classe Game que representa o jogo.

    Atributos:
        client_stub: ClientStub - o stub do cliente
        height: int - a altura do ecrã
        width: int - a largura do ecrã
        screen: Surface - o ecrã
        background: Surface - o fundo do ecrã
        grid_surface: Surface - a grelha do ecrã
        grid_size: int - o tamanho do quadrante
        clock: Clock - o relógio do jogo
        eggs: LayeredDirty - os ovos
        bushes: Group - os arbustos
        grass: Group - a erva
        players: LayeredDirty - os jogadores
        id: int - o id do jogador

    Métodos:
        game_settings: None - configurações do jogo
        sound_effect: None - toca um efeito sonoro
        draw_text: None - renderiza um texto no ecrã
        draw_panel: None - desenha um painel no ecrã
        draw_scoreboard: None - desenha o painel de pontuação
        draw_timer: None - desenha o painel do tempo
        draw_grid: None - desenha a grelha no ecrã
        create_bushes: None - cria arbustos no ecrã
        create_grass: None - cria erva no ecrã
        create_players: None - cria um jogador
        update_eggs: None - atualiza a posição dos ovos
        check_collisions: None - verifica se houve colisões entre os jogadores e os ovos
        get_egg: Egg | None - obtém um ovo através do seu id
        start_game: None - inicia o jogo
        get_objects: None - obtém os objetos
        update_objects: None - atualiza os objetos
        run: None - inicia o jogo
    """

    def __init__(self, client_sub: ClientStub, grid_size: int):
        """
        Inicializa um objeto Game.
        :param client_sub: ClientStub - o stub do cliente
        :param grid_size: int - o tamanho do quadrante
        """
        self.client_stub: ClientStub = client_sub
        # Screen and background
        self.height: int = self.client_stub.get_nr_quad_y() * grid_size
        self.width: int = self.client_stub.get_nr_quad_x() * grid_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background: pygame.Surface = pygame.Surface(self.screen.get_size())
        self.background: pygame.Surface = self.background.convert()
        game_icon = pygame.image.load(GAME_ICON)
        pygame.display.set_icon(game_icon)
        # Grid
        self.grid_surface: pygame.Surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.grid_surface.fill(TRANSPARENT)
        self.grid_size: int = grid_size
        self.draw_grid(self.grid_surface, self.width, self.height, self.grid_size, (2, 150, 72))
        # Name of the game
        pygame.display.set_caption("Hop to It!")
        # Clock
        self.clock: pygame.time.Clock = pygame.time.Clock()
        # Music
        # pygame.mixer.init()
        # self.sound_effect(GAME_MUSIC, 0.2, -1, CHANNEL_MUSIC)
        # Other attributes
        self.eggs: pygame.sprite.LayeredDirty = pygame.sprite.LayeredDirty()
        self.bushes: pygame.sprite.Group = pygame.sprite.Group()
        self.grass: pygame.sprite.Group = pygame.sprite.Group()
        self.players: pygame.sprite.LayeredDirty = pygame.sprite.LayeredDirty()
        self.id: int | None = None
        pygame.display.update()

    @staticmethod
    def sound_effect(music: str, volume: float, repeat: int, channel: int) -> None:
        """
        Toca um efeito sonoro
        :param music: caminho do ficheiro de música
        :param volume: volume do som
        :param repeat: número de vezes que o som é repetido
        :param channel: canal onde o som é tocado
        :return: None
        """
        channel: pygame.mixer.Channel = pygame.mixer.Channel(channel)
        sound: pygame.mixer.Sound = pygame.mixer.Sound(music)
        channel.set_volume(volume)
        channel.play(sound, loops=repeat)

    def draw_text(self, text: str, font: pygame.font.Font, color: tuple, x: int, y: int) -> None:
        """
        Renderiza um texto no ecrã
        :param text: texto a ser renderizado
        :param font: tipo de letra
        :param color: cor do texto
        :param x:  posição x
        :param y: posição y
        :return: None
        """
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_panel(self, panel_text: str, x: int, y: int) -> None:
        """
        Desenha um painel no ecrã
        :param panel_text: texto a ser renderizado
        :param x:  posição x do painel
        :param y:  posição y do painel
        :return: None
        """
        font: pygame.font.Font = pygame.font.Font(FONT, FONT_SIZE)
        text_width, text_height = font.size(panel_text)
        panel_surface = pygame.Surface((max(self.width, text_width), max(20, text_height)), pygame.SRCALPHA)
        panel_surface.fill(TRANSPARENT)
        self.screen.blit(panel_surface, (x, y))
        self.draw_text(panel_text, font, WHITE, x, y)
        pygame.display.update(pygame.Rect(x, y, max(self.width, text_width), max(20, text_height)))

    def draw_scoreboard(self) -> None:
        """
        Desenha o painel de pontuação
        :return: None
        """
        for jogador in self.players:
            x: int = self.width // 2 - 220 if jogador.get_id() == 0 else self.width // 2 + 110
            panel_text = f"{jogador.get_name()}: {self.client_stub.get_score(jogador.get_id())}"
            self.draw_panel(panel_text, x, 5)

    def draw_timer(self) -> None:
        """
        Desenha o painel do tempo
        :return: None
        """
        panel_text: str = self.client_stub.calc_time()
        self.draw_panel(panel_text, self.width // 2 - 25, 5)

    @staticmethod
    def draw_grid(surface: pygame.Surface, width: int, height: int, size: int, colour: tuple) -> None:
        """
        Desenha a grelha no ecrã
        :param surface: superfície onde a grelha é desenhada
        :param width: largura do ecrã
        :param height: altura do ecrã
        :param size: tamanho do quadrante
        :param colour: cor da grelha
        :return: None
        """
        for pos in range(0, height, size):
            pygame.draw.line(surface, colour, (0, pos), (width, pos))
        for pos in range(0, width, size):
            pygame.draw.line(surface, colour, (pos, 0), (pos, height))

    def create_bushes(self, bush_size: int) -> None:
        """
        Cria arbustos no ecrã
        :param bush_size: tamanho do arbusto
        :return: None
        """
        for x in range(0, self.width, bush_size):
            for y in range(0, self.height, bush_size):
                if x in (0, self.width - bush_size) or y in (0, self.height - bush_size):
                    arbusto: bush.Bush = bush.Bush(x, y, 0, bush_size, self.bushes)
                    self.bushes.add(arbusto)

    def create_grass(self, grass_size: int) -> None:
        """
        Cria erva no ecrã
        :param grass_size: tamanho da erva
        :return: None
        """
        for x in range(0, self.width, grass_size):
            for y in range(0, self.height, grass_size):
                erva: grass.Grass = grass.Grass(x, y, grass_size, self.grass)
                self.grass.add(erva)

    def create_players(self, size: int) -> None:
        """
        Método para criar um jogador
        :param size: tamanho do jogador
        :return: None
        """
        name: str = str(input("Qual é o teu nome? "))
        pos, skin, player_id = self.client_stub.set_player(name)
        self.id: int = player_id
        player: Player = Player(pos[0], pos[1], size, player_id, name, skin, self.players)
        self.players.add(player)
        self.client_stub.add_player(name, player_id, pos, 0, skin)

    def update_eggs(self) -> None:
        """
        Atualiza a posição dos ovos
        :return: None
        """
        self.eggs.empty()
        ovos: dict = self.client_stub.update_eggs()
        for egg_id, egg_pos, egg_value, skin in ovos.values():
            new_egg = egg.Egg(egg_pos[0], egg_pos[1], self.grid_size, skin, egg_id, egg_value, self.eggs)
            self.eggs.add(new_egg)
        self.eggs.update(self, self.client_stub)
        rect_1 = self.eggs.draw(self.screen)
        pygame.display.update(rect_1)

    def check_collisions(self) -> None:
        """
        Verifica se houve colisões entre os jogadores e os ovos
        :return: None
        """
        collison, egg_id = self.client_stub.check_egg_collison()
        if collison:
            self.get_egg(egg_id).kill()
            self.eggs.remove(egg_id)
            self.sound_effect(EGG_COLLECT, 0.5, 0, CHANNEL_EGG)
            self.update_eggs()

    def get_egg(self, egg_id) -> egg.Egg | None:
        """
        Obtém um ovo através do seu id
        :param egg_id: id do ovo
        :return: ovo ou None caso não exista
        """
        for ovo in self.eggs:
            if ovo.get_id() == egg_id:
                return ovo
        return None

    def start_game(self) -> bool:
        """
        Inicia o jogo
        :return: True se o jogo foi iniciado, False caso contrário
        """
        return bool(self.client_stub.execute_start_game())

    def get_objects(self, size) -> None:
        """
        Obtém os objetos do jogo
        :param size: tamanho do objeto
        :return: None
        """
        objects: dict = self.client_stub.get_objects()
        for object_id in objects:
            if int(object_id) != self.id:
                player = SecondPlayer(objects[object_id][1][0], objects[object_id][1][1], size, int(object_id),
                                      objects[object_id][0], objects[object_id][4], self.players)
                self.players.add(player)

    def update_objects(self) -> None:
        """
        Atualiza os objetos
        :return: None
        """
        objects = self.client_stub.get_objects()
        for player in self.players:
            if player.get_id() != self.id:
                player.set_rect(objects[str(player.get_id())][1])

    def run(self) -> None:
        """
        Inicia o jogo
        :return: None
        """
        self.create_bushes(self.grid_size)
        self.create_players(self.grid_size)
        self.create_grass(self.grid_size)

        end_game: bool = False
        self.start_game()
        self.get_objects(self.grid_size)

        while not end_game:
            dt = self.clock.tick(GAME_TICK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_game = True
            self.grass.draw(self.screen)
            self.bushes.update(dt)
            self.bushes.draw(self.screen)
            self.players.update(self, self.client_stub)
            self.update_objects()
            rects = self.players.draw(self.screen)
            self.screen.blit(self.grid_surface, (0, 0))
            self.update_eggs()
            self.check_collisions()
            if self.client_stub.winner() != "False":
                print(self.client_stub.winner())
                end_game = True
            self.draw_scoreboard()
            self.draw_timer()
            pygame.display.update(rects)
        return None
