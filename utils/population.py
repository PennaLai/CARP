def find_best_solution(populations):
    """
    find the lower cost solution from the populaitons
    :param populations: populations
    :return: best: best solutions
    """
    if len(populations) == 0:
        print('populations are all died')
        return None
    # sort_population(populations)
    return populations[0]


def sort_population(population):
    """
    sort population by their cost
    :param population:
    :return:
    """
    return population.sort(key=lambda pop: pop.Cost)


def print_populations(populations):
    """
    just a test use, print all population and the best one
    :param populations:
    :return:
    """
    for x in populations:
        print(x.Cost)


def ave_population_cost(populations):
    """
    this function used to evaluate the fitness of the whole group
    :param populations:
    :return:
    """
    total_cost = 0
    num = len(populations)
    for po in populations:
        total_cost += po.Cost
    return int(total_cost/num)