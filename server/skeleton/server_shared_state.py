import threading
from server_impl.gamemech import GameMech
from server_impl import MAX_CLIENTS


class ServerSharedState:

    def __init__(self, gamemech: GameMech):
        self.nr_connections: int = 0
        self.connections_lock: threading.Lock = threading.Lock()
        self.start_game: bool = False
        self.start_game_sem: threading.Semaphore = threading.Semaphore(0)
        self.gamemech: GameMech = gamemech

    def add_client(self):
        with self.connections_lock:
            self.nr_connections += 1

        if self.nr_connections == MAX_CLIENTS:
            with self.connections_lock:
                for _ in range(MAX_CLIENTS):
                    self.start_game_sem.release()

    def get_start_game_sem(self):
        return self.start_game

    def start_game(self):
        return self.start_game

    def get_gamemech(self):
        return self.gamemech
