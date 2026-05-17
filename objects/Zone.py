from typing import List
class Hub:
    def __init__(self, name:str, x: int, y:int, type: str, color: str, max_drones: int)-> None:
        self.name = name
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.max_drones = max_drones
        self.neighbors: List[tuple[str, int]] = []
        self.is_start = False
        self.is_end = False
        self.current_drones = 0

    def __repr__(self):
        return f"(name={self.name}, x={self.x}, y={self.y}, type={self.type}, color={self.color}, max_drones={self.max_drones}, connected_zones={self.connected_zones})"
