from threading import Thread
import logging
import server_impl as server
import numpy as np
import ast
from server_impl.gamemech import GameMech


class ClientThread(Thread):
    def __init__(self, gamemech, current_connection, address):
        self.current_connection = current_connection
        self.gamemech = gamemech
        self.address = address
        Thread.__init__(self)

    def process_update(self):
        pass

    """def process_add(self) -> None:
        a = self.current_connection.receive_int(server.INT_SIZE)
        b = self.current_connection.receive_int(server.INT_SIZE)
        result = self.mathserver.add(a, b)
        self.current_connection.send_int(result, server.INT_SIZE)

    def process_sym(self) -> None:
        a = self.current_connection.receive_int(server.INT_SIZE)
        result = self.mathserver.sym(a)
        self.current_connection.send_int(result, server.INT_SIZE)

    def process_subtract(self) -> None:
        a = self.current_connection.receive_int(server.INT_SIZE)
        b = self.current_connection.receive_int(server.INT_SIZE)
        result = self.mathserver.subtract(a, b)
        self.current_connection.send_int(result, server.INT_SIZE)


    def process_matrix_sum(self) -> None:
        a = self.current_connection.receive_obj(server.INT_SIZE)
        b = self.current_connection.receive_obj(server.INT_SIZE)
        result = self.mathserver.matrix_add(a,b)
        self.current_connection.send_obj(result,server.INT_SIZE)
"""

    def dispatch_request(self) -> (bool, bool):
        """
        Calls process functions based on type of request.
        """
        request_type = self.current_connection.receive_str(server.COMMAND_SIZE)
        # print(request_type)
        keep_running = True
        last_request = False
        if request_type == server.UPDATE_OP:
            logging.info("Update operation requested" + str(self.address))
            self.process_update()
        elif request_type == server.BYE_OP:
            last_request = True
        elif request_type == server.STOP_SERVER_OP:
            last_request = True
            keep_running = False
        return keep_running, last_request

    def run(self):
        # While client connected, wait for its demmands and dispatch the requests
        #with self.current_connection:
        last_request = False
        #If it is not the last request receive the request
        while not last_request:
            keep_running, last_request = self.dispatch_request()
        #If it is the last request, client is disconnecting...
        logging.debug("Client " + str(self.address) + " disconnected")
