from .Drone import Drone
from .Zone import Hub
from .Connection import Connection

class Data:
    def __init__(self, nb_drones:int, Drones: list[Drone], start_zone: Hub , end_zone: Hub, zones: list[Hub], connections: list[Connection]):
        self.nb_drones = nb_drones
        self.drones = Drones
        self.start = start_zone
        self.end = end_zone
        self.zones = zones
        self.connections = connections


        