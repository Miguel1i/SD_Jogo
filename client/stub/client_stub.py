from sys import getsizeof

from socket_impl.sockets import Socket
import stub as client


class ClientStub:
    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
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

    def calculate_egg_spawn(self):
        self.socket.send_str(client.CALC_EGGS)
        size = self.socket.receive_int(client.INT_SIZE)
        x, y = self.socket.receive_obj(size)
        return x, y

    def calc_time(self):
        '''
        Protocolo de comunicação com o servidor para obter o tempo
        :return:
        '''
        self.socket.send_str(client.TIME_OP)
        msg_size = self.socket.receive_int(client.INT_SIZE)
        return self.socket.receive_str(msg_size)

    def determine_egg(self) -> tuple:
        """
        Protocolo de comunicação com o servidor para determinar a posição de um ovo
        :return: tuple - posição do ovo
        """
        self.socket.send_str(client.DETERMINE_OP)
        tuple_size = self.socket.receive_int(client.INT_SIZE)
        x, y = self.socket.receive_obj(tuple_size)
        return x, y

    def winner(self):
        self.socket.send_str(client.WINNER_OP)
        msg_size = self.socket.receive_int(client.INT_SIZE)
        return self.socket.receive_str(msg_size)

    def check_egg_collison(self):
        self.socket.send_str(client.CHECK_COLLISION_OP)
        tuple_size = self.socket.receive_int(client.INT_SIZE)
        return self.socket.receive_obj(tuple_size)

    def execute(self, player_id: int, direction: str):
        self.socket.send_str(client.EXECUTE)
        self.socket.send_int(player_id, client.INT_SIZE)
        self.socket.send_str(direction)
        tuple_size = self.socket.receive_int(client.INT_SIZE)
        return self.socket.receive_obj(tuple_size)

    def set_player(self, name):
        self.socket.send_str(client.SET_PLAYER_OP)
        self.socket.send_int(getsizeof(name), client.INT_SIZE)
        self.socket.send_str(name)
        size = self.socket.receive_int(client.INT_SIZE)
        return self.socket.receive_obj(size)

    def add_player(self, player_name, player_id, player_pos, player_score):
        self.socket.send_str(client.ADD_PLAYER_OP)
        self.socket.send_int(getsizeof(player_name), client.INT_SIZE)
        self.socket.send_str(player_name)
        self.socket.receive_str(20)
        self.socket.send_int(player_id, client.INT_SIZE)
        self.socket.send_obj(player_pos, client.INT_SIZE)
        self.socket.send_int(player_score, client.INT_SIZE)
        return None

    def get_nr_eggs(self) -> int:
        self.socket.send_str(client.GET_NR_EGGS_OP)
        return self.socket.receive_int(client.INT_SIZE)

    def add_egg(self, egg_id, egg_pos, egg_value):
        self.socket.send_str(client.ADD_EGG_OP)
        self.socket.send_int(egg_id, client.INT_SIZE)
        self.socket.send_int(getsizeof(egg_pos), client.INT_SIZE)
        self.socket.send_obj(egg_pos, getsizeof(egg_pos))
        self.socket.send_int(egg_value, client.INT_SIZE)
        return None
    def exec_stop_client(self):
        self.socket.send_str(client.BYE_OP)
        self.socket.close()

    def exec_stop_server(self):
        self.socket.send_str(client.STOP_SERVER_OP)
        self.socket.close()

    # ----- running ------
    # def run(self) -> None:
    #     """
    #     Executes a simple client
    #     """
    #     # first interaction with the stubs
    #     print("First interaction")
    #
    #     self.add()
    #     self.subtract()
    #     self.sym()
    #     self.stop_client()
    #     # second interaction with the stubs
    #     print("Second interaction")
    #     self.sym()
    #
    #     # terminate the server
    #     self.stop_server()

#def main():
#
#    client = ClientMathServer(SERVER_ADDRESS, PORT)
#    client.run()


#if __name__=="__main__":
#    main()
