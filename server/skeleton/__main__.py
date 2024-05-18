from server_impl.gamemech import GameMech
from server_impl import GRID_X, GRID_Y
from skeleton.server_skeleton import GameServerSkeleton
from skeleton.server_shared_state import ServerSharedState


def main():
    """
    Função principal do servidor.
    :return: None
    """
    gamemech: GameMech = GameMech(GRID_X, GRID_Y)
    server_state: ServerSharedState = ServerSharedState(gamemech)
    skeleton: GameServerSkeleton = GameServerSkeleton(server_state)
    skeleton.run()


if __name__ == "__main__":
    main()
