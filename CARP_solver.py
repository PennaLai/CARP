'''
this program is used to solve the carp problem in the course cs303 Artifical intelligence in SUSTECH
'''
import argparse
import time
import numpy as np



def main():
    '''
    main function
    '''
    # start time
    start = time.time()
    # read the command
    parser = argparse.ArgumentParser(prog='CARP',description='import problem')
    parser.add_argument('instance', type=argparse.FileType('r'))
    parser.add_argument('-t','--time', type=int)
    parser.add_argument('-s','--seed', type=int)
    arg_set = parser.parse_args()
    limit_time = arg_set.time
    seed = arg_set.seed
    sampe_file = arg_set.instance
    infos, graph_data = read_file(sampe_file)
    print(graph_data)


def read_file(sample_file):
    '''
    read the file for given sample
    Args:
        sample_file: the given sample file
    Returns:
        infos: the information except the graph data
        graph_data: the data that can make a graph
    '''
    line_count = 1
    infos = dict()
    graph_data = np.array()
    while sample_file.read_file is not None:
        line = sample_file.readline()
        if line_count <= 9:
            info = line.split(':')
            infos[info[0]] = info[1]
        else:
            graph_info = line.split()
            graph_data.append([x.strip() for x in graph_info])
        line_count += 1
    sample_file.close()
    return infos, graph_data


if __name__ == '__main__':
    main()
