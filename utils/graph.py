"""
a class used to make the graph
"""

from collections import namedtuple
import numpy as np

edge_info = namedtuple('edge_info', 'Cost Demand')


class Graph:
    def __init__(self, infos, graph_data):
        """
        init the graph
        :param infos: the information of the problem
        :param graph_data: the data of the problem
        """
        self.vertices_set = dict()
        self.edge_set = dict()
        self.verti_numb = int(infos['VERTICES'])  # number of node
        self.capa = int(infos['CAPACITY'])
        # init cost array
        self.cost_table = np.full((self.verti_numb, self.verti_numb), float('inf'), dtype=float)
        for i in range(self.verti_numb):
            self.cost_table[i, i] = 0
        self.read_data(graph_data)
        floyd(self.cost_table)
        # print_table(self.cost_table)
        # print(self.edge_set)

    def read_data(self, graph_data):
        """
        read the given data and make a graph
        :param graph_data: the numpy array contain x, y, cost, demand
        """
        for data in graph_data:
            x = int(data[0])
            y = int(data[1])
            cost = int(data[2])
            demand = int(data[3])
            self.add_vertices(x, y)
            self.add_vertices(y, x)
            self.add_edge(x, y, cost, demand)

    def add_vertices(self, x, y):
        """
        add a node into graph
        :param x: node1
        :param y: node2
        """
        if x not in self.vertices_set.keys():
            self.vertices_set[x] = []
        self.vertices_set[x].append(y)

    def add_edge(self, x, y, cost, demand):
        """
        add edge into graph, and update the distance table for two vertices
        :param x: node1
        :param y: node2
        :param cost: cost from node1 to node2
        :param demand: demand from node1 to node2
        """
        if (x, y) not in self.edge_set:
            self.edge_set[(x, y)] = edge_info(Cost=int(cost), Demand=int(demand))
            # the numpy index begin from 0 but the vertices begin from 1
            self.cost_table[x-1, y-1] = int(cost)
            self.cost_table[y-1, x-1] = int(cost)

    def calculate_cost(self, route):
        cost = 0
        for task in route:
            node_now = 1
            for edge in task:
                cost += self.cost_table[node_now-1, edge[0]-1]
                if edge in self.edge_set:
                    edge_cost = self.edge_set[edge].Cost
                else:
                    edge_cost = self.edge_set[(edge[1], edge[0])].Cost
                cost += edge_cost
                node_now = edge[1]
            cost += self.cost_table[node_now-1, 0]  # back cost
        return cost

    def calculate_task_demand(self, task):
        demand = 0
        for x in task:
            if x in self.edge_set:
                demand += self.edge_set[x].Demand
            else:
                demand += self.edge_set[(x[1], x[0])].Demand
        return demand

def floyd(dis_arr):
    """
    given a exist distance array for each two node, calculate the min distance for two node
    :param dis_arr: the distance array
    """
    res_len = len(dis_arr)
    for k in range(res_len):
        for i in range(res_len):
            for j in range(res_len):
                dis_arr[i, j] = min(dis_arr[i, j], dis_arr[i, k] + dis_arr[k, j])


def print_table(np_array):
    for x in np_array:
        for y in x:
            print(y, end=' ')
        print()
