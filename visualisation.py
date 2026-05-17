import pygame
from objects.Data import Data


class Visualisation:
    def __init__(self, data: Data, simulation) -> None:
        self.zones = data.zones
        self.drones = data.drones
        self.connections = data.connections
        self.size = 30
        self.offset_x = 120
        self.offset_y = 120
        self.scale = 110
        self.simulation = simulation

    def run(self) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        info = pygame.display.Info()
        x_screen = info.current_w
        y_screen = info.current_h
        screen = pygame.display.set_mode((x_screen, y_screen))
        screen.fill(color=(90, 0, 30))
        pygame.display.set_caption("Fly_in")

        run = True
        start_map = 1
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if start_map:
                    screen.fill(color=(90, 0, 30))
                    self.draw_connections(screen)
                    self.draw_zone(screen)
                    self.draw_drone(screen)
                    pygame.display.flip()
                    start_map = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.offset_x = self.offset_x - 20
                        screen.fill(color=(90, 0, 30))
                        self.draw_connections(screen)
                        self.draw_zone(screen)
                        self.draw_drone(screen)
                        pygame.display.flip()
                    if event.key == pygame.K_RIGHT:
                        self.offset_x = self.offset_x + 20
                        screen.fill(color=(90, 0, 30))
                        self.draw_connections(screen)
                        self.draw_zone(screen)
                        self.draw_drone(screen)
                        pygame.display.flip()
                    if event.key == pygame.K_UP:
                        self.offset_y = self.offset_y - 20
                        screen.fill(color=(90, 0, 30))
                        self.draw_connections(screen)
                        self.draw_zone(screen)
                        self.draw_drone(screen)
                        pygame.display.flip()
                    if event.key == pygame.K_DOWN:
                        self.offset_y = self.offset_y + 20
                        screen.fill(color=(90, 0, 30))
                        self.draw_connections(screen)
                        self.draw_zone(screen)
                        self.draw_drone(screen)
                        pygame.display.flip()

                    if event.key == pygame.K_a:  # check the key exact

                        if not self.simulation.finish:
                            screen.fill(color=(90, 0, 30))
                            self.draw_connections(screen)
                            self.draw_zone(screen)
                            self.simulation.move_drones()
                            self.draw_drone(screen)
                            pygame.display.flip()
                            self.clock.tick(2)

    def draw_connections(self, screen) -> None:
        for con in self.connections:
            x1 = self.zones[con.zone1].x * self.scale + self.offset_x
            y1 = self.zones[con.zone1].y * self.scale + self.offset_y
            x2 = self.zones[con.zone2].x * self.scale + self.offset_x
            y2 = self.zones[con.zone2].y * self.scale + self.offset_y
            pygame.draw.line(screen, (150, 150, 150), (x1, y1), (x2, y2), 2)

    def draw_zone(self, screen) -> None:
        font = pygame.font.SysFont("consolas", 14)
        for zon in self.zones.values():
            x = zon.x * self.scale + self.offset_x
            y = zon.y * self.scale + self.offset_y
            try:
                color = pygame.Color(zon.color)
            except Exception:
                color = pygame.Color("pink")
            pygame.draw.circle(screen, color, (x, y), self.size)
            place_txt_x = x
            place_txt_y = y + self.size // 2 + 20
            txt = font.render(zon.name, True, (255, 255, 255))
            txt_rect = txt.get_rect()
            txt_rect.center = (place_txt_x, place_txt_y)
            screen.blit(txt, txt_rect)

    def draw_drone(self, screen):
        for drone in self.drones:
            if drone.in_transit:
                x = (
                    ((self.zones[drone.current_zone].x + drone.next_zone.x)
                     / 2)
                    * self.scale
                    + self.offset_x
                    - 30
                )
                y = (
                    ((self.zones[drone.current_zone].y + drone.next_zone.y)
                     / 2)
                    * self.scale
                    + self.offset_y
                    - 28
                )
            else:
                x = (
                    (self.zones[drone.current_zone].x * self.scale)
                    + self.offset_x - 30
                )
                y = (
                    (self.zones[drone.current_zone].y * self.scale)
                    + self.offset_y - 28
                )
            d = pygame.image.load("drone.png")
            d = pygame.transform.scale(d, (60, 60))
            screen.blit(d, (x, y))
