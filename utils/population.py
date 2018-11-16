def find_best_solution(populations):
    """
    find the lower cost solution from the populaitons
    :param populations: populations
    :return: best: best solutions
    """
    if len(populations) == 0:
        print('populations are all died')
        return None
    return populations[0]


def sort_population(population):
    return population.sort(key=lambda pop: pop.Cost)


def print_populations(populations):
    """
    just a test use, print all population and the best one
    :param populations:
    :return:
    """
    for x in populations:
        print(x.Cost)
        print(x.Route)