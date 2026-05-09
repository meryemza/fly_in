from objects.Graph import Graph
import heapq

class pathfound:
    def __init__(self, graph:Graph):
        self.zones = graph.zone
        self.start = graph.start
        self.end = graph.end

    def get_cost(self, zone):
        if zone.type == "restricted":
            return 2
        else:
            return 1
    
    def found_path(self):
        distance = {}
        previous = {}
        path = []
        heap = [(0, self.start.name)]
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
                    heapq.heappush(heap, (cost_total,neighbor_name))

        node = self.end.name
        while node != self.start.name:
            path.append(node)
            node = previous[node]
        path.append(self.start.name)
        return path[::-1]
