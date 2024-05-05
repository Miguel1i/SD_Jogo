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
