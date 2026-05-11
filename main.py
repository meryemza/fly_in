
from parser.parsing import parser
from objects.Graph import Graph
from path import pathfound
from simulation import Simulation


def main():
    p = parser()
    data = p.parse_data("01_linear_path.txt")
    graph = Graph(data).build()
    path = pathfound(graph)
    pathh = path.find_path()
    print(pathh)
    simulation = Simulation(graph, pathh)
    print(data.drones)
    move = simulation.move_drones()
    print(data.drones)


main()
