'''
this program is used to solve the carp problem in the course cs303 Artifical intelligence in SUSTECH
'''
import argparse
import time
import numpy as np
from utils.graph import Graph


def main():
    """
    main function
    :return:
    """
    # start time
    start = time.time()
    # read the command
    parser = argparse.ArgumentParser(prog='CARP',description='import problem')
    parser.add_argument('instance', type=argparse.FileType('r'))
    parser.add_argument('-t', '--time', type=int)
    parser.add_argument('-s', '--seed', type=int)
    arg_set = parser.parse_args()
    limit_time = arg_set.time
    seed = arg_set.seed
    sample_file = arg_set.instance
    infos, graph_data = read_file(sample_file)
    graph = Graph(infos, graph_data)


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


if __name__ == '__main__':
    main()
