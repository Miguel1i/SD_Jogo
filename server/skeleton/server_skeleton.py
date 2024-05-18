import logging
from socket_impl.sockets import Socket
from server_impl import LOG_FILENAME, PORT, SERVER_ADDRESS, LOG_LEVEL
from skeleton.server_shared_state import ServerSharedState
import client_server


class GameServerSkeleton:
    """
    Esqueleto de um servidor de jogo.
    Atributos:
        shared_state: ServerSharedState - estado partilhado entre os clientes
    Métodos:
        __init__: None - construtor
        run: None - executa o servidor
    """

    def __init__(self, shared_state: ServerSharedState) -> None:
        """
        Construtor da classe GameServerSkeleton.
        :param shared_state: ServerSharedState - estado partilhado entre os clientes
        """
        logging.basicConfig(filename=LOG_FILENAME,
                            level=LOG_LEVEL,
                            format='%(asctime)s (%(levelname)s): %(message)s')
        self.shared_state: ServerSharedState = shared_state

    # ------------------- server execution -------------------------------------
    def run(self) -> None:
        """
        Executa o servidor.
        :return: None
        """
        socket = Socket.create_server_connection(SERVER_ADDRESS, PORT)
        logging.info("Waiting for clients to connect on port " + str(socket.port))
        keep_running = True
        while keep_running:
            current_connection, address = socket.server_connect()
            logging.debug("Client " + str(address) + " just connected")
            client_server.ClientThread(self.shared_state, current_connection, address).start()
        self.socket.close()
        logging.info("Server stopped")
