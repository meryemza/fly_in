from objects.Graph import Graph
class Simulation:
    def __init__(self, graph:Graph, path):
        self.drones = graph.data.drones
        self.nb_drones = graph.data.nb_drones
        self.path = path
        self.zones = graph.zone
        self.connection= graph.data.connections
    
    def move_drones(self):
        finish = 0
        while finish < self.nb_drones:
            for drone in self.drones:
                if drone.finished:
                    continue
                current_index = drone.current_index
                next_index = current_index+1

                if next_index < len(self.path):
                    next_zone = self.zones[self.path[next_index]]
                    current_zone = self.zones[self.path[current_index]]
                    if next_zone.max_drones > next_zone.current_drones:
                        next_zone.current_drones += 1
                        current_zone.current_drones -= 1
                        drone.current_index = next_index
                        drone.current_zone = self.path[next_index]
                if drone.current_zone == self.path[-1] and  not drone.finished:
                    drone.finished = True
                    finish += 1
            # print(self.drones)
            
