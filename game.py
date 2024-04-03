import pygame
from gamemech import GameMech
from constants import GRID_SIZE, GRID_X, GRID_Y, GAME_TICK, PLAYER_1, PLAYER_2, FONT, FONT_SIZE, WHITE, TRANSPARENT, \
    GAME_ICON
import player
import player_key
import egg
import grass
import bush


class Game(object):

    def __init__(self, game_mechanics: GameMech):
        # Screen and background
        self.height: None = None
        self.width: None = None
        self.screen: None = None
        self.background: None = None
        # Clock
        self.clock: None = None
        # Grid
        self.grid_size: None = None
        self.grid_surface: None = None
        self.game_settings()
        # Other attributes
        self.gm: GameMech = game_mechanics
        self.eggs: pygame.sprite.LayeredDirty = pygame.sprite.LayeredDirty()
        self.bushes: pygame.sprite.Group = pygame.sprite.Group()
        self.grass: pygame.sprite.Group = pygame.sprite.Group()
        self.players: pygame.sprite.LayeredDirty = pygame.sprite.LayeredDirty()
        pygame.display.update()

    def game_settings(self):
        self.width, self.height = GRID_X * GRID_SIZE, GRID_Y * GRID_SIZE
        # Screen and background
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        game_icon = pygame.image.load(GAME_ICON)
        pygame.display.set_icon(game_icon)
        # Grid
        self.grid_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.grid_surface.fill(TRANSPARENT)
        self.grid_size = GRID_SIZE
        self.draw_grid(self.grid_surface, self.width, self.height, self.grid_size, (2, 150, 72))
        # Name of the game
        pygame.display.set_caption("Hop to It!")
        # Clock
        self.clock = pygame.time.Clock()

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_panel(self, panel_text, x, y):
        font = pygame.font.SysFont(FONT, FONT_SIZE)
        text_width, text_height = font.size(panel_text)
        panel_surface = pygame.Surface((max(self.width, text_width), max(20, text_height)), pygame.SRCALPHA)
        panel_surface.fill(TRANSPARENT)
        self.screen.blit(panel_surface, (x, y))
        self.draw_text(panel_text, font, WHITE, x, y)
        pygame.display.update(pygame.Rect(x, y, max(self.width, text_width), max(20, text_height)))

    def draw_scoreboard(self):
        for jogador in self.players:
            x = self.width // 2 - 220 if jogador.get_id() == 0 else self.width // 2 + 110
            panel_text = f"{jogador.get_name()}: {self.gm.get_score(jogador.get_id())}"
            self.draw_panel(panel_text, x, 5)

    def draw_timer(self):
        panel_text = self.gm.calc_time()
        self.draw_panel(panel_text, self.width // 2 - 25, 5)

    @staticmethod
    def draw_grid(surface, width: int, height: int, size: int, colour: tuple):

        # Draw horizontal lines
        for pos in range(0, height, size):
            pygame.draw.line(surface, colour, (0, pos), (width, pos))
        # Draw vertical lines
        for pos in range(0, width, size):
            pygame.draw.line(surface, colour, (pos, 0), (pos, height))

    def create_bushes(self, bush_size: int):

        for x in range(0, self.width, bush_size):
            for y in range(0, self.height, bush_size):
                if x in (0, self.width - bush_size) or y in (0, self.height - bush_size):
                    arbusto = bush.Bush(x, y, 0, bush_size, self.bushes)
                    self.bushes.add(arbusto)

    def create_grass(self, grass_size: int):

        for x in range(0, self.width, grass_size):
            for y in range(0, self.height, grass_size):
                erva = grass.Grass(x, y, grass_size, self.grass)
                self.grass.add(erva)

    def create_players(self, size: int) -> None:

        player_b = player.Player(5, 5, size, 0, "Henrique", PLAYER_1, self.players)
        player_c = player_key.PlayerKEY(6, 5, size, 1, "Miguel", PLAYER_2, self.players)
        self.players.add(player_b, player_c)
        self.gm.add_player(player_b)
        self.gm.add_player(player_c)

    def create_eggs(self, egg_size: int, number_eggs: int) -> None:

        for _ in range(number_eggs):
            new_id = 0
            if self.eggs:
                new_id = max([ovo.get_id() for ovo in self.eggs]) + 1
            pos_x, pos_y = self.gm.calculate_egg_spawn(number_eggs)
            skin, value = self.gm.determine_egg()
            new_egg = egg.Egg(pos_x, pos_y, egg_size, skin, new_id, value, self.eggs)
            self.eggs.add(new_egg)
            self.gm.add_egg(new_egg)

    def check_collisions(self):
        for jogador in self.players:
            for ovo in self.eggs:
                if pygame.sprite.collide_rect(jogador, ovo):
                    self.gm.update_score(jogador.get_id(), ovo.get_value())
                    ovo.kill()
                    self.eggs.remove(ovo)
                    self.gm.pop_egg(ovo, jogador)
                    self.create_eggs(self.grid_size, 1)
                    self.eggs.update(self, self.gm)
                    rect_1 = self.eggs.draw(self.screen)
                    pygame.display.update(rect_1)

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

            self.grass.draw(self.screen)

            self.players.update(self, self.gm)
            rects = self.players.draw(self.screen)

            self.bushes.update(dt)
            self.bushes.draw(self.screen)

            self.eggs.draw(self.screen)

            self.screen.blit(self.grid_surface, (0, 0))
            self.check_collisions()

            if self.gm.winner():
                end_game = True

            self.draw_scoreboard()
            self.draw_timer()

            pygame.display.update(rects)

        return None


def main():
    pygame.init()
    game_mechanics = GameMech(GRID_X, GRID_Y)
    game = Game(game_mechanics)
    game.run()


if __name__ == "__main__":
    main()
