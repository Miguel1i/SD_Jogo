from socket_impl.sockets import Socket
import stub as client
#Constants
# COMMAND_SIZE = 9
# INT_SIZE = 8
# ADD_OP = "add      "
# SYM_OP = "sym      "
# BYE_OP =  "bye      "
# SUB_OP = "sub      "
# STOP_SERVER_OP = "stop    "
# PORT = 8000
# SERVER_ADDRESS = "localhost"

class ClientStub:
    def __init__(self, host, port) -> None:
        self._host = host
        self._port = port
        self.socket = Socket.create_client_connection(self._host, self._port)
    # ------------------- conencting to socket ---------------------
    #def connect(self) -> None:
    #    self.current_connection = socket.socket()
    #    self.current_connection.connect((self._host, self._port))
    # ------------------- executing actions ------------------------
    # def add(self) -> None:
    #     """
    #     Asks the user two integer numbers and use the stubs stubs to add them
    #     """
    #     print("Add two numbers")
    #     a = int(input("a: "))
    #     b = int(input("b: "))
    #     res = self.exec_add(a,b)
    #     print("the result is", res)
    #
    # def subtract(self) -> None:
    #     """
    #     Asks the user two integer numbers and use the stubs stubs to subtract them
    #     """
    #     print("Subtract two numbers")
    #     a = int(input("a: "))
    #     b = int(input("b: "))
    #     res = self.exec_subtract(a,b)
    #     print("the result is", res)
    #
    # def sym(self) -> None:
    #     """
    #     Asks the user for an integer number and uses the stubs stubs to compute its symmetric
    #     """
    #     print("The symmetric of a number")
    #     a = int(input("a: "))
    #     res = self.exec_sym(a)
    #     print("the result is", res)
    #
    # def stop_server(self):
    #     self.exec_stop_server()
    #
    # def stop_client(self):
    #     self.exec_stop_client()


    #---------------------------------- sending info via sockets ------------------

    # def receive_int(self, n_bytes: int) -> int:
    #     """
    #     :param n_bytes: The number of bytes to read from the current connection
    #     :return: The next integer read from the current connection
    #     """
    #     data = self.current_connection.recv(n_bytes)
    #     return int.from_bytes(data, byteorder='big', signed=True)
    #
    # def send_int(self, value: int, n_bytes: int) -> None:
    #     """
    #     :param value: The integer value to be sent to the current connection
    #     :param n_bytes: The number of bytes to send
    #     """
    #     self.current_connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))
    #
    # def receive_str(self, n_bytes: int) -> str:
    #     """
    #     :param n_bytes: The number of bytes to read from the current connection
    #     :return: The next string read from the current connection
    #     """
    #     data = self.current_connection.recv(n_bytes)
    #     return data.decode()
    #
    # def send_str(self, value: str) -> None:
    #     """
    #     :param value: The string value to send to the current connection
    #     """
    #     self.current_connection.send(value.encode())

    # Operação de adição: envia sinal que vai adicionar, envia inteiros, espera resultado
    def exec_add(self, a: int, b: int) -> int:
        """
        Read two integers from the current open connection, adds them up,
        and send the result back through the connection.
        """
        if self.socket.current_connection is None:
            self.socket = Socket.create_client_connection(self._host, self._port)
            #self.socket.connect()
        self.socket.send_str(client.ADD_OP)
        self.socket.send_int(a, client.INT_SIZE)
        self.socket.send_int(b, client.INT_SIZE)
        return self.socket.receive_int(client.INT_SIZE)

    # Operação de subtração: envia sinal que vai subtrair, envia inteiros, espera resultado
    def exec_subtract(self, a: int, b: int) -> int:
        """
        Read two integers from the current open connection, adds them up,
        and send the result back through the connection.
        """
        if self.socket.current_connection is None:
            self.socket = Socket.create_client_connection(self._host, self._port)
            #self.socket.connect()
        self.socket.send_str(client.SUB_OP)
        self.socket.send_int(a, client.INT_SIZE)
        self.socket.send_int(b, client.INT_SIZE)
        return self.socket.receive_int(client.INT_SIZE)

    def exec_sym(self, a: int) -> int:
        """
        Read one integer from the current open connection, computes its
        symmetric, and send the result back to the connection
        """
        if self.socket.current_connection is None:
            # Reconnection!
            self.socket = Socket.create_client_connection(self._host, self._port)

        self.socket.send_str(client.SYM_OP)
        self.socket.send_int(a, client.INT_SIZE)
        return self.socket.receive_int(client.INT_SIZE)

    def exec_matrix_sum(self,a: list, b: list):
        if self.socket.current_connection is None:
            # Reconnection!
            self.socket = Socket.create_client_connection(self._host, self._port)
        self.socket.send_str(client.MATRIX_OP)
        self.socket.send_obj(a,client.INT_SIZE)
        self.socket.send_obj(b,client.INT_SIZE)
        return self.socket.receive_obj(client.INT_SIZE)

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