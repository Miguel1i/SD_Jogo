import pygame
import bush
from gamemech import GameMech
import player
import grass
import egg
from constants import GRID_SIZE, GRID_X, GRID_Y, GAME_TICK, PLAYER_1, PLAYER_2, EGG_NEGATIVE, EGG_POSITIVE
import player_key


class Game(object):

    def __init__(self, game_mechanics: GameMech, nr_x: int = 20, nr_y: int = 20, size: int = 20):
        self.width, self.height = nr_x * size, nr_y * size
        # Screen and background
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        # Grid
        self.grid_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.grid_surface.fill((0, 0, 0, 0))
        self.grid_size = size
        self.draw_grid(self.grid_surface, self.width, self.height, self.grid_size, (2, 150, 72))
        # Name of the game
        pygame.display.set_caption("Hop to It!")
        # Clock
        self.clock = pygame.time.Clock()
        # Other attributes
        self.gm = game_mechanics
        self.eggs = pygame.sprite.LayeredDirty()
        self.players = pygame.sprite.LayeredDirty()
        pygame.display.update()

    @staticmethod
    def draw_grid(surface, width: int, height: int, size: int, colour: tuple):

        # Draw horizontal lines
        for pos in range(0, height, size):
            pygame.draw.line(surface, colour, (0, pos), (width, pos))
        # Draw vertical lines
        for pos in range(0, width, size):
            pygame.draw.line(surface, colour, (pos, 0), (pos, height))

    def create_bushes(self, bush_size: int):

        # Create Wall (sprites) around world
        self.bushes = pygame.sprite.Group()
        for x in range(0, self.width, bush_size):
            for y in range(0, self.height, bush_size):
                if x in (0, self.width - bush_size) or y in (0, self.height - bush_size):
                    b = bush.Bush(x, y, 0, bush_size, self.bushes)
                    self.bushes.add(b)

    def create_grass(self, grass_size: int):
        self.grass = pygame.sprite.Group()

        for x in range(0, self.width, grass_size):
            for y in range(0, self.height, grass_size):
                g = grass.Grass(x, y, grass_size, self.grass)
                self.grass.add(g)

    def create_players(self, size: int) -> None:

        player_b = player.Player(5, 5, size, 0, "Henrique", PLAYER_1, self.players)
        player_c = player_key.PlayerKEY(6, 5, size, 1, "Miguel", PLAYER_2, self.players)

        self.players.add(player_b)
        self.players.add(player_c)
        self.gm.add_player(player_b)
        self.gm.add_player(player_c)

    def create_eggs(self, egg_size: int, number_eggs: int) -> None:

        for _ in range(number_eggs):
            new_id = len(self.eggs) + 1
            pos_x, pos_y = self.gm.calculate_egg_spawn(number_eggs, new_id)
            new_egg = egg.Egg(pos_x, pos_y, egg_size, EGG_POSITIVE, new_id, self.eggs)
            self.eggs.add(new_egg)

    def check_collisions(self):
        for player in self.players:
            for egg in self.eggs:
                if pygame.sprite.collide_rect(player, egg):
                    player.set_score(egg.value)
                    egg.kill()
                    self.eggs.remove(egg)
                    self.gm.pop_egg(egg, player)
                    self.create_egg()
                    self.eggs.update(self, self.gm)
                    rect_1 = self.eggs.draw(self.screen)
                    pygame.display.update(rect_1)

    def create_egg(self):
        new_id = len(self.eggs) + 1
        x, y = self.gm.calculate_egg_spawn(1, new_id)
        new_egg = egg.Egg(x, y, self.grid_size, EGG_NEGATIVE, new_id, self.eggs)
        self.eggs.add(new_egg)

    def run(self):
        self.create_eggs(self.grid_size, 5)
        self.create_grass(self.grid_size)
        self.create_bushes(self.grid_size)
        self.create_players(self.grid_size)

        end_game = False
        while not end_game:
            dt = self.clock.tick(GAME_TICK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_game = True

            # Draw grass sprites onto the screen
            self.grass.draw(self.screen)

            self.players.update(self, self.gm)
            rects = self.players.draw(self.screen)

            self.bushes.update(dt)
            self.bushes.draw(self.screen)

            self.eggs.draw(self.screen)

            # Blit the grid surface onto the screen
            self.screen.blit(self.grid_surface, (0, 0))

            self.check_collisions()

            if self.gm.winner():
                end_game = True
            pygame.display.update(rects)

        return None


def main():
    pygame.init()
    game_mechanics = GameMech(GRID_X, GRID_Y)
    game = Game(game_mechanics, GRID_X, GRID_Y, GRID_SIZE)
    game.run()


if __name__ == "__main__":
    main()
