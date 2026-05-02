class parser:

    zone = ["normal", "blocked", "restricted", "priority"]

    def parse_data(self, path):
        zones = {}
        first_line = 0
        start_hub = {}
        end_hub = {}
        connetcion = {}
        coordonate = []
        try:
            with open(path) as f:
                lines = []
                for l in f:
                    lines.append(l.strip())
                if not lines:
                    raise Exception("empty file")
                for line in lines:
                    if line.startswith('#') or not line:
                        continue
                    elif line.startswith("nb_drones"):
                       if first_line:
                           raise Exception ("nb_drones duplicate")
                       nb_drones =  self.validate_drones(line)
                       first_line = 1
                       continue
                    elif line.startswith("start_hub"):
                        if not start_hub:
                             raise Exception ("start_hub duplicate")
                        start_hub = self.validate_hub(line)
                        if start_hub["name"] in zones:
                            raise Exception ("duplicate name zone")
                        if (start_hub["x"],start_hub["y"]) in coordonate:
                            raise Exception ("duplicate coordonate zone")
                        coordonate.append((start_hub["x"],start_hub["y"]))
                        zones[zone["name"]] = zone
                    elif line.startswith("end_hub"):
                        if not end_hub:
                             raise Exception ("end_hub duplicate")
                        end_hub = self.validate_hub(line)
                        if end_hub["name"] in zones:
                            raise Exception ("duplicate name zone")
                        if (end_hub["x"],end_hub["y"]) in coordonate:
                            raise Exception ("duplicate coordonate zone")
                        coordonate.append((end_hub["x"],end_hub["y"]))
                        zones[zone["name"]] = zone
                    elif line.startswith("hub"):
                        zone = self.validate_hub(line)

                        zones[zone["name"]] = zone
                    elif line.startswith("connection"):
                        self.validate_connection(line)
        except FileNotFoundError:
            print("file not found")
    def validate_drones(self, line:str) -> int:
        data = line.split(":")
        try:
            nb_drones = int(data[1])
            if nb_drones <= 0:
                raise Exception("number of drones less than or equal to 0")
            return nb_drones
        except ValueError :
            print("invalid number")

    def validate_hub(self, line:str) -> dict:
        data = line.split(":")
        info = data[1].split(" ")
        name = info[0].strip()
        try:
            x = int(info[1])
            if(x < 0):
                raise Exception("The x-coordinate is less than 0")
            y = int(info[2])
            if(y < 0):
                raise Exception("The y-coordinate is less than 0")
            meta_data = self.validate_data(info[3])
            if "zone" not in meta_data:
                meta_data["zone"] = "normal"
            if "color" not in meta_data:
                meta_data["color"] = "none"
            if "max_drones" not in meta_data:
                meta_data["max_drones"] = 1
            return { "name": name, "x": x, "y": y, 
                    "zone": meta_data["zone"],
                    "color": meta_data["color"],
                    "max_drones": meta_data["max_drones"]}
        except ValueError:
            print("invalid number")

    def validate_data(line:str)-> dict:
        data = {}
        if not line :
            return data
        for k in line.split(" "):
            key, value = k.split("=")
            if key not in ["zone", "color", "max_drones"]:
                raise Exception("invalide meta data")
            if not key or not value:
                raise Exception("uncomplete meta data")
            data[key] = value
        return data
            


        

        

        


