import pygame
from objects.Graph import Graph

class Visualisation:
    def __init__(self, graph:Graph, simulation):
        self.zones = graph.zone
        self.drones = graph.data.drones
        self.connections = graph.data.connections
        self.size = 70
        self.offset_x = 120
        self.offset_y = 120
        self.scale = 110
        self.simulation = simulation

    def run(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        info = pygame.display.Info()
        x_screen = info.current_w
        y_screen = info.current_h
        screen = pygame.display.set_mode((x_screen, y_screen))
        screen.fill(color=(90, 0, 30)) # to set a color of window
        pygame.display.set_caption("Fly_in")

        run = True
        start_map = 1
        while(run):
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
               if event.type == pygame.KEYDOWN: #Checks if a keyboard key was pressed
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
                     
                if event.key == pygame.K_a: # check the key exact 
                        
                    if  not self.simulation.finish:
                            screen.fill(color=(90, 0, 30))
                            self.draw_connections(screen)
                            self.draw_zone(screen)
                            self.simulation.move_drones()
                            self.draw_drone(screen)
                            pygame.display.flip() # to update content on the display screen
                            self.clock.tick(2)
    
    def draw_connections(self, screen):
        half = self.size // 2
        for con in self.connections:
            x1 = self.zones[con.zone1].x*self.scale + self.offset_x + half
            y1 = self.zones[con.zone1].y*self.scale  + self.offset_y + half
            x2 = self.zones[con.zone2].x*self.scale + self.offset_x + half
            y2 = self.zones[con.zone2].y*self.scale + self.offset_y + half
            pygame.draw.line(screen, (150,150,150), (x1,y1), (x2,y2), 2)

    def draw_zone(self, screen):
        font = pygame.font.SysFont("consolas", 14)
        for zon in self.zones.values():
            x = zon.x*self.scale+ self.offset_x
            y = zon.y*self.scale+ self.offset_y
            if zon.is_start:
                pygame.draw.circle(screen, zon.color, (x + 35 ,y+35), self.size - 30)
                zone = pygame.image.load("start.png")
                zone = pygame.transform.scale(zone, (self.size, self.size)) #
                screen.blit(zone,(x,y))
            elif zon.is_end:
                pygame.draw.circle(screen, zon.color, (x + 35,y+35), self.size - 30)
                zone = pygame.image.load("end.png")
                zone = pygame.transform.scale(zone, (self.size, self.size))
                screen.blit(zone,(x,y))
            else:
                pygame.draw.circle(screen, zon.color, (x + 35,y + 35), self.size - 30)
                zone = pygame.image.load("zone.png")
                zone = pygame.transform.scale(zone, (self.size, self.size))
                screen.blit(zone,(x,y))
            place_txt_x = self.size // 2 + x
            place_txt_y = self.size + 10 + y
            txt = font.render(zon.name, True, (255, 255, 255))
            txt_rect = txt.get_rect()
            txt_rect.center = (place_txt_x, place_txt_y)
            screen.blit(txt, txt_rect)
    
    def draw_drone(self,screen):
      for drone in self.drones:
          if drone.in_transit:
               x = ((self.zones[drone.current_zone].x  + drone.next_zone.x ) / 2 )*self.scale + self.offset_x 
               y = ((self.zones[drone.current_zone].y  + drone.next_zone.y) / 2 ) *self.scale + self.offset_y
          else:
            x = self.zones[drone.current_zone].x *self.scale + self.offset_x 
            y = self.zones[drone.current_zone].y *self.scale + self.offset_y
          d = pygame.image.load("drone.png")
          d = pygame.transform.scale(d, (self.size , self.size))
          screen.blit(d,(x,y))
