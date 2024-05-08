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

    def process_get_score(self):
        player_id: int = self.current_connection.receive_int(server.INT_SIZE)
        score = self.gamemech.get_score(player_id)
        self.current_connection.send_int(score, server.INT_SIZE)

    def process_time(self):
        time: str = self.gamemech.calc_time()
        self.current_connection.send_int(getsizeof(time), server.INT_SIZE)
        self.current_connection.send_str(time)

    def process_determine_egg(self):
        egg: tuple = self.gamemech.determine_egg()
        self.current_connection.send_int(getsizeof(egg), server.INT_SIZE)
        self.current_connection.send_obj(egg, getsizeof(egg))

    def process_winner(self):
        winner: str = self.gamemech.winner()
        self.current_connection.send_int(getsizeof(winner), server.INT_SIZE)
        self.current_connection.send_str(winner)

    def process_check_collision(self):
        collision: tuple = self.gamemech.check_egg_collison()
        self.current_connection.send_int(getsizeof(collision), server.INT_SIZE)
        self.current_connection.send_obj(collision, getsizeof(collision))

    def process_calc_eggs(self):
        nr_eggs: int = self.gamemech.calculate_nr_eggs()
        coords: tuple = self.gamemech.calculate_egg_spawn(nr_eggs)
        self.current_connection.send_int(getsizeof(coords), server.INT_SIZE)
        self.current_connection.send_obj(coords, getsizeof(coords))

    def process_execute(self):
        player_id: int = self.current_connection.receive_int(server.INT_SIZE)
        direction: str = self.current_connection.receive_str(server.COMMAND_SIZE)
        new_position = self.gamemech.execute(player_id, direction)
        self.current_connection.send_int(getsizeof(new_position), server.INT_SIZE)
        self.current_connection.send_obj(new_position, getsizeof(new_position))

    def process_get_nr_eggs(self):
        nr_eggs = self.gamemech.calculate_nr_eggs()
        self.current_connection.send_int(nr_eggs, server.INT_SIZE)

    def process_add_egg(self):
        egg_id = self.current_connection.receive_int(server.INT_SIZE)
        egg_pos_size = self.current_connection.receive_int(server.INT_SIZE)
        egg_x, egg_y = self.current_connection.receive_obj(egg_pos_size)
        egg_value = self.current_connection.receive_int(server.INT_SIZE)
        self.gamemech.add_egg(egg_id, (egg_x, egg_y), egg_value)

    def process_tick(self):
        tick: int = self.current_connection.recieve_int(server.INT_SIZE)
        self.current_connection.send_int(tick, server.INT_SIZE)

    def process_set_player(self):
        size = self.current_connection.receive_int(server.INT_SIZE)
        player_name = self.current_connection.receive_str(size)
        res: tuple = self.gamemech.set_player(player_name)
        self.current_connection.send_int(getsizeof(res), server.INT_SIZE)
        self.current_connection.send_obj(res, getsizeof(res))

    def process_add_player(self):
        size = self.current_connection.receive_int(server.INT_SIZE)
        player_name = self.current_connection.receive_str(size)
        self.current_connection.send_str("ok")
        player_id = self.current_connection.receive_int(server.INT_SIZE)
        x_pos, y_pos = self.current_connection.receive_obj(server.INT_SIZE)
        player_score = self.current_connection.receive_int(server.INT_SIZE)
        self.gamemech.add_player(player_id, player_name, (x_pos, y_pos), player_score)


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
        elif request_type == server.SET_PLAYER_OP:
            logging.info("Set player operation requested" + str(self.address))
            self.process_set_player()
        elif request_type == server.ADD_EGG_OP:
            logging.info("Add egg operation requested" + str(self.address))
            self.process_add_egg()
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
        elif request_type == server.DETERMINE_OP:
            logging.info("Determine egg operation requested" + str(self.address))
            self.process_determine_egg()
        elif request_type == server.WINNER_OP:
            logging.info("Winner operation requested" + str(self.address))
            self.process_winner()
        elif request_type == server.GAME_TICK:
            logging.info("Tick operation requested" + str(self.address))
            self.process_tick()
        elif request_type == server.CHECK_COLLISION_OP:
            logging.info("Check collision operation requested" + str(self.address))
            self.process_check_collision()
        elif request_type == server.CALC_EGGS:
            logging.info("Calculated eggs operation requested" + str(self.address))
            self.process_calc_eggs()
        elif request_type == server.EXECUTE:
            logging.info("Execute operation requested" + str(self.address))
            self.process_execute()
        elif request_type == server.GET_NR_EGGS_OP:
            logging.info("Get nr eggs operation requested" + str(self.address))
            self.process_get_nr_eggs()
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
