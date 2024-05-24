import threading
from server_impl.gamemech import GameMech
from server_impl import MAX_CLIENTS


class ServerSharedState:
    """
    Classe que representa o estado partilhado entre os clientes.

    Atributos:
        nr_connections: int - número de conexões
        connections_lock: threading.Lock - lock para controlar o acesso às conexões
        start_game_sem: threading.Semaphore - semáforo para iniciar o jogo
        gamemech: GameMech - mecanismo do jogo

    Métodos:
        add_client: None - adiciona um cliente
        get_start_game_sem: threading.Semaphore - obtém o semáforo para iniciar o jogo
        get_gamemech: GameMech - obtém o mecanismo do jogo
        get_objects: dict - obtém os objetos
        calc_time: str - calcula o tempo
        get_score: int - obtém o score
        get_nr_quad_x: int - obtém o número de quadrantes no eixo x
        get_nr_quad_y: int - obtém o número de quadrantes no eixo y
        check_egg_collison: tuple - verifica a colisão dos ovos
        step: tuple - executa um passo
        set_player: tuple - define um jogador
        add_player: None - adiciona um jogador
        update_eggs: dict - atualiza os ovos
    """

    def __init__(self, gamemech: GameMech):
        """
        Construtor da classe ServerSharedState.
        :param gamemech: GameMech - mecanismo do jogo
        """
        self.nr_connections: int = 0
        self.connections_lock: threading.Lock = threading.Lock()
        self.start_game_sem: threading.Semaphore = threading.Semaphore(0)
        self.gamemech: GameMech = gamemech

    def add_client(self) -> None:
        """
        Adiciona um cliente ao estado partilhado.
        :return: None
        """
        with self.connections_lock:
            self.nr_connections += 1

        if self.nr_connections == MAX_CLIENTS:
            with self.connections_lock:
                for _ in range(MAX_CLIENTS):
                    self.start_game_sem.release()

    def get_start_game_sem(self) -> threading.Semaphore:
        """
        Obtém o semáforo para iniciar o jogo.
        :return: threading.Semaphore - semáforo para iniciar o jogo
        """
        return self.start_game_sem

    def get_gamemech(self) -> GameMech:
        """
        Obtém o mecanismo do jogo.
        :return: GameMech - mecanismo do jogo
        """
        return self.gamemech

    def get_objects(self) -> dict:
        """
        Obtém os objetos do jogo.
        :return: dict - objetos
        """
        with self.connections_lock:
            res: dict = self.gamemech.get_players()  # ver outros objetos
        return res

    def calc_time(self) -> str:
        """
        Calcula o tempo do jogo.
        :return: str - tempo
        """
        with self.connections_lock:
            res: str = self.gamemech.calc_time()
        return res

    def get_score(self, player_id: int) -> int:
        """
        Obtém o score de um jogador.
        :param player_id: int - id do jogador
        :return: int - score do jogador
        """
        with self.connections_lock:
            res: int = self.gamemech.get_score(player_id)
        return res

    def get_nr_quad_x(self) -> int:
        """
        Obtém o número de quadrantes no eixo x.
        :return: int - número de quadrantes no eixo x
        """
        with self.connections_lock:
            res: int = self.gamemech.get_nr_x()
        return res

    def get_nr_quad_y(self) -> int:
        """
        Obtém o número de quadrantes no eixo y.
        :return: int - número de quadrantes no eixo y
        """
        with self.connections_lock:
            res: int = self.gamemech.get_nr_y()
        return res

    def check_egg_collison(self) -> tuple:
        """
        Verifica a colisão dos ovos.
        :return: tuple - colisão
        """
        with self.connections_lock:
            res: tuple = self.gamemech.check_egg_collision()
        return res

    def step(self, player_id: int, direction: str) -> tuple:
        """
        Executa um passo do jogo.
        :param player_id: int - id do jogador
        :param direction: str - direção
        :return: tuple - resultado do passo
        """
        with self.connections_lock:
            res: tuple = self.gamemech.execute(player_id, direction)
        return res

    def set_player(self, player_name: str) -> tuple:
        """
        Define os atribudos de um jogador.
        :param player_name: str - nome do jogador
        :return: tuple - atributos do jogador
        """
        with self.connections_lock:
            res: tuple = self.gamemech.set_player(player_name)
        return res

    def add_player(self, player_id: int, player_name: str, player_pos: tuple, player_score: int,
                   player_skin: str) -> None:
        """
        Adiciona um jogador ao jogo.
        :param player_id: int - id do jogador
        :param player_name: str - nome do jogador
        :param player_pos: tuple - posição do jogador
        :param player_score: int - score do jogador
        :param player_skin: str - skin do jogador
        :return: None
        """
        with self.connections_lock:
            self.gamemech.add_player(player_id, player_name, player_pos, player_score, player_skin)
        return None

    def update_eggs(self) -> dict:
        """
        Atualiza os ovos do jogo.
        :return: dict - ovos
        """
        with self.connections_lock:
            res: dict = self.gamemech.update_eggs()
        return res

    def winner(self) -> str:
        """
        Obtém o vencedor do jogo.
        :return: str - vencedor
        """
        with self.connections_lock:
            res: str = self.gamemech.winner()
        return res
