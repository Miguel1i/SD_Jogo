from stub.client_stub import ClientStub
from stub import SERVER_ADDRESS, PORT, GRID_SIZE
import pygame
from game import Game


def main():
    pygame.init()
    client_stub: ClientStub = ClientStub(SERVER_ADDRESS, PORT)
    game: Game = Game(client_stub, GRID_SIZE)
    game.run()


if __name__ == "__main__":
    main()
