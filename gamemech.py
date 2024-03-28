import random
from constants import MATCH_TIME, MAX_POINTS
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

    def generate_world(self, nr_x: int, nr_y: int):
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

    def calculate_egg_spawn(self, nr_eggs: int, egg_id: int):
        for _ in range(nr_eggs):
            while True:
                x = random.randint(1, self.x_max - 2)
                y = random.randint(1, self.y_max - 2)
                if not self.world[(x, y)]:
                    self.eggs[egg_id] = ["egg", (x, y)]
                    self.world[(x, y)].append(["egg", egg_id])
                    return x, y

    def add_player(self, player):
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

    def winner(self):
        for player_id in self.players:
            if self.players[player_id][0].get_score() >= self.max_points or self.calc_time():
                return True

    def calc_time(self):
        self.time = datetime.datetime.now()
        if self.time >= self.end_time:
            return True

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
