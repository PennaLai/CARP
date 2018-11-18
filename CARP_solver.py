"""
this program is used to solve the carp problem in the course cs303 Artificial intelligence in SUSTECH
"""
import argparse
import time
import numpy as np
from utils.graph import Graph
from multiprocessing import Pool, Manager
from collections import namedtuple
from utils.evolution import *
from utils.population import *

PROCESSORS = 8
Solution = namedtuple("Solution", "Route Cost")
LIMIT_TIME = 0
SEED = 0


def main():
    """
    main function
    """
    # start time
    start_time = time.time()
    # read the command
    parser = argparse.ArgumentParser(prog='CARP',description='import problem')
    parser.add_argument('instance', type=argparse.FileType('r'))
    parser.add_argument('-t', '--time', type=int)
    parser.add_argument('-s', '--seed', type=int)
    arg_set = parser.parse_args()
    LIMIT_TIME = arg_set.time
    SEED = arg_set.seed
    np.random.seed(SEED)
    sample_file = arg_set.instance
    infos, graph_data = read_file(sample_file)
    graph = Graph(infos, graph_data)
    mg = Manager()
    populations = mg.list()
    # multiprocessing to solve the problem
    p = Pool(PROCESSORS)
    for i in range(PROCESSORS):
        # every processing have it own seed (0 -> 10^9)
        p.apply_async(solve_problem, (populations, graph, infos, start_time, LIMIT_TIME, np.random.randint(0, 10 ** 9)))
    # print('wait for all subprocesses done')
    p.close()
    p.join()
    # get the last result into a world
    world = list()
    for po in populations:
        world += po
    sort_population(world)
    print_populations(world)
    # print('world number is ', len(world))
    best = find_best_solution(world)
    print(solution_output(best.Route))
    print('q', int(best.Cost))
    # print('group fit', ave_population_cost(world))
    # print('The limited time is ', LIMIT_TIME)
    # end = time.time()
    # print('total_time', end-start_time)


def solve_problem(result_list, graph, infos, start_time, limited_time, seed):
    """
    the main solve function, will use multiprocessor to solve it
    :return:
    """
    np.random.seed(seed)
    populations = list()
    populations = init_population(populations, np.random.randint(0, 10 ** 9), 200, graph, infos)
    sort_population(populations)
    best_cost = populations[0].Cost
    pop_num = get_group_number(best_cost)
    populations = populations[0:pop_num]  # we only need 30
    evolution_time = limited_time - (time.time() - start_time)
    evo = EvoSolves(graph, populations, evolution_time, seed=seed)
    populations = evo.evolutionary(populations)
    result_list.append(populations)


def init_population(result_list, random_seed, pop_num, graph, infos):
    """
    this method use random path-scanning to generate the population
    :param pop_num: the number of the population
    :param result_list: return the result to this list
    :param random_seed: decide the random
    :param graph: graph information
    :param infos: problem information
    :return: a group of population
    """
    np.random.seed(random_seed)
    for i in range(pop_num):
        solution = path_scanning(graph, infos, np.random.randint(0, 10 ** 9))
        result_list.append(solution)
    return result_list


def path_scanning(graph, infos, random_seed):
    """
    this is the basic method to find the solution of carp problem
    :param graph:
    :param infos:
    :param random_seed: decide the random value
    :return:
        route: the solution path
        total_cost : the cost for this path scanning
    """
    np.random.seed(random_seed)
    capa = int(infos['CAPACITY'])
    cost_table = graph.cost_table
    edge_set = graph.edge_set  # the relation of edge and cost, command
    free_edge = get_free_edge(edge_set)  # the edge whose demand are larger than zero
    demand = []
    cost = []
    route = []
    while free_edge:  # while free_edge is not empty
        edges = free_edge.copy()  # only for this path task using
        edges = get_less_cap_edge(edges, edge_set, capa)
        node_now = 1  # begin from depot
        this_cap = capa
        this_cost = 0
        this_demand = 0
        route.append([])
        while edges:  # while there are still edges that satisfy our cap
            '''
            the next edge has a big influence on the result, maybe 
            we can choose the diff way to choose next cost, for example
            the ratio of demand/cost
            improve it later !
            '''
            # =========== choose edge setting ==============
            way = np.random.randint(0, 2)
            if way == 1:
                next_node, next_cost, next_edge = find_min_distance_edge(edges, edge_set, cost_table, node_now, np.random.randint(0, 10 ** 9))
            else:
                next_node, next_cost, next_edge = find_max_demand_div_cost_edge(edges, edge_set, cost_table, node_now, np.random.randint(0, 10 ** 9))
            #  =============================================
            node_now = next_node
            this_cap -= edge_set[next_edge].Demand
            # add edge with right direction into list
            if next_edge[1] == node_now:
                route[-1].append(next_edge)
            else:
                route[-1].append((next_edge[1], next_edge[0]))
            # after clean, remove this edge
            free_edge.remove(next_edge)
            edges.remove(next_edge)
            # update the new edges that satisfy capacity
            '''
            sometimes we can give up, that means if there are still 
            have edge we can clean but with high cost. we could give up
            so we set the randomly give up 
            '''
            # =========== give up setting ==============
            # randomly give up
            give_up_cap = np.random.randint(1, 4)
            if this_cap <= give_up_cap/10 * capa:
                this_cap = 0
            # this_cap = this_cap-1 if this_cap > 1 else this_cap
            # ==========================================
            edges = get_less_cap_edge(edges, edge_set, this_cap) # select the edge less than capacity now
            this_cost += next_cost
            this_demand += edge_set[next_edge].Demand
        this_cost += cost_table[node_now-1, 0]  # add the back to depot cost
        cost.append(this_cost)
        demand.append(this_demand)
    total_cost = sum(cost)
    solution = Solution(Route=route, Cost=total_cost)
    return solution


