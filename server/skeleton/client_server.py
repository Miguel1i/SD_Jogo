from sys import getsizeof
from threading import Thread
import logging
import server_impl as server

from skeleton.server_shared_state import ServerSharedState


class ClientThread(Thread):
    """
    Classe que representa um cliente conectado ao servidor.

    Atributos:
        shared_state: ServerSharedState - estado partilhado entre os clientes
        current_connection: Socket - ligação com o cliente
        address: tuple - endereço do cliente

    Métodos:
        process_start_game: None - processa um pedido para iniciar o jogo
        process_get_nr_quad_x: None - processa um pedido para obter o número de quadrantes no eixo x
        process_get_nr_quad_y: None - processa um pedido para obter o número de quadrantes no eixo y
        process_get_score: None - processa um pedido para obter o score de um jogador
        process_time: None - processa um pedido para obter o tempo
        process_winner: None - processa um pedido para obter o vencedor
        process_check_collision: None - processa um pedido para verificar colisões
        process_step: None - processa um pedido para mover um jogador
        process_set_player: None - processa um pedido para definir um jogador
        process_add_player: None - processa um pedido para adicionar um jogador
        process_update_eggs: None - processa um pedido para atualizar os ovos
        process_get_objects: None - processa um pedido para obter os objetos
        dispatch_request: (bool, bool) - processa um pedido
        run: None - método principal da thread
    """

    def __init__(self, shared_state: ServerSharedState, current_connection, address):
        """
        Construtor da classe ClientThread.
        :param shared_state: ServerSharedState - estado partilhado entre os clientes
        :param current_connection: Socket - ligação com o cliente
        :param address: tuple - endereço do cliente
        """
        self.shared_state: ServerSharedState = shared_state
        self.current_connection = current_connection
        self.gamemech = self.shared_state.get_gamemech()
        self.address = address
        Thread.__init__(self)

    def process_start_game(self) -> None:
        """
        Processa um pedido para iniciar o jogo.
        :return: None
        """
        self.shared_state.get_start_game_sem().acquire()
        self.current_connection.send_int(1, server.INT_SIZE)

    def process_get_nr_quad_x(self) -> None:
        """
        Processa um pedido para obter o número de quadrantes no eixo x.
        :return: None
        """
        nr_x: int = self.shared_state.get_nr_quad_x()
        self.current_connection.send_int(nr_x, server.INT_SIZE)

    def process_get_nr_quad_y(self) -> None:
        """
        Processa um pedido para obter o número de quadrantes no eixo y.
        :return: None
        """
        nr_y: int = self.shared_state.get_nr_quad_y()
        self.current_connection.send_int(nr_y, server.INT_SIZE)

    def process_get_score(self) -> None:
        """
        Processa um pedido para obter o score de um jogador.
        :return: None
        """
        player_id: int = self.current_connection.receive_int(server.INT_SIZE)
        score: int = self.shared_state.get_score(player_id)
        self.current_connection.send_int(score, server.INT_SIZE)

    def process_time(self) -> None:
        """
        Processa um pedido para obter o tempo.
        :return: None
        """
        time: str = self.shared_state.calc_time()
        self.current_connection.send_int(getsizeof(time), server.INT_SIZE)
        self.current_connection.send_str(time)

    def process_winner(self) -> None:
        """
        Processa um pedido para obter o vencedor.
        :return: None
        """
        winner: str = self.shared_state.winner()
        self.current_connection.send_int(getsizeof(winner), server.INT_SIZE)
        self.current_connection.send_str(winner)

    def process_check_collision(self) -> None:
        """
        Processa um pedido para verificar colisões.
        :return: None
        """
        collision: tuple = self.shared_state.check_egg_collison()
        self.current_connection.send_obj(collision, server.INT_SIZE)

    def process_step(self) -> None:
        """
        Processa um pedido para mover um jogador.
        :return: None
        """
        player_id: int = self.current_connection.receive_int(server.INT_SIZE)
        direction: str = self.current_connection.receive_str(server.COMMAND_SIZE)
        new_position: tuple = self.shared_state.step(player_id, direction)
        self.current_connection.send_obj(new_position, server.INT_SIZE)

    def process_set_player(self) -> None:
        """
        Processa um pedido para definir um jogador.
        :return: None
        """
        size: int = self.current_connection.receive_int(server.INT_SIZE)
        player_name: str = self.current_connection.receive_str(size)
        res: tuple = self.shared_state.set_player(player_name)
        self.current_connection.send_obj(res, server.INT_SIZE)

    def process_add_player(self) -> None:
        """
        Processa um pedido para adicionar um jogador.
        :return: None
        """
        size: int = self.current_connection.receive_int(server.INT_SIZE)
        player_name: str = self.current_connection.receive_str(size)
        self.current_connection.send_str("ok")
        player_id: int = self.current_connection.receive_int(server.INT_SIZE)
        x_pos, y_pos = self.current_connection.receive_obj(server.INT_SIZE)
        player_score: int = self.current_connection.receive_int(server.INT_SIZE)
        skin_size: int = self.current_connection.receive_int(server.INT_SIZE)
        player_skin: str = self.current_connection.receive_str(skin_size)
        self.shared_state.add_player(player_id, player_name, (x_pos, y_pos), player_score, player_skin)
        self.shared_state.add_client()

    def process_update_eggs(self) -> None:
        """
        Processa um pedido para atualizar os ovos.
        :return:
        """
        eggs: dict = self.shared_state.update_eggs()
        self.current_connection.send_obj(eggs, server.INT_SIZE)

    def process_get_objects(self) -> None:
        """
        Processa um pedido para obter os objetos.
        :return: None
        """
        objects: dict = self.shared_state.get_objects()
        self.current_connection.send_obj(objects, server.INT_SIZE)

    def dispatch_request(self) -> (bool, bool):
        """
        Processa um pedido do cliente.
        :return: bool, bool - se o servidor deve continuar a correr, se é o último pedido
        """
        request_type = self.current_connection.receive_str(server.COMMAND_SIZE)
        keep_running = True
        last_request = False
        if request_type == server.BYE_OP:
            last_request = True
        elif request_type == server.STOP_SERVER_OP:
            last_request = True
            keep_running = False
        elif request_type == server.START_GAME:
            logging.info("Start game operation requested" + str(self.address))
            self.process_start_game()
        elif request_type == server.QUADX_OP:
            logging.info("Quad x operation requested" + str(self.address))
            self.process_get_nr_quad_x()
        elif request_type == server.SET_PLAYER_OP:
            logging.info("Set player operation requested" + str(self.address))
            self.process_set_player()
        elif request_type == server.QUADY_OP:
            logging.info("Quad y operation requested" + str(self.address))
            self.process_get_nr_quad_y()
        elif request_type == server.ADD_PLAYER_OP:
            logging.info("Add player operation requested" + str(self.address))
            self.process_add_player()
        elif request_type == server.SCORE_OP:
            logging.info("Score operation requested" + str(self.address))
            self.process_get_score()
        elif request_type == server.TIME_OP:
            logging.info("Time operation requested" + str(self.address))
            self.process_time()
        elif request_type == server.WINNER_OP:
            logging.info("Winner operation requested" + str(self.address))
            self.process_winner()
        elif request_type == server.CHECK_COLLISION_OP:
            logging.info("Check collision operation requested" + str(self.address))
            self.process_check_collision()
        elif request_type == server.UPDATE_EGGS_OP:
            logging.info("Update eggs operation requested" + str(self.address))
            self.process_update_eggs()
        elif request_type == server.STEP_OP:
            logging.info("Step operation requested" + str(self.address))
            self.process_step()
        elif request_type == server.GET_OBJECTS:
            logging.info("Get objects operation requested" + str(self.address))
            self.process_get_objects()
        return keep_running, last_request

    def run(self) -> None:
        """
        Método principal da thread.
        :return: None
        """
        last_request = False
        while not last_request:
            keep_running, last_request = self.dispatch_request()
        logging.debug("Client " + str(self.address) + " disconnected")
