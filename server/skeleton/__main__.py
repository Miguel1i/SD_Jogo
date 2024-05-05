from server_impl.gamemech import GameMech
from server_impl import GRID_X, GRID_Y
from skeleton.server_skeleton import GameServerSkeleton


def main():
    gamemech = GameMech(GRID_X, GRID_Y)
    skeleton = GameServerSkeleton(gamemech)
    skeleton.run()


if __name__ == "__main__":
    main()
