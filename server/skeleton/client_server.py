from sys import getsizeof
from threading import Thread
import logging
import server_impl as server
from server_impl.gamemech import GameMech


class ClientThread(Thread):
    def __init__(self, gamemech: GameMech, current_connection, address):
        self.current_connection = current_connection
        self.gamemech: GameMech = gamemech
        self.address = address
        Thread.__init__(self)

    def process_update(self):
        pass

    def process_get_nr_quad_x(self):
        nr_x: int = self.gamemech.get_nr_x()
        self.current_connection.send_int(nr_x, server.INT_SIZE)

    def process_get_nr_quad_y(self):
        nr_y: int = self.gamemech.get_nr_y()
        self.current_connection.send_int(nr_y, server.INT_SIZE)

    def dispatch_request(self) -> (bool, bool):
        """
        Calls process functions based on type of request.
        """
        request_type = self.current_connection.receive_str(server.COMMAND_SIZE)
        # print(request_type)
        keep_running = True
        last_request = False
        # if request_type == server.UPDATE_OP:
        #     logging.info("Update operation requested" + str(self.address))
        #     self.process_update()
        if request_type == server.BYE_OP:
            last_request = True
        elif request_type == server.STOP_SERVER_OP:
            last_request = True
            keep_running = False
        elif request_type == server.QUADX_OP:
            logging.info("Quad x operation requested" + str(self.address))
            self.process_get_nr_quad_x()
        elif request_type == server.QUADY_OP:
            logging.info("Quad y operation requested" + str(self.address))
            self.process_get_nr_quad_y()

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
