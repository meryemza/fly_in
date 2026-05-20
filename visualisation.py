import pygame
from Data import Data
from simulation import Simulation


class Visualisation:
    """
    Pygame-based visualization system for the drone simulation.
    Responsible for:
    Rendering zones and connections
    Displaying drone positions
    Handling camera movement
    Updating the simulation visually turn by turn"""

    def __init__(self, data: Data, simulation: Simulation) -> None:
        self.zones = data.zones
        self.drones = data.drones
        self.connections = data.connections
        self.size = 30
        self.offset_x = 120
        self.offset_y = 120
        self.scale = 110
        self.simulation = simulation
        self.nb_turn = 0

    def run(self) -> None:
        """Starts the visualization loop and handles user interaction."""

        pygame.init()

        info = pygame.display.Info()
        x_screen = info.current_w
        y_screen = info.current_h
        screen = pygame.display.set_mode((x_screen, y_screen))
        pygame.display.set_caption("Fly_in")

        run = True
        self.draw_all(screen)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.offset_x = self.offset_x - 20
                        self.draw_all(screen)
                    if event.key == pygame.K_RIGHT:
                        self.offset_x = self.offset_x + 20
                        self.draw_all(screen)
                    if event.key == pygame.K_UP:
                        self.offset_y = self.offset_y - 20
                        self.draw_all(screen)
                    if event.key == pygame.K_DOWN:
                        self.offset_y = self.offset_y + 20
                        self.draw_all(screen)
                    if event.key == pygame.K_a:
                        if not self.simulation.finish:
                            self.nb_turn += 1
                            screen.fill(color=(90, 0, 30))
                            font2 = pygame.font.SysFont(None, 30)
                            txt = font2.render(
                                f"nb_turn: {self.nb_turn}", True,
                                (255, 255, 255)
                            )
                            screen.blit(txt, (40, 40))
                            self.draw_connections(screen)
                            self.draw_zone(screen)
                            self.simulation.move_drones()
                            self.draw_drone(screen)
                            pygame.display.flip()

    def draw_connections(self, screen: pygame.Surface) -> None:
        """Draws all connections between zones on the screen."""

        for con in self.connections:
            x1 = self.zones[con.zone1].x * self.scale + self.offset_x
            y1 = self.zones[con.zone1].y * self.scale + self.offset_y
            x2 = self.zones[con.zone2].x * self.scale + self.offset_x
            y2 = self.zones[con.zone2].y * self.scale + self.offset_y
            pygame.draw.line(screen, (150, 150, 150), (x1, y1), (x2, y2), 2)

    def draw_zone(self, screen: pygame.Surface) -> None:
        """Draws all zones with their names and colors.
        if a zone color is invalid, a default pink color is used."""
        font = pygame.font.SysFont(None, 17)
        for zon in self.zones.values():
            x = zon.x * self.scale + self.offset_x
            y = zon.y * self.scale + self.offset_y
            try:
                color = pygame.Color(zon.color)
            except Exception:
                color = pygame.Color("pink")
            pygame.draw.circle(screen, color, (x, y), self.size)
            place_txt_x = x - 20
            place_txt_y = y + self.size // 2 + 20
            txt = font.render(zon.name, True, (255, 255, 255))
            screen.blit(txt, (place_txt_x, place_txt_y))

    def draw_drone(self, screen: pygame.Surface) -> None:
        d = pygame.image.load("drone.png")
        """Draws drones on the map.
            Normal drones are displayed inside their current zone
            Drones in restricted-zone transit are displayed between zones"""

        for drone in self.drones:
            if drone.in_transit:
                if drone.next_zone is not None:
                    x = (
                        (self.zones[drone.current_zone].x + drone.next_zone.x)
                        / 2
                        * self.scale
                        + self.offset_x
                        - 30
                    )
                    y = (
                        (self.zones[drone.current_zone].y + drone.next_zone.y)
                        / 2
                        * self.scale
                        + self.offset_y
                        - 28
                    )
            else:
                x = (
                    (self.zones[drone.current_zone].x * self.scale)
                    + self.offset_x - 30)
                y = (
                    (self.zones[drone.current_zone].y * self.scale)
                    + self.offset_y - 28)
            d = pygame.transform.scale(d, (60, 60))
            screen.blit(d, (x, y))

    def draw_all(self, screen: pygame.Surface) -> None:
        screen.fill(color=(90, 0, 30))
        font2 = pygame.font.SysFont(None, 30)
        txt = font2.render(f"nb_turn: {self.nb_turn}", True, (255, 255, 255))
        screen.blit(txt, (40, 40))
        self.draw_connections(screen)
        self.draw_zone(screen)
        self.draw_drone(screen)
        pygame.display.flip()
