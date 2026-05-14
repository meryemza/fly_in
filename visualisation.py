import pygame
from objects.Graph import Graph

class Visualisation:
    def __init__(self, graph:Graph):
        self.zones = graph.zone
        self.drones = graph.data.drones
        self.connections = graph.data.connections
    def run(self):
        pygame.init()

        screen = pygame.display.set_mode((700, 700))
        screen.fill(color=(90, 0, 30)) # to set a color of window
        pygame.display.set_caption("Fly_in")
        # bg = pygame.image.load("back.jpeg")
        # screen.blit(bg,(0,0))
        scale, off_x, off_y = self.compute(screen)
        self.draw_connections(screen, scale, off_x, off_y, 60)
        self.draw_zone(screen, scale, off_x, off_y, 60)
        self.draw_drone(screen, scale, off_x, off_y, 60)
        pygame.display.flip() # to update content on the display screen
        run = True 
        while(run):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit()

    def compute(self, screen):
        w, h = screen.get_size()

        max_x = max(z.x for z in self.zones.values())
        max_y = max(z.y for z in self.zones.values())

        scale = 100  

        offset_x = (w - max_x * scale) // 2
        offset_y = (h - max_y * scale) // 2

        return scale, offset_x, offset_y
    
    def draw_connections(self, screen, scale, off_x, off_y, size):
        half = size // 2
        for con in self.connections:
            x1 = self.zones[con.zone1].x*scale + off_x + half
            y1 = self.zones[con.zone1].y*scale  + off_y + half
            x2 = self.zones[con.zone2].x*scale + off_x + half
            y2 = self.zones[con.zone2].y*scale + off_y + half
            pygame.draw.line(screen, (150,150,150), (x1,y1), (x2,y2), 2)

    def draw_zone(self, screen, scale, off_x, off_y, size):
        font = pygame.font.SysFont("consolas", 14)
        for zon in self.zones.values():
            x = zon.x*scale+ off_x
            y = zon.y*scale+ off_y
            if zon.is_start:
                zone = pygame.image.load("start.png")
                zone = pygame.transform.scale(zone, (size, size)) #
                screen.blit(zone,(x,y))
            elif zon.is_end:
                zone = pygame.image.load("end.png")
                zone = pygame.transform.scale(zone, (size, size))
                screen.blit(zone,(x,y))
            else:
                zone = pygame.image.load("zone.png")
                zone = pygame.transform.scale(zone, (size, size))
                screen.blit(zone,(x,y))
            place_txt_x = size // 2 + x
            place_txt_y = size + 10 + y
            txt = font.render(zon.name, True, (255, 255, 255))
            txt_rect = txt.get_rect()
            txt_rect.center = (place_txt_x, place_txt_y)
            screen.blit(txt, txt_rect)
    
    def draw_drone(self,screen ,scale, off_x, off_y, size):
      half = size // 2
      for drone in self.drones:
          x = self.zones[drone.current_zone].x *scale + off_x + half
          y = self.zones[drone.current_zone].y *scale + off_y + half
          d = pygame.image.load("drone.png")
          d = pygame.transform.scale(d, (size , size))
          screen.blit(d,(x,y))
    

