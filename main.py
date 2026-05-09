
from parser.parsing import parser
from objects.Graph import Graph
from path import pathfound
def main():
    p = parser()
    data = p.parse_data("data.txt")
    graph = Graph(data).build()
    path = pathfound(graph)
    pathh = path.found_path()
    print(pathh)
main()
