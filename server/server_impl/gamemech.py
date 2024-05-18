import random
from server_impl import MATCH_TIME, MAX_POINTS, EGG_NEGATIVE, EGG_POSITIVE, GOLDEN_EGG, SPAWN_POINT_A, \
    SPAWN_POINT_B, PLAYER_1, PLAYER_2
import datetime


class GameMech:
    """
    Classe GameMech, responsável por realizar os cálculos do jogo

    Atributos:
        world: dict - mundo
        players: dict - jogadores
        bushes: dict - arbustos
        eggs: dict - ovos
        x_max: int - número de quadrantes no eixo x
        y_max: int - número de quadrantes no eixo y
        nr_players: int - número de jogadores
        time: datetime - tempo
        end_time: datetime - tempo final
        max_points: int - número máximo de pontos
        golden_egg: bool - True se o ovo dourado foi gerado, False caso contrário

    Métodos:
        get_nr_x(self) -> int: Retorna o número de quadrantes no eixo x
        get_nr_y(self) -> int: Retorna o número de quadrantes no eixo y
        generate_world(self, nr_x: int, nr_y: int) -> None: Gera o mundo
        generate_bushes(self) -> None: Gera os arbustos
        calculate_nr_eggs(self) -> int: Calcula o número de ovos a serem gerados
        update_eggs(self) -> dict: Atualiza os ovos
        create_eggs(self) -> None: Cria os ovos
        calculate_egg_spawn(self, nr_eggs: int) -> tuple: Calcula a posição de spawn dos ovos
        check_distance(self, x: int, y: int) -> bool: Verifica a distância entre os ovos
        set_player(self, player_name: str) -> tuple: Gera a posição, skin e id do jogador
        add_player(self, player_id: int, player_name: str, player_pos: tuple, player_score: int, player_skin: str) -> None: Adiciona um jogador ao mundo e ao dicionário de jogadores
        add_egg(self, egg_id: int, egg_pos: tuple, egg_value: int, egg_skin: str) -> None: Adiciona um ovo ao mundo e ao dicionário de ovos
        pop_egg(self, egg_id: int, egg_pos: tuple, egg_value: int) -> None: Remove um ovo do mundo e do dicionário de ovos
        winner(self) -> str: Determina o vencedor
        get_score(self, player_id: int) -> int: Retorna o score de um jogador
        update_score(self, player_id: int, score: int) -> None: Atualiza o score de um jogador
        determine_egg(self) -> tuple: Determina o valor e a skin do ovo a ser gerado
        check_time(self) -> datetime: Verifica o tempo atual
        calc_time(self) -> str: Calcula o tempo restante da partida
        check_egg_collision(self) -> tuple: Verifica se houve colisão entre um jogador e um ovo
        get_players(self) -> dict: Retorna os jogadores
    """

    def __init__(self, nr_x: int, nr_y: int):
        """
        Construtor da classe GameMech
        :param nr_x: int - número de quadrantes no eixo x
        :param nr_y: int - número de quadrantes no eixo y
        """
        self.world: dict = {}
        self.players: dict = {}
        self.bushes: dict = {}
        self.eggs: dict = {}
        self.x_max: int = nr_x
        self.y_max: int = nr_y
        self.generate_world(nr_x, nr_y)
        self.generate_bushes()
        self.nr_players: int = 0
        self.time: datetime = datetime.datetime.now()
        self.end_time: datetime = datetime.timedelta(seconds=MATCH_TIME) + self.time
        self.max_points: int = MAX_POINTS
        self.golden_egg: bool = False

    def get_nr_x(self) -> int:
        """
        Retorna o número de quadrantes no eixo x
        :return: int - número de quadrantes no eixo x
        """
        return self.x_max

    def get_nr_y(self) -> int:
        """
        Retorna o número de quadrantes no eixo y
        :return: int - número de quadrantes no eixo y
        """
        return self.y_max

    def generate_world(self, nr_x: int, nr_y: int) -> None:
        """
        Gera o mundo
        :param nr_x: int - número de quadrantes no eixo x
        :param nr_y: int - número de quadrantes no eixo y
        :return: None
        """
        self.world: dict = {(x, y): [] for x in range(nr_x) for y in range(nr_y)}
        self.bushes: dict = {(x, y): [] for x in range(nr_x) for y in range(nr_y)}

    def generate_bushes(self) -> None:
        """
        Gera os arbustos
        :return: None
        """
        nr_bushes: int = 0
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                if x in (0, self.x_max - 1) or y in (0, self.y_max - 1):
                    self.bushes[nr_bushes] = ["bush", (x, y)]
                    self.world[(x, y)].append(["obst", "bush", nr_bushes])
                    nr_bushes += 1

    def calculate_nr_eggs(self) -> int:
        """
        Calcula o número de ovos a serem gerados
        :return: int - número de ovos a serem gerados
        """
        if len(self.eggs) == 0:
            return 5
        elif len(self.eggs) + 1 >= 6:
            return 0
        return 1

    def update_eggs(self) -> dict:
        """
        Atualiza os ovos
        :return: dict - ovos
        """
        self.create_eggs()
        return self.eggs

    def create_eggs(self) -> None:
        """
        Cria os ovos
        :return: None
        """
        nr_eggs = self.calculate_nr_eggs()
        if nr_eggs == 0:
            return
        for _ in range(nr_eggs):
            x, y = self.calculate_egg_spawn(nr_eggs)
            skin, value = self.determine_egg()
            egg_id: int = max(self.eggs.keys()) + 1 if self.eggs else 0
            self.add_egg(egg_id, (x, y), value, skin)

    def calculate_egg_spawn(self, nr_eggs: int):
        """
        Calcula a posição de spawn dos ovos
        :param nr_eggs:  int - número de ovos a serem gerados
        :return: tuple - posição de spawn dos ovos
        """
        for _ in range(nr_eggs):
            while True:
                x: int = random.randint(1, self.x_max - 2)
                y: int = random.randint(1, self.y_max - 2)
                if not self.world[(x, y)] and self.check_distance(x, y):
                    return x, y

    def check_distance(self, x: int, y: int) -> bool:
        """
        Verifica a distância entre os ovos
        :param x: int - posição x
        :param y: int - posição y
        :return: bool - True se a distância for superior a 2 quadriculas, False caso contrário
        """
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (x + i, y + j) in self.world and self.world[(x + i, y + j)]:
                    return False
        return True

    def set_player(self, player_name: str) -> tuple[tuple, str, int] | int:
        """
        Gera a posição, skin e id do jogador
        :param player_name: str - nome do jogador
        :return: tuple - posição, skin e id do jogador, 0 caso o jogador já exista
        """
        pos, skin = (SPAWN_POINT_A, PLAYER_1) if self.nr_players == 0 else (SPAWN_POINT_B, PLAYER_2)
        player_id: int = self.nr_players
        if player_name not in self.players:
            self.nr_players += 1
            return pos, skin, player_id
        else:
            return 0

    def add_player(self, player_id: int, player_name: str, player_pos: tuple, player_score: int,
                   player_skin: str) -> None:
        """
        Adiciona um jogador ao mundo e ao dicionário de jogadores
        :param player_id:  int - id do jogador
        :param player_name:  str - nome do jogador
        :param player_pos: tuple - posição do jogador
        :param player_score: int - score do jogador
        :param player_skin: str - skin do jogador
        :return: None
        """
        self.players[player_id] = [player_name, player_pos, player_score, player_id, player_skin]
        self.world[player_pos].append(["player", player_name, player_id])

    def add_egg(self, egg_id: int, egg_pos: tuple, egg_value: int, egg_skin: str) -> None:
        """
        Adiciona um ovo ao mundo e ao dicionário de ovos
        :param egg_id: int - id do ovo
        :param egg_pos: tuple - posição do ovo
        :param egg_value: int - valor do ovo
        :param egg_skin: str - skin do ovo
        :return: None
        """
        self.eggs[egg_id] = [egg_id, egg_pos, egg_value, egg_skin]
        self.world[egg_pos].append(["egg", egg_id])

    def pop_egg(self, egg_id: int, egg_pos: tuple, egg_value: int) -> None:
        """
        Remove um ovo do mundo e do dicionário de ovos
        :param egg_id: int - id do ovo
        :param egg_pos: tuple - posição do ovo
        :param egg_value: int - valor do ovo
        :return: None
        """
        self.eggs.pop(egg_id)
        self.world[egg_pos].remove(["egg", egg_id])
        if egg_value == 2:
            self.golden_egg: bool = False

    def winner(self) -> str:
        """
        Determina o vencedor
        :return: str - vencedor
        """
        for player in self.players.values():
            if player[2] >= self.max_points:
                return f"Player {player[0]} ganhou!"
        if self.check_time() >= self.end_time:
            player_1_score: int = self.players[0][2]
            player_2_score: int = self.players[1][2]
            if player_1_score > player_2_score:
                return f"Tempo acabou, o Jogador {self.players[0][0]} ganhou!"
            elif player_2_score > player_1_score:
                return f"Tempo acabou, o Jogador {self.players[1][0]} ganhou!"
            else:
                return "Tempo acabou, Empate!"
        return "False"

    def get_score(self, player_id: int) -> int:
        """
        Retorna o score de um jogador
        :param player_id: int - id do jogador
        :return: int - score do jogador
        """
        return self.players[player_id][2]

    def update_score(self, player_id: int, score: int) -> None:
        """
        Atualiza o score de um jogador
        :param player_id: int - id do jogador
        :param score: int - score a ser adicionado
        :return: None
        """
        self.players[player_id][2] += score

    def determine_egg(self) -> tuple:
        """
        Determina o valor e a skin do ovo a ser gerado
        :return: tuple - valor e skin do ovo
        """
        current_points: int = sum(self.players[player_id][2] for player_id in self.players)
        if current_points != 0 and current_points % 10 == 0 and self.golden_egg is False:
            self.golden_egg = True
            return GOLDEN_EGG, 2
        all_negative: int = sum(-1 for egg_id in self.eggs if self.eggs[egg_id][2] == -1)
        all_positive: int = sum(1 for egg_id in self.eggs if self.eggs[egg_id][2] == 1)
        if all_negative == -3:
            return EGG_POSITIVE, 1
        if all_positive == 4:
            return EGG_NEGATIVE, -1
        egg = random.choice([EGG_NEGATIVE, EGG_POSITIVE])
        return (egg, 1) if egg == EGG_POSITIVE else (egg, -1)

    def check_time(self) -> datetime:
        """
        Verifica o tempo atual
        :return:  datetime - tempo restante
        """
        self.time: datetime = datetime.datetime.now()
        return self.time

    def calc_time(self) -> str:
        """
        Calcula o tempo restante da partida
        :return: str - tempo restante
        """
        delta: datetime = self.end_time - datetime.datetime.now()
        total_seconds: float = delta.total_seconds()
        minutes: float = total_seconds // 60
        seconds: float = total_seconds % 60
        if delta <= datetime.timedelta():
            return "0:00"
        return f"{int(minutes)}:{int(seconds):02}"

    def check_egg_collision(self) -> tuple[bool, int] | tuple[bool, None]:
        """
        Verifica se houve colisão entre um jogador e um ovo
        :return: tuple - True se houve colisão, False caso contrário
        """
        for player in self.players.values():
            for egg in self.eggs.values():
                if player[1] == egg[1]:
                    self.update_score(player[3], egg[2])
                    self.pop_egg(*egg[:3])
                    return True, egg[0]
        return False, None

    def get_players(self) -> dict:
        """
        Retorna os jogadores
        :return: dict - jogadores
        """
        return self.players

    def execute(self, player_id: int, direction: str) -> tuple:
        """
        Executa o movimento de um jogador
        :param player_id: int - id do jogador
        :param direction: str - direção do movimento
        :return: tuple - nova posição do jogador
        """
        if player_id in self.players:
            nome, pos_anterior, score, player_id, player_skin = self.players[player_id]
            directions: dict = {"RIGHT": (1, 0), "LEFT": (-1, 0), "UP": (0, -1), "DOWN": (0, 1)}
            if direction in directions:
                new_pos: tuple = (
                    pos_anterior[0] + directions[direction][0], pos_anterior[1] + directions[direction][1])
                mundo_pos: list = self.world[new_pos]
                if not mundo_pos or mundo_pos[0][0] != "obst" and mundo_pos[0][0] != "player":
                    self.world[pos_anterior].remove(["player", nome, player_id])
                    self.world[new_pos].append(["player", nome, player_id])
                    self.players[player_id] = [nome, new_pos, score, player_id, player_skin]
                    return new_pos
                else:
                    self.players[player_id] = [nome, pos_anterior, score, player_id, player_skin]
                    old_pos: tuple = tuple(pos_anterior)
                    return old_pos
