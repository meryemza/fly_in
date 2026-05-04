from class_error import MapError

class parser:

    zone = ["normal", "blocked", "restricted", "priority"]

    def parse_data(self, path):
        zones = {}
        first_line = 0
        start_hub = {}
        end_hub = {}
        connetcion = set()
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
                    elif line.startswith("start_hub"):
                        if  start_hub:
                             raise MapError ("start_hub duplicate")
                        start_hub = self.validate_hub(line)
                        if start_hub["name"] in zones:
                            raise MapError ("duplicate name zone")
                        if (start_hub["x"],start_hub["y"]) in coordonate:
                            raise MapError ("duplicate coordonate zone")
                        coordonate.append((start_hub["x"],start_hub["y"]))
                        zones[start_hub["name"]] = start_hub
                    elif line.startswith("end_hub"):
                        if end_hub:
                             raise MapError ("end_hub duplicate")
                        end_hub = self.validate_hub(line)
                        if end_hub["name"] in zones:
                            raise MapError ("duplicate name zone")
                        if (end_hub["x"],end_hub["y"]) in coordonate:
                            raise MapError ("duplicate coordonate zone")
                        coordonate.append((end_hub["x"],end_hub["y"]))
                        zones[end_hub["name"]] = end_hub
                    elif line.startswith("hub"):
                        zone = self.validate_hub(line)
                        if zone["name"] in zones:
                            raise MapError ("duplicate name zone")
                        if (zone["x"],zone["y"]) in coordonate:
                            raise MapError ("duplicate coordonate zone")
                        coordonate.append((zone["x"],zone["y"]))
                        zones[zone["name"]] = zone
                    elif line.startswith("connection"):
                       con = self.validate_connection(line)
                       if con[0] not in zones or con[1] not in zones:
                           raise  MapError ("invalide zone")
                       connetcion.add(frozenset([con[0], con[1]]))
                    else:
                        raise MapError("invalide line")
            
        except FileNotFoundError:
            print("file not found")
        return {"nb_drones": nb_drones, "zones": zones, "connections": connetcion}
    def validate_drones(self, line:str) -> int:
        data = line.split(":")
        try:
            nb_drones = int(data[1])
            if nb_drones <= 0:
                raise MapError("number of drones less than or equal to 0")
            return nb_drones
        except ValueError :
            print("invalid number")

    def validate_hub(self, line:str) -> dict:
        meta_data = {}
        data = line.split(":")
        info = data[1].strip().split("[")
        name = info[0].strip().split()[0]
        if len(info) == 1:
            meta_data["zone"] = "normal"
            meta_data["color"] = "none"
            meta_data["max_drones"] = 1
        else:
            try:
                x = int(info[0].strip().split()[1])
                if(x < 0):
                        raise MapError("The x-coordinate is less than 0")
                y = int(info[0].strip().split()[2])
                if(y < 0):
                        raise MapError("The y-coordinate is less than 0")
                meta_data = self.validate_data(info[1])
                if "zone" not in meta_data:
                        meta_data["zone"] = "normal"
                if "color" not in meta_data:
                        meta_data["color"] = "none"
                if "max_drones" not in meta_data:
                        meta_data["max_drones"] = 1
                if meta_data["zone"] not in self.zone:
                        raise MapError("invalid zone")
            except ValueError:
                print("invalid number")
        return { "name": name, "x": x, "y": y, 
                    "zone": meta_data["zone"],
                    "color": meta_data["color"],
                    "max_drones": meta_data["max_drones"]}

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
        data = line.split(":")
        info = data[1].strip().split("[")
        zone1, zone2 = info[0].strip().split("-")
        if len(info) == 1:
          meta_data["max_link_capacity"] = 1
        else:
            meta_data = self.validate_data(info[1])
        if not meta_data:
                meta_data["max_link_capacity"] = 1
        if int(meta_data["max_link_capacity"]) <= 0:
            raise MapError("invalide number for max link capacity")
        return [zone1, zone2, meta_data]

p = parser()
print(p.parse_data("data.txt"))