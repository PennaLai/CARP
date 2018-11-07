'''
a class used to make the graph
'''
import collections
edge_info = collections.namedtuple('edge_info', 'Cost Demand')

class Graph():
    def __init__(self, graph_data):
        self.vertices_set = dict()
        self.edge_set = dict()
        self.read_data(graph_data)
        pass

    def read_data(self, graph_data):
        for data in graph_data:
            x = data[0]
            y = data[1]
            cost = data[2]
            demand = data[3]
            self.add_vertice(x, y)
            self.add_vertice(y, x)
            self.add_edge(x, y, cost, demand)
        print(self.vertices_set)
        print(self.edge_set)

    def add_vertice(self, x, y):
        if  x not in self.vertices_set.keys():
            self.vertices_set[x] = []
        self.vertices_set[x].append(y)

    def add_edge(self, x, y, cost, demand):
        if (x, y) not in self.edge_set:
            self.edge_set[(x, y)] = edge_info(Cost=cost, Demand=demand)


