from .Data import Data

class Graph:
    def __init__(self, data :Data):
        self.data = data
        self.zone = {}
        self.start = None
        self.end = None

    def build(self):
        self.start = self.data.start
        self.end = self.data.end
        for i in self.data.zones.values():
            self.add_zone(i)
        return self

    def add_zone(self, z):
        if z.name in self.zone:
            return
        self.zone[z.name] = z