def find_min_distance_edge(edges, edge_set, cost_table, node_pos, seed):
    """
    min the distance cost
    :param edges: the edge set that satisfy capacity right now
    :param edge_set: the edge set that contain demand information
    :param cost_table: the all cost information between two node
    :param node_pos: the position which we are in now
    :param seed: make it random
    :return:
        next_node : the next node we will arrive
        total_cost : the cost to the last position
        edge: the next edge
    """
    near_node = -1
    near_cost = float('inf')
    near_list_edge = []
    for edge in edges:
        for x in edge:
            if cost_table[node_pos-1, x-1] <= near_cost:
                if x != near_node:  # if we have not meet this node before
                    near_node = x
                    near_cost = cost_table[node_pos-1, x-1]
                    near_list_edge = []  # update new near_node and clear the list
                near_list_edge.append(edge)
    '''
     if we find a nearest node, but it may have server edge in this node, we need to find a one
     now we find the one which have large demand that we can collect more demand this time
     and it there are two same command, we randomly chose it
    '''
    # sort its demand from low to high
    near_list_edge.sort(key=lambda edge: edge_set[edge].Demand)
    np.random.seed(seed)
    r = np.random.randint(0, 2)
    next_edge = near_list_edge[-1]
    if len(near_list_edge) > 1:
        if edge_set[near_list_edge[-1]].Demand == edge_set[near_list_edge[-2]].Demand:
            next_edge = near_list_edge[-1] if r == 0 else near_list_edge[-2]
    next_node = next_edge[0] if next_edge[0] != near_node else next_edge[1]
    total_cost = near_cost + edge_set[next_edge].Cost  # the cost to the nearest node + edge cost
    return next_node, total_cost, next_edge


def find_max_demand_div_cost_edge(edges, edge_set, cost_table, node_pos, seed):
    """
    the similar function to the function 'find_min_distance_edge'
    """
    near_node = -1
    next_edge = None
    d_ratio_c = -1
    np.random.seed(seed)
    for edge in edges:
        for x in edge:
            # if the next node is current node, the distance would be zero
            node_cost = 0.5 if cost_table[node_pos-1, x-1] == 0 else cost_table[node_pos-1, x-1]
            new_ratio = edge_set[edge].Demand/node_cost
            if new_ratio >= d_ratio_c:
                if new_ratio - d_ratio_c <= 0.0000001:  # if they are equal (float number)
                    r = np.random.randint(0, 2)
                    if r == 0:  # we do switch it randomly
                        continue
                d_ratio_c = new_ratio
                near_node = x
                next_edge = edge
    # the cost to the nearest node + edge cost
    next_node = next_edge[0] if next_edge[0] != near_node else next_edge[1]
    total_cost = cost_table[node_pos-1, near_node-1] + edge_set[next_edge].Cost
    return next_node, total_cost, next_edge


def get_free_edge(edge_set):
    """
    for given a edge dict, return a list contains
    the free_edge whose demand equals to zero
    :param edge_set: a dict
    :return: free_edge: a list
    """
    return [edge for edge in edge_set.keys() if edge_set[edge].Demand != 0]


def get_less_cap_edge(edges, edge_set, cap):
    """
    find the edge that still can satisfy cap
    :param edges: edge set right now
    :param edge_set: information set
    :param cap: cap that the vehicles have now
    """
    return [edge for edge in edges if not edge_set[edge].Demand > cap]


def read_file(sample_file):
    """
    :param sample_file: the given sample file
    :return:
        infos: the information except the graph data
        graph_data: the data that can make a graph
    """
    line_count = 1
    infos = dict()
    graph_data = list()
    while True:
        line = sample_file.readline()
        if 'END' in line:
            break
        if line_count <= 8:
            info = line.split(':')
            key = info[0].strip()
            value = info[1].replace('\n', '')
            value = value.strip()
            infos[key] = value
        elif line_count > 9:
            graph_info = line.split()
            graph_data.append([x.strip() for x in graph_info])
        line_count += 1
    graph_data = np.array(graph_data)
    sample_file.close()
    return infos, graph_data


def solution_output(route):
    """
    give a format output of the answer
    :param route: the array contain the route information
    :return: r: route string like s 0,(1,2),(2,4),(4,1),0,0,(4,3),(3,1),0
    """
    r = 's '
    for path in route:
        r += '0,'
        for edge in path:
            r += '({},{}),'.format(edge[0], edge[1])
        r += '0'
        if path != route[-1]:
            r += ','
    return r


if __name__ == '__main__':
    main()
