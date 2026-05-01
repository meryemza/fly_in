class parser:

    zone = ["normal", "blocked", "restricted", "priority"]

    def parse_data(self, path):
        zones = {}
        # start_hub = {}
        # end_hub = {}
        connetcion = {}
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
                       nb_drones =  self.validate_drones(line)
                    elif line.startswith(("start_hub", "end_hub", "hub")):
                        self.validate_hub(line)
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
            if len(info == 4):
                meta_data = self.validate_data(info[3])
            else:
                meta_data = {"zone":"normal", "color":"none", "max_drones":1}
            return { "name": name, "x": x, "y": y, "meta_data": meta_data}
        except ValueError:
            print("invalid number")

    def validate_data(line:str)-> dict:
        data = line.split(" ")
        

        

        


