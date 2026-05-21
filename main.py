from parsing import parser
from path import pathfound
from simulation import Simulation
from visualisation import Visualisation
import sys


def main() -> None:
    if "--capacity-info" in sys.argv:
        show = True
    else:
        show = False
    if len(sys.argv) < 2:
        print("run program with make run FILE=map_file")
        return
    p = parser()
    data = p.parse_data(sys.argv[1])
    path_found = pathfound(data)
    paths = path_found.find_path()
    # print(paths)
    simulation = Simulation(data, paths, show)
    Visualisation(data, simulation).run()


try:
    main()
except Exception as e:
    print(e)
