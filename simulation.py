from Data import Data
from Connection import Connection
from typing import List, Tuple


class Simulation:
    """Core simulation engine for multi-drone movement on a zone graph
    Uses a shared path for all drones and resolves conflicts using
    per-turn reservation system (zone_reserved / con_reserved)."""

    def __init__(self, data: Data, path: List[List[str]]) -> None:
        self.drones = data.drones
        self.nb_drones = data.nb_drones
        self.paths = path
        self.zones = data.zones
        self.connection = data.connections
        self.finish = False
        self.nb_turns = 0

    def fill_paths(self) -> None:
        for i in range(len(self.drones)):
            self.drones[i].path = self.paths[i % len(self.paths)]

    def move_drones(self) -> None:
        self.fill_paths()
        """ Executes one simulation turn for all drones.
           Handles all cases of drones (currently in transit, normale)
           and Computes next valid moves based on:
            (zone capacity, connection capacity ,reserved resources
            in current turn)"""

        fini = 0

        moves = []
        zone_reserved: dict[str, int] = {}
        con_reserved: dict[Connection, int] = {}
        actions: List[Tuple] = []
        for drone in self.drones:
            current_index = drone.current_index
            next_index = current_index + 1
            if drone.finished:
                continue

            if next_index >= len(drone.path):
                continue
            con = self.get_connection(drone.path[current_index],
                                      drone.path[next_index])
            next_zone = self.zones[drone.path[next_index]]
            current_zone = self.zones[drone.path[current_index]]
            if drone.in_transit and next_index < len(drone.path):

                drone.remaining_turns -= 1
                if drone.remaining_turns == 0:
                    # future_zone = (
                    #     (zone_reserved.get(next_zone.name, 0))
                    #     + next_zone.current_drones
                    # )
                    # if future_zone < next_zone.max_drones:
                    #     zone_reserved[next_zone.name] = (
                    #         zone_reserved.get(next_zone.name, 0) + 1
                    #     )
                    #     zone_reserved[current_zone.name] = (
                    #         zone_reserved.get(current_zone.name, 0) - 1
                    #     )
                    actions.append(
                        ("arrive", drone, con, next_zone, current_zone,
                         next_index)
                    )

                continue

            if con in con_reserved:
                con_used = con_reserved[con]
            else:
                con_used = 0

            future_zone = next_zone.current_drones + zone_reserved.get(
                next_zone.name, 0
            )
            zone_avail = next_zone.max_drones - future_zone
            con_avail = con.capacity - (con.current_load + con_used)

            if zone_avail > 0 and con_avail > 0:

                zone_reserved[next_zone.name] = (
                    zone_reserved.get(next_zone.name, 0)
                    + 1)
                zone_reserved[current_zone.name] = (
                    zone_reserved.get(current_zone.name, 0) - 1
                )
                con_reserved[con] = con_used + 1
                if next_zone.type == "restricted":
                    actions.append(
                        ("transit", drone, con, next_zone, current_zone,
                         next_index)
                    )
                else:
                    actions.append(
                        ("move", drone, con, next_zone, current_zone,
                         next_index)
                    )

        for action in actions:
            if action[0] == "arrive":
                _, drone, con, next_zone, current_zone, next_index = action
                con.current_load -= 1
                drone.in_transit = False
                next_zone.current_drones += 1
                current_zone.current_drones -= 1
                drone.current_index = next_index
                drone.current_zone = drone.path[next_index]
                moves.append(f"D{drone.id}-{drone.current_zone}")
            if action[0] == "transit":
                _, drone, con, next_zone, current_zone, next_index = action
                drone.in_transit = True
                con.current_load += 1
                drone.remaining_turns = 1
                current_zone.current_drones -= 1
                drone.next_zone = self.zones[drone.path[next_index]]
                moves.append(f"D{drone.id}-{current_zone.name}-"
                             f"{next_zone.name}")
            if action[0] == "move":
                _, drone, con, next_zone, current_zone, next_index = action
                next_zone.current_drones += 1
                current_zone.current_drones -= 1
                drone.current_index = next_index
                drone.current_zone = drone.path[next_index]
                moves.append(f"D{drone.id}-{drone.current_zone}")
        for drone in self.drones:
            if drone.current_zone == drone.path[-1] and not drone.finished:
                drone.finished = True
            if drone.finished:
                fini += 1
        if fini == self.nb_drones:
            self.finish = True
        print(" ".join(moves))
        self.nb_turns += 1

    def get_connection(self, zone1: str, zone2: str) -> Connection:
        """Retrieves the connection object between two zones."""

        for con in self.connection:
            if (con.zone1 == zone1 and con.zone2 == zone2) or (
                con.zone1 == zone2 and con.zone2 == zone1
            ):
                return con
        raise ValueError(f"no connection between {zone1} et {zone2}")
