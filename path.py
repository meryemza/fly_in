from Data import Data
from Zone import Hub
from typing import List
import heapq


class pathfound:
    """using a Dijkstra-like algorithm to compute the
    lowest-cost path between start and end zones."""

    def __init__(self, data: Data) -> None:
        self.zones = data.zones
        self.start = data.start
        self.end = data.end

    def get_cost(self, zone: Hub) -> float:
        if zone.type == "restricted":
            return 2
        elif zone.type == "priority":
            return 0.9
        else:
            return 1

    def find_path(self, nb: int = 2) -> List[List[str]]:
        """Computes and return list of shortest  paths from start
        to end using a Dijkstra-style algorithm with a
        priority queue ."""

        paths: List[List[str]] = []
        heap: List[tuple[float, str, List[str]]] = [
            (0, self.start.name, [self.start.name])
        ]
        while heap and nb > len(paths):
            current_cost, current_zone, path = heapq.heappop(heap)
            if current_zone == self.end.name:
                paths.append(path)
                continue
            for neighbor in self.zones[current_zone].neighbors:
                if neighbor in path:
                    continue
                cost_neighbor = self.get_cost(self.zones[neighbor])
                total_cost = cost_neighbor + current_cost
                new_path = path + [neighbor]
                heapq.heappush(heap, (total_cost, neighbor, new_path))
        if not paths:
            raise ValueError("invalid path found")
        return paths
