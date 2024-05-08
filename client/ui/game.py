import pygame

from ui.constants import GAME_TICK, FONT, FONT_SIZE, WHITE, TRANSPARENT, \
    GAME_ICON, GAME_MUSIC, EGG_COLLECT, CHANEL_MUSIC, CHANEL_EGG, NUMBER_EGGS
from ui.player import Player
import egg
import grass
import bush
from stub.client_stub import ClientStub


class Game(object):

    def __init__(self, client_sub: ClientStub, grid_size: int):
        # Screen and background
        self.width = None
        self.height = None
        self.client_stub = client_sub
        self.screen: None = None
        self.background: None = None
        # Clock
        self.clock: None = None
        # Grid
        self.grid_size: None = None
        self.grid_surface: None = None
        self.game_settings(grid_size)
        # Other attributes
        self.eggs: pygame.sprite.LayeredDirty = pygame.sprite.LayeredDirty()
        self.bushes: pygame.sprite.Group = pygame.sprite.Group()
        self.grass: pygame.sprite.Group = pygame.sprite.Group()
        self.players: pygame.sprite.LayeredDirty = pygame.sprite.LayeredDirty()
        pygame.display.update()

    def game_settings(self, grid_size: int):
        # Screen and background
        self.height: int = self.client_stub.get_nr_quad_y() * grid_size
        self.width: int = self.client_stub.get_nr_quad_x() * grid_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        game_icon = pygame.image.load(GAME_ICON)
        pygame.display.set_icon(game_icon)
        # Grid
        self.grid_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.grid_surface.fill(TRANSPARENT)
        self.grid_size = grid_size
        self.draw_grid(self.grid_surface, self.width, self.height, self.grid_size, (2, 150, 72))
        # Name of the game
        pygame.display.set_caption("Hop to It!")
        # Clock
        self.clock = pygame.time.Clock()
        # Music
        #pygame.mixer.init()
        #self.sound_effect(GAME_MUSIC, 0.2, -1, CHANEL_MUSIC)

    @staticmethod
    def sound_effect(music: str, volume: float, repeat: int, channel: int):
        channel = pygame.mixer.Channel(channel)
        sound = pygame.mixer.Sound(music)
        channel.set_volume(volume)
        channel.play(sound, loops=repeat)

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_panel(self, panel_text, x, y):
        font = pygame.font.Font(FONT, FONT_SIZE)
        text_width, text_height = font.size(panel_text)
        panel_surface = pygame.Surface((max(self.width, text_width), max(20, text_height)), pygame.SRCALPHA)
        panel_surface.fill(TRANSPARENT)
        self.screen.blit(panel_surface, (x, y))
        self.draw_text(panel_text, font, WHITE, x, y)
        pygame.display.update(pygame.Rect(x, y, max(self.width, text_width), max(20, text_height)))

    def draw_scoreboard(self):
        for jogador in self.players:
            x = self.width // 2 - 220 if jogador.get_id() == 0 else self.width // 2 + 110
            panel_text = f"{jogador.get_name()}: {self.client_stub.get_score(jogador.get_id())}"
            self.draw_panel(panel_text, x, 5)

    def draw_timer(self):
        panel_text = self.client_stub.calc_time()
        print(panel_text)
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
        name: str = str(input("Qual é o teu nome? "))
        pos, skin, player_id = self.client_stub.set_player(name)
        player: Player = Player(pos[0], pos[1], size, player_id, name, skin, self.players)
        self.players.add(player)
        self.client_stub.add_player(name, player_id, pos, player.get_score())


    def create_eggs(self, egg_size: int) -> None:
        number_eggs = self.client_stub.get_nr_eggs()
        for _ in range(number_eggs):
            new_id = 0
            if self.eggs:
                new_id = max([ovo.get_id() for ovo in self.eggs]) + 1
            pos_x, pos_y = self.client_stub.calculate_egg_spawn()
            skin, value = self.client_stub.determine_egg()
            new_egg = egg.Egg(pos_x, pos_y, egg_size, skin, new_id, value, self.eggs)
            self.eggs.add(new_egg)
            self.client_stub.add_egg(new_egg)

    def check_collisions(self):
        egg_collision = self.client_stub.check_egg_collison()
        if egg_collision[0]:
            egg_collision[1].kill()
            self.eggs.remove(egg_collision[1])
            self.sound_effect(EGG_COLLECT, 0.5, 0, CHANEL_EGG)
            self.create_eggs(self.grid_size)
            self.eggs.update(self, self.client_stub)
            rect_1 = self.eggs.draw(self.screen)
            pygame.display.update(rect_1)

    def run(self):
        #self.create_eggs(self.grid_size)
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

            self.players.update(self, self.client_stub)
            rects = self.players.draw(self.screen)

            self.bushes.update(dt)
            self.bushes.draw(self.screen)

            #self.eggs.draw(self.screen)

            self.screen.blit(self.grid_surface, (0, 0))
            #self.check_collisions()

            # if self.client_stub.winner() != "False":
            #     end_game = True

            #self.draw_scoreboard()
            self.draw_timer()

            pygame.display.update(rects)


        return None
