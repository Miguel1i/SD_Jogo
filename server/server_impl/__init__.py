# Operations
QUADX_OP = "quad_x  "
QUADY_OP = "quad_y  "
SCORE_OP = "score   "
TIME_OP = "time    "
DETERMINE_OP = "det_egg "
BYE_OP = "bye     "
WINNER_OP = "winner  "
CHECK_COLLISION_OP = "check   "
ADD_PLAYER_OP = "add_play"
SET_PLAYER_OP = "set_play"
EXECUTE = "execute "
GET_NR_EGGS_OP = "get_eggs"
ADD_EGG_OP = "add_egg "
STOP_SERVER_OP = "stop    "
CALC_EGGS = "calceggs "
GET_BUSHES_OP = "getbush "
UPDATE_EGGS_OP = "updeggs "
UPDATE_PLAYERS_OP = "updplay "
START_GAME = "start   "
# Constants
COMMAND_SIZE = 9
INT_SIZE = 8
LOG_FILENAME = "server.log"
LOG_LEVEL = 1
# Game
GRID_X: int = 20
GRID_Y: int = 20
MATCH_TIME: int = 180
MAX_POINTS: int = 30
EGG_POSITIVE: str = "assets/Sprites/egg_positive.png"
EGG_NEGATIVE: str = "assets/Sprites/egg_negative.png"
GOLDEN_EGG: str = "assets/Sprites/golden_egg.png"
GAME_TICK: int = 10
SPAWN_POINT_A: tuple = (5, 5)
SPAWN_POINT_B: tuple = (6, 5)
PLAYER_1: str = "assets/Sprites/player_1.png"
PLAYER_2: str = "assets/Sprites/player_2.png"
MAX_CLIENTS: int = 2
# Connection
PORT = 35000
SERVER_ADDRESS = "localhost"
