from parsing import parser
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
    path_found = pathfound(data)
    paths = path_found.find_path()
    print(paths)
    simulation = Simulation(data, paths)
    Visualisation(data, simulation).run()
    print(f"number of turns is {simulation.nb_turns}")


try:
    main()
except Exception as e:
    print(e)
