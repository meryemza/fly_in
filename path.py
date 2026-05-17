from objects.Data import Data
from objects.Zone import Hub
from typing import List
import heapq


class pathfound:
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

    def find_path(self) -> List[str]:
        distance: dict[str, float] = {}
        previous: dict[str, str] = {}
        path = []
        heap: List[tuple[float, str]] = [(0, self.start.name)]
        for zone in self.zones.values():
            if zone.name == self.start.name:
                distance[zone.name] = 0
            else:
                distance[zone.name] = float("inf")
        while heap:
            current_cost, current_zone = heapq.heappop(heap)
            if current_zone == self.end.name:
                break
            for neighbor in self.zones[current_zone].neighbors:
                neighbor_name = neighbor[0]
                cost_neighbor = self.get_cost(self.zones[neighbor_name])
                cost_total = current_cost + cost_neighbor
                if cost_total < distance[neighbor_name]:
                    distance[neighbor_name] = cost_total
                    previous[neighbor_name] = current_zone
                    heapq.heappush(heap, (cost_total, neighbor_name))

        node = self.end.name
        while node != self.start.name:
            path.append(node)
            node = previous[node]
        path.append(self.start.name)
        return path[::-1]
