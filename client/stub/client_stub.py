from sys import getsizeof
from socket_impl.sockets import Socket
import stub as client


class ClientStub:
    """
    Classe que representa o stub do cliente.

    Atributos:
        _host: str - endereço do servidor
        _port: int - porta do servidor
        socket: Socket - socket do cliente

    Métodos:
        get_nr_quad_x: int - obtém o número de quadrantes no eixo x
        get_nr_quad_y: int - obtém o número de quadrantes no eixo y
        get_score: int - obtém o score de um jogador
        calc_time: str - calcula o tempo
        winner: str - obtém o vencedor
        check_egg_collison: tuple - verifica a colisão dos ovos
        step: tuple - executa um passo
        set_player: tuple - define um jogador
        add_player: None - adiciona um jogador
        update_eggs: dict - atualiza os ovos
        execute_start_game: int - executa o início do jogo
        get_objects: dict - obtém os objetos
        exec_stop_client: None - termina o cliente
        exec_stop_server: None - termina o servidor
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Construtor da classe ClientStub.
        :param host: endereço do servidor
        :param port: porta do servidor
        """
        self._host: str = host
        self._port: int = port
        self.socket = Socket.create_client_connection(self._host, self._port)

    def get_nr_quad_x(self) -> int:
        """
        Protocolo de comunicação com o servidor para obter o número de quadrantes no eixo x
        :return: int - número de quadrantes no eixo x
        """
        self.socket.send_str(client.QUADX_OP)
        return self.socket.receive_int(client.INT_SIZE)

    def get_nr_quad_y(self) -> int:
        """
        Protocolo de comunicação com o servidor para obter o número de quadrantes no eixo y
        :return: int - número de quadrantes no eixo y
        """
        self.socket.send_str(client.QUADY_OP)
        return self.socket.receive_int(client.INT_SIZE)

    def get_score(self, player_id: int) -> int:
        """
        Protocolo de comunicação com o servidor para obter o score de um jogador
        :param player_id: int - id do jogador
        :return: int - score do jogador
        """
        self.socket.send_str(client.SCORE_OP)
        self.socket.send_int(player_id, client.INT_SIZE)
        return self.socket.receive_int(client.INT_SIZE)

    def calc_time(self) -> str:
        """
        Protocolo de comunicação com o servidor para obter o tempo
        :return: str - tempo
        """
        self.socket.send_str(client.TIME_OP)
        msg_size: int = self.socket.receive_int(client.INT_SIZE)
        return self.socket.receive_str(msg_size)

    def winner(self) -> str:
        """
        Protocolo de comunicação com o servidor para obter o vencedor
        :return: str - vencedor
        """
        self.socket.send_str(client.WINNER_OP)
        msg_size: int = self.socket.receive_int(client.INT_SIZE)
        return self.socket.receive_str(msg_size)

    def check_egg_collison(self) -> tuple:
        """
        Protocolo de comunicação com o servidor para verificar a colisão dos ovos
        :return: tuple - colisão
        """
        self.socket.send_str(client.CHECK_COLLISION_OP)
        return self.socket.receive_obj(client.INT_SIZE)

    def step(self, player_id: id, direction: str) -> tuple:
        """
        Protocolo de comunicação com o servidor para executar um passo
        :param player_id: int - id do jogador
        :param direction: str - direção
        :return: tuple - resultado do passo
        """
        self.socket.send_str(client.STEP_OP)
        self.socket.send_int(player_id, client.INT_SIZE)
        self.socket.send_str(direction)
        return self.socket.receive_obj(client.INT_SIZE)

    def set_player(self, player_name: str) -> tuple:
        """
        Protocolo de comunicação com o servidor para definir um jogador
        :param player_name: str - nome do jogador
        :return: tuple - jogador
        """
        self.socket.send_str(client.SET_PLAYER_OP)
        self.socket.send_int(getsizeof(player_name), client.INT_SIZE)
        self.socket.send_str(player_name)
        return self.socket.receive_obj(client.INT_SIZE)

    def add_player(self, player_name: str, player_id: int, player_pos: tuple, player_score: int, player_skin: str):
        """
        Protocolo de comunicação com o servidor para adicionar um jogador
        :param player_name: str - nome do jogador
        :param player_id: int - id do jogador
        :param player_pos: tuple - posição do jogador
        :param player_score: int - score do jogador
        :param player_skin: str - skin do jogador
        :return: None
        """
        self.socket.send_str(client.ADD_PLAYER_OP)
        self.socket.send_int(getsizeof(player_name), client.INT_SIZE)
        self.socket.send_str(player_name)
        self.socket.receive_str(20)
        self.socket.send_int(player_id, client.INT_SIZE)
        self.socket.send_obj(player_pos, client.INT_SIZE)
        self.socket.send_int(player_score, client.INT_SIZE)
        self.socket.send_int(getsizeof(player_skin), client.INT_SIZE)
        self.socket.send_str(player_skin)
        return None

    def update_eggs(self) -> dict:
        """
        Protocolo de comunicação com o servidor para atualizar os ovos
        :return: dict - ovos
        """
        self.socket.send_str(client.UPDATE_EGGS_OP)
        return self.socket.receive_obj(client.INT_SIZE)

    def execute_start_game(self) -> int:
        """
        Protocolo de comunicação com o servidor para executar o início do jogo
        :return: int - id do jogador
        """
        self.socket.send_str(client.START_GAME)
        return self.socket.receive_int(client.INT_SIZE)

    def get_objects(self) -> dict:
        """
        Protocolo de comunicação com o servidor para obter os objetos
        :return: dict - objetos
        """
        self.socket.send_str(client.GET_OBJECTS)
        return self.socket.receive_obj(client.INT_SIZE)

    def exec_stop_client(self) -> None:
        """
        Protocolo de comunicação com o servidor para terminar o cliente
        :return: None
        """
        self.socket.send_str(client.BYE_OP)
        self.socket.close()

    def exec_stop_server(self) -> None:
        """
        Protocolo de comunicação com o servidor para terminar o servidor
        :return: None
        """
        self.socket.send_str(client.STOP_SERVER_OP)
        self.socket.close()
