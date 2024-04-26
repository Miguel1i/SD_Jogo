import logging

import server_impl as server
from server_impl.mathserver import MathServer

from server_impl.gamemech import GameMech
from socket_impl.sockets import Socket
from server_impl import LOG_FILENAME, PORT, SERVER_ADDRESS, LOG_LEVEL


import client_server


class GameServerSkeleton:
    def __init__(self, gamemech: GameMech) -> None:
        """
        Creates a client given the server server to use
        """
        # Keeps information about the execution of the program
        logging.basicConfig(filename=LOG_FILENAME,
                            level=LOG_LEVEL,
                            format='%(asctime)s (%(levelname)s): %(message)s')

        self.gamemech = gamemech

    # ------------ execution of the service ----------------------------------------

    #    def add(self, a: int, b: int) -> int:
    #        return a + b
    # ------------ sending data to socket .........................................
    # Enviar e receber inteiros e strings através do socket
    # def process_add(self) -> None:
    #    a = self.socket.receive_int(server.INT_SIZE)
    #    b = self.socket.receive_int(server.INT_SIZE)
    #    result = self.mathserver.add(a, b)
    #    self.socket.send_int(result, server.INT_SIZE)

    # ------------ execution of the service ----------------------------------------
    #   def sym(self,a: int) -> int:
    #       return -a
    # ------------ sending data to socket .........................................
    # def process_sym(self) -> None:
    #    a = self.socket.receive_int(server.INT_SIZE)
    #    result = self.mathserver.sym(a)
    #    self.socket.send_int(result, server.INT_SIZE)

    # ------------ execution of the service ----------------------------------------
    #   def subtract(self, a: int, b: int) -> int:
    #       return a - b
    # ------------ sending data to socket .........................................
    # def process_subtract(self) -> None:
    #    a = self.socket.receive_int(server.INT_SIZE)
    #    b = self.socket.receive_int(server.INT_SIZE)
    #    result = self.mathserver.subtract(a, b)
    #    self.socket.send_int(result, server.INT_SIZE)
    # ------- analysis of the type of the message sent ----------------------
    # def dispatch_request(self) -> (bool, bool):
    #    """
    #    Calls process functions based on type of request.
    #    """
    #    request_type = self.socket.receive_str(server.COMMAND_SIZE)
    #    print(request_type)
    #    keep_running = True
    #    last_request = False
    #    if request_type == server.ADD_OP:
    #        logging.info("Add operation requested")
    #        self.process_add()
    #    elif request_type == server.SYM_OP:
    #        logging.info("Symetric operation requested")
    #        self.process_sym()
    #    elif request_type == server.SUB_OP:
    #        logging.info("Subtract operation requested")
    #        self.process_subtract()
    #    elif request_type == server.BYE_OP:
    #        last_request = True
    #    elif request_type == server.STOP_SERVER_OP:
    #        last_request = True
    #        keep_running = False
    #    return keep_running, last_request

    # ------------------- server execution -------------------------------------
    def run(self) -> None:
        """
        Runs the server server until the client sends a "terminate" action
        """
        socket = Socket.create_server_connection(SERVER_ADDRESS, PORT)
        logging.info("Waiting for clients to connect on port " + str(socket.port))
        keep_running = True
        # While keep_running, get connections and then interact with the client connected
        while keep_running:
            current_connection, address = socket.server_connect()
            logging.debug("Client " + str(address) + " just connected")
            client_server.ClientThread(self.gamemech, current_connection).start()
            # While client connected, wait for its demmands and dispatch the requests
            # with current_connection:
            #    last_request = False
            #    #If it is not the last request receive the request
            #    while not last_request:
            #        keep_running, last_request = self.dispatch_request()
            #    #If it is the last request, client is disconnecting...
            #    logging.debug("Client " + str(address) + " disconnected")
        # If it is not keep_running than socket must be closed...
        self.socket.close()
        logging.info("Server stopped")

