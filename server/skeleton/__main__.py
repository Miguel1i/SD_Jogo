from server_impl.gamemech import GameMech
from server_skeleton import GameServerSkeleton
def main():
    gamemech = GameMech()
    skeleton = GameServerSkeleton(gamemech)
    skeleton.run()


if __name__ == "__main__":
    main()
