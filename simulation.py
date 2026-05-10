from objects.Graph import Graph
class Simulation:
    def __init__(self, graph:Graph, path):
        self.drones = graph.data.drones
        self.nb_drones = graph.data.nb_drones
        self.path = path
        self.zones = graph.zone
        self.connection= graph.data.connections
    
GIT
            # print(self.drones)
            
