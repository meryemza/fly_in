from parser.parsing import parser
from path import pathfound
from simulation import Simulation
from visualisation import Visualisation
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("run program with make run FILE=map_file")
        return
    p = parser()
    data = p.parse_data(sys.argv[1])
    path = pathfound(data)
    pathh = path.find_path()
    print(pathh)
    print(data.drones)
    simulation = Simulation(data, pathh)
    Visualisation(data, simulation).run()
    print(data.drones)
    print(f"number of turns is {simulation.nb_turns}")


try:
    main()
except Exception as e:
    print(e)
