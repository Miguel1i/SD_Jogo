from server_impl.gamemech import GameMech
from server_impl import GRID_X, GRID_Y
from skeleton.server_skeleton import GameServerSkeleton
from skeleton.server_shared_state import ServerSharedState


def main():
    gamemech = GameMech(GRID_X, GRID_Y)
    skeleton = GameServerSkeleton(gamemech)
    skeleton.run()
    # gamemech = GameMech(GRID_X, GRID_Y)
    # server_state = ServerSharedState(gamemech)
    # skeleton = GameServerSkeleton(server_state)
    # skeleton.run()


if __name__ == "__main__":
    main()
