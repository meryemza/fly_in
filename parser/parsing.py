from .class_error import MapError
from objects.Zone import Hub
from objects.Drone import Drone
from objects.Connection import Connection
from objects.Data import Data
import re

class parser:
    zone = ["normal", "blocked", "restricted", "priority"]

    def parse_data(self, path):
        Drones = []
        zones = {}
        first_line = 0
        start_hub = {}
        end_hub = {}
        connetcion = []
        coordonate = []
        try:
            with open(path) as f:
                lines = []
                for l in f:
                    lines.append(l.strip())
                if not lines:
                    raise MapError("empty file")
                for line in lines:
                    if line.startswith('#') or not line:
                        continue
                    elif line.startswith("nb_drones"):
                       if first_line:
                           raise MapError ("nb_drones duplicate")
                       nb_drones =  self.validate_drones(line)
                       first_line = 1
                       continue
                    elif not first_line:
                        raise MapError ("nb_drones should be the first line")
                    elif line.startswith("start_hub"):
                        if  start_hub:
                             raise MapError ("start_hub duplicate")
                        start_hub = self.validate_hub(line)
                        start_hub.is_start = True
                        if start_hub.name in zones:
                            raise MapError ("duplicate name zone")
                        if (start_hub.x,start_hub.y) in coordonate:
                            raise MapError ("duplicate coordonate zone")
                        if start_hub.type == "blocked":
                            raise MapError ("start_hub can't be blocked")
                        if start_hub.max_drones < nb_drones:
                            raise MapError ("start_hub max_drones can't be less than number of drones")
                        coordonate.append((start_hub.x,start_hub.y))
                        zones[start_hub.name] = start_hub
                    elif line.startswith("end_hub"):
                        if end_hub:
                             raise MapError ("end_hub duplicate")
                        end_hub = self.validate_hub(line)
                        end_hub.is_end = True
                        if end_hub.name in zones:
                            raise MapError ("duplicate name zone")
                        if (end_hub.x,end_hub.y) in coordonate:
                            raise MapError ("duplicate coordonate zone")
                        if end_hub.type == "blocked":
                            raise MapError ("end_hub can't be blocked")
                        if end_hub.max_drones < nb_drones:
                            raise MapError ("end_hub max_drones can't be less than number of drones")
                        coordonate.append((end_hub.x,end_hub.y))
                        zones[end_hub.name] = end_hub
                    elif line.startswith("hub"):
                        zone = self.validate_hub(line)
                        if zone.name in zones:
                            raise MapError ("duplicate name zone")
                        if (zone.x,zone.y) in coordonate:
                            raise MapError ("duplicate coordonate zone")
                        coordonate.append((zone.x,zone.y))
                        zones[zone.name] = zone
                    elif line.startswith("connection"):
                       con = self.validate_connection(line)
                       for co in connetcion:
                            if con.zone1 == co.zone1 and con.zone2 == co.zone2 or con.zone1 == co.zone2 and con.zone2 == co.zone1:
                                raise MapError ("duplicate connection")
                       if con.zone1 not in zones or con.zone2 not in zones:
                           raise  MapError ("invalide zone")
                       connetcion.append(con)
                    else:
                        raise MapError("invalide line")
            
        except FileNotFoundError:
            raise MapError("file not found")
        if not start_hub:
            raise MapError("start_hub is missing")
        if not end_hub:
            raise MapError("end_hub is missing")
        for i in range(nb_drones):
             Drones.append(Drone(i +1, start_hub.name))

        for con in connetcion:
                 z1 = zones[con.zone1]
                 z2 = zones[con.zone2]
                 if zones[con.zone2].type != "blocked" and zones[con.zone1].type != "blocked":
                    z1.neighbors.append((z2.name, con.capacity))
                    z2.neighbors.append((z1.name, con.capacity))
        zones[start_hub.name].current_drones = nb_drones
        return Data(nb_drones, Drones, start_hub, end_hub, zones, connetcion)
    def validate_drones(self, line:str) -> int:
        data = line.split(":")
        try:
            nb_drones = int(data[1])
            if nb_drones <= 0:
                raise MapError("number of drones less than or equal to 0")
            return nb_drones
        except ValueError :
            raise MapError("invalid number")

    def validate_hub(self, line:str) -> Hub:
        meta_data = {}
        line_format = r":\s*(\w+)\s+(\d+)\s+(\d+)\s*(?:\[(.*?)\])?$"
        data = re.search(line_format, line)
        if not data:
            raise MapError("invalid line format")
        name = data.group(1)
        try:
                x = int(data.group(2))
                y = int(data.group(3))
        except ValueError:
            raise MapError("invalid number")
        if data.group(4) is None:
            meta_data["zone"] = "normal"
            meta_data["color"] = "none"
            meta_data["max_drones"] = 1
            max_drones = 1

        else:
                meta_data = self.validate_data(data.group(4))
                if "zone" not in meta_data:
                        meta_data["zone"] = "normal"
                if "color" not in meta_data:
                        meta_data["color"] = "none"
                if "max_drones" not in meta_data:
                        meta_data["max_drones"] = 1
                max_drones = int(meta_data["max_drones"])
                if max_drones <= 0:
                        raise MapError("invalide number for max drones")
                if meta_data["zone"] not in self.zone:
                        raise MapError("invalid zone")
        return  Hub (name, x, y, meta_data["zone"], meta_data["color"], max_drones)

    def validate_data(self, line:str)-> dict:
        data = {}
        if not line :
            return data
        line = line.replace("[", "").replace("]", "").strip()
        for k in line.split():
            if "=" not in k:
                raise MapError("invalid metadata format")
            key, value = k.split("=")
            if key not in ["zone", "color", "max_drones", "max_link_capacity"]:
                raise MapError("invalid meta data")
            if not key or not value:
                raise MapError("uncomplete meta data")
            data[key] = value
        return data
    def validate_connection(self, line):
        meta_data = {}
        line_format = r":\s*(\w+)-(\w+)\s*(?:\[(.*?)\])?$"
        data = re.search(line_format, line)
        if not data:
            raise MapError("invalid line format")
        zone1, zone2 = data.group(1), data.group(2)
        meta_data = self.validate_data(data.group(3))
        if not meta_data:
                meta_data["max_link_capacity"] = 1
        
        if int(meta_data["max_link_capacity"]) <= 0:
            raise MapError("invalide number for max link capacity")
        return Connection(zone1, zone2, int(meta_data["max_link_capacity"]))
