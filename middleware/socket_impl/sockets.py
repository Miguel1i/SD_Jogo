import socket
import json


class Socket:
    """
    Classe que representa uma ligação por sockets.

    Atributos:
        _current_connection: socket - ligação atual
        _port: int - porta

    Métodos:
        get_address: tuple - obtém o endereço
        receive_int: int - recebe um inteiro
        send_int: None - envia um inteiro
        receive_str: str - recebe uma string
        send_str: None - envia uma string
        send_obj: None - envia um objeto
        receive_obj: object - recebe um objeto
        close: None - fecha a ligação
        server_connect: tuple - conecta-se ao servidor
        create_server_connection: Socket - cria uma ligação como servidor
        create_client_connection: Socket - cria uma ligação como cliente
    """

    def __init__(self, connection, port: int):
        """
        Construtor da classe Socket.
        :param connection: socket - ligação
        :param port: int - porta
        """
        self._current_connection = connection
        self._port = port

    @property
    def port(self) -> int:
        """
        Propriedade que obtém a porta.
        :return: int - porta
        """
        return self._port

    def get_address(self) -> tuple:
        """
        Obtém o endereço da ligação.
        :return: tuple - endereço
        """
        return self._current_connection.getpeername()

    @property
    def current_connection(self) -> socket:
        """
        Propriedade que obtém a ligação atual.
        :return: socket - ligação atual
        """
        return self._current_connection

    def receive_int(self, n_bytes: int) -> int:
        """
        Protocolo de comunicação para receber um inteiro.
        :param n_bytes: int - número de bytes
        :return: int - inteiro
        """
        data = self._current_connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_int(self, value: int, n_bytes: int) -> None:
        """
        Protocolo de comunicação para enviar um inteiro.
        :param value: int - valor
        :param n_bytes: int - número de bytes
        :return: None
        """
        self._current_connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_str(self, n_bytes: int) -> str:
        """
        Protocolo de comunicação para receber uma string.
        :param n_bytes: int - número de bytes
        :return: str - string
        """
        data = self._current_connection.recv(n_bytes)
        return data.decode()

    def send_str(self, value: str) -> None:
        """
        Protocolo de comunicação para enviar uma string.
        :param value: str - valor
        :return: None
        """
        self._current_connection.send(value.encode())

    def send_obj(self, value: object, n_bytes: int) -> None:
        """
        Protocolo de comunicação para enviar um objeto.
        :param value: object - valor
        :param n_bytes:  int - número de bytes
        :return:  None
        """
        msg = json.dumps(value)
        size = len(msg)
        self.send_int(size, n_bytes)
        self.send_str(msg)

    def receive_obj(self, n_bytes: int) -> object:
        """
        Protocolo de comunicação para receber um objeto.
        :param n_bytes: int - número de bytes
        :return: object - objeto
        """
        size = self.receive_int(n_bytes)
        obj = self.receive_str(size)
        return json.loads(obj)

    def close(self):
        """
        Fecha a ligação.
        :return: None
        """
        self._current_connection.close()
        self._current_connection = None

    def server_connect(self) -> tuple:
        """
        Conecta-se ao servidor.
        :return: tuple - ligação, endereço
        """
        connection, address = self._current_connection.accept()
        return Socket(connection, self._port), address

    @staticmethod
    def create_server_connection(host: str, port: int):
        """
        Cria uma ligação com o servidor.
        :param host: str - endereço
        :param port: int - porta
        :return: Socket - ligação
        """
        connection = socket.socket()
        connection.bind((host, port))
        connection.listen(1)
        return Socket(connection, port)

    @staticmethod
    def create_client_connection(host: str, port: int):
        """
        Cria uma ligação com o cliente.
        :param host: str - endereço
        :param port: int - porta
        :return: Socket - ligação
        """
        connection = socket.socket()
        connection.connect((host, port))
        return Socket(connection, port)
