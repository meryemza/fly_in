from parser.parsing import parser
from path import pathfound
from simulation import Simulation
from visualisation import Visualisation


def main() -> None:
    p = parser()
    data = p.parse_data("01_linear_path.txt")
    # graph = Graph(data)
    # graph.build()
    path = pathfound(data)
    pathh = path.find_path()
    print(pathh)
    print(data.drones)
    # screen, scale, off_x, off_y , size = visualisation.run()
    simulation = Simulation(data, pathh)
    Visualisation(data, simulation).run()
    print(data.drones)
    print(f"number of turns is {simulation.nb_turns}")


try:
    main()
except Exception as e:
    print(e)
