class  Connection:
    def __init__(self,zone1:str, zone2:str, capacity:int):
        self.zone1 = zone1
        self.zone2 = zone2
        self.capacity = capacity
    def __repr__(self):
        return f"({self.zone1}, {self.zone2}, {self.capacity})"