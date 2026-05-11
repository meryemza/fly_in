from objects.Graph import Graph
class Simulation:
    def __init__(self, graph:Graph, path):
        self.drones = graph.data.drones
        self.nb_drones = graph.data.nb_drones
        self.path = path
        self.zones = graph.zone
        self.connection = graph.data.connections
    
    def move_drones(self):
        finish = 0
        i = 0
        while finish < self.nb_drones:
            moves = []
            for drone in self.drones:
                current_index = drone.current_index
                next_index = current_index+1
                if drone.finished:
                    continue
                if drone.in_transit and next_index < len(self.path):
                        con = self.get_connection(self.path[current_index], self.path[next_index])
                        next_zone = self.zones[self.path[next_index]]
                        current_zone = self.zones[self.path[current_index]]
                        drone.remaining_turns-=1
                        if drone.remaining_turns == 0:
                            con.current_load -=1
                            drone.in_transit = False
                            next_zone.current_drones += 1
                            current_zone.current_drones -= 1
                            drone.current_index = next_index
                            drone.current_zone = self.path[next_index]
                            moves.append(f"D{drone.id}-{drone.current_zone}")
                        continue
                if next_index < len(self.path) and not drone.in_transit:
                    next_zone = self.zones[self.path[next_index]]
                    current_zone = self.zones[self.path[current_index]]
                    if next_zone.max_drones > next_zone.current_drones:
                        con = self.get_connection(self.path[current_index], self.path[next_index])
                        if con.current_load < con.capacity:
                            if next_zone.type == "restricted":
                                drone.in_transit = True
                                con.current_load +=1
                                drone.remaining_turns = 2
                                moves.append(f"D{drone.id}-{current_zone.name}-{next_zone.name}")
                            else:
                                next_zone.current_drones += 1
                                current_zone.current_drones -= 1
                                drone.current_index = next_index
                                drone.current_zone = self.path[next_index]
                                moves.append(f"D{drone.id}-{drone.current_zone}")
                if drone.current_zone == self.path[-1] and  not drone.finished:
                    drone.finished = True
                    finish += 1
            i+=1
            print(" ".join(moves))
        print(f"{i} turns")
          

    def get_connection(self, zone1, zone2) :
        for con in self.connection:
            if (con.zone1 == zone1 and con.zone2 == zone2 ) or (con.zone1 == zone2 and con.zone2 == zone1 ):
                return con