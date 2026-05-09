class Hub:
    def __init__(self, name:str, x: int, y:int, type: str, color: str, max_drones: int):
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.max_drones = max_drones
        self.neighbors = []
        self.is_start = False
        self.is_end = False

    def __repr__(self):
        return f"(name={self.name}, x={self.x}, y={self.y}, type={self.type}, color={self.color}, max_drones={self.max_drones}, connected_zones={self.connected_zones})"
