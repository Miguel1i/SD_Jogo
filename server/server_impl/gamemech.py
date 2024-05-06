import random
from server_impl import MATCH_TIME, MAX_POINTS, EGG_NEGATIVE, EGG_POSITIVE, GOLDEN_EGG
import datetime


class GameMech:

    def __init__(self, nr_x: int, nr_y: int):
        self.world: dict = {}
        self.players: dict = {}
        self.bushes: dict = {}
        self.eggs: dict = {}
        self.x_max: int = nr_x
        self.y_max: int = nr_y
        self.generate_world(nr_x, nr_y)
        self.generate_bushes()
        self.nr_players = 0
        self.time = datetime.datetime.now()
        self.end_time = datetime.timedelta(seconds=MATCH_TIME) + self.time
        self.max_points = MAX_POINTS
        self.golden_egg = False

    def get_nr_x(self) -> int:
        return self.x_max

    def get_nr_y(self) -> int:
        return self.y_max

    def generate_world(self, nr_x: int, nr_y: int) -> None:
        self.world = {(x, y): [] for x in range(nr_x) for y in range(nr_y)}
        self.bushes = {(x, y): [] for x in range(nr_x) for y in range(nr_y)}

    def generate_bushes(self):
        nr_bushes = 0
        for x in range(0, self.x_max):
            for y in range(0, self.y_max):
                if x in (0, self.x_max - 1) or y in (0, self.y_max - 1):
                    self.bushes[nr_bushes] = ["bush", (x, y)]
                    self.world[(x, y)].append(["obst", "bush", nr_bushes])
                    nr_bushes += 1

    def calculate_nr_eggs(self) -> int:
        if len(self.eggs) == 0:
            return 5
        return 1

    def calculate_egg_spawn(self, nr_eggs: int):
        for _ in range(nr_eggs):
            while True:
                x = random.randint(1, self.x_max - 2)
                y = random.randint(1, self.y_max - 2)
                if not self.world[(x, y)] and self.check_distance(x, y):
                    return x, y

    def check_distance(self, x, y):
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (x + i, y + j) in self.world and self.world[(x + i, y + j)]:
                    return False
        return True

    def add_player(self, player) -> None:
        if player.get_name() not in self.players and player.get_pos():
            self.players[player.get_id()] = [player, player.get_pos()]
            self.world[player.get_pos()].append(["player", player.get_name(), player.get_id()])
            self.nr_players += 1

    def add_egg(self, egg) -> None:
        self.eggs[egg.get_id()] = [egg, egg.get_pos()]
        self.world[egg.get_pos()].append(["egg", egg.get_id()])

    def pop_egg(self, egg, player) -> None:

        print(f"{player.get_name()} -> {player.get_score()}")
        self.eggs.pop(egg.get_id())
        self.world[egg.get_pos()].remove(["egg", egg.get_id()])
        if egg.get_value() == 2:
            self.golden_egg = False

    def winner(self):
        for player in self.players.values():
            if player[0].get_score() >= self.max_points:
                return f"Player {player[0].get_name()} ganhou!"
        if self.check_time() >= self.end_time:
            player_1 = self.players[0][0].get_score()
            player_2 = self.players[1][0].get_score()
            if player_1 > player_2:
                return f"Tempo acabou, o Jogador {self.players[0][0].get_name()} ganhou!"
            elif player_2 > player_1:
                return f"Tempo acabou, o Jogador {self.players[1][0].get_name()} ganhou!"
            else:
                return "Tempo acabou, Empate!"
        return "False"

    def get_score(self, player_id) -> int:
        return self.players[player_id][0].get_score()

    def update_score(self, player_id, score):
        self.players[player_id][0].set_score(score)

    def determine_egg(self) -> tuple:
        current_points = sum(self.players[player_id][0].get_score() for player_id in self.players)
        if current_points != 0 and current_points % 10 == 0 and self.golden_egg is False:
            self.golden_egg = True
            return GOLDEN_EGG, 2

        all_negative = sum(-1 for egg_id in self.eggs if self.eggs[egg_id][0].get_value() == -1)
        all_positive = sum(1 for egg_id in self.eggs if self.eggs[egg_id][0].get_value() == 1)

        if all_negative == -3:
            return EGG_POSITIVE, 1
        if all_positive == 4:
            return EGG_NEGATIVE, -1

        egg = random.choice([EGG_NEGATIVE, EGG_POSITIVE])
        return (egg, 1) if egg == EGG_POSITIVE else (egg, -1)

    def check_time(self):
        self.time = datetime.datetime.now()
        return self.time

    def calc_time(self) -> str:
        delta = self.end_time - datetime.datetime.now()
        total_seconds = delta.total_seconds()
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        if delta <= datetime.timedelta():
            return "0:00"
        return f"{int(minutes)}:{int(seconds):02}"

    def check_egg_collison(self) -> tuple:
        for jogador in self.players.values():
            for ovo in self.eggs.values():
                if jogador[1] == ovo[1]:
                    self.update_score(jogador[0].get_id(), ovo[0].get_value())
                    self.pop_egg(ovo[0], jogador[0])
                    return True, ovo[0]
        return False, None

    def execute(self, player_id: int, direction: str):

        if player_id in self.players:
            player = self.players[player_id][0]
            nome: str = self.players[player_id][0].get_name()
            pos_anterior: list = self.players[player_id][1]
            directions = {"RIGHT": (1, 0), "LEFT": (-1, 0), "UP": (0, -1), "DOWN": (0, 1)}
            if direction in directions:
                new_pos: tuple = (
                    pos_anterior[0] + directions[direction][0], pos_anterior[1] + directions[direction][1])
                mundo_pos = self.world[new_pos]

                if not mundo_pos or mundo_pos[0][0] != "obst" and mundo_pos[0][0] != "player":
                    self.world[pos_anterior].remove(["player", nome, player_id])
                    self.world[new_pos].append(["player", nome, player_id])
                    self.players[player_id] = [player, new_pos]
                    return new_pos
                else:
                    self.players[player_id] = [player, pos_anterior]
                    old_pos = tuple(pos_anterior)
                    return old_pos
