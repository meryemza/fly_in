
from parser.parsing import parser
from objects.Graph import Graph
from path import pathfound
from simulation import Simulation
from visualisation import Visualisation


def main():
    p = parser()
    data = p.parse_data("01_linear_path.txt")
    graph = Graph(data).build()
    path = pathfound(graph)
    pathh = path.find_path()
    print(pathh)
    print(data.drones)
    # screen, scale, off_x, off_y , size = visualisation.run()
    simulation = Simulation(graph, pathh)
    visualisation = Visualisation(graph, simulation).run()
    print(data.drones)
    print(f"number of turns is {simulation.nb_turns}")

try:
    main()
except Exception as e:
    print(e)
