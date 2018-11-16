import time
import random


class EvoSolves:

    def __init__(self, graph, p, evo_time, seed):
        self.graph = graph
        self.population = p
        self.best_solution = None
        self.start_time = time.time()
        self.evo_time = evo_time
        self.seed = seed
        if self.seed:
            random.seed(self.seed)

    def evolutionary(self, p, k):
        """
        given a population P, and select parents to
        make a better fitness child
        :param p: population (path-scanning random solution)
        :return:
        """
        # give 60s, and we use 60-10=50s in evolutionary
        while time.time() - self.start_time > self.evo_time-1:
            while k > 0:  # the k iteration number
                k -= 1
                pa, pb = self.select_parents(p)
                child1, child2 = crossover(pa, pb)
                # true_child = random_select(child1, child2)
                parent_fitness = min(fitness(pa), fitness(pb))
                fit_chi1 = fitness(child1)
                fit_chi2 = fitness(child2)
                if fitness(child1) < parent_fitness:  # the cost, less is better
                    #replace pa by child1
                    if fitness(child1) < fitness(self.best_solution):
                        self.best_solution = child1
                    # replace the parent which have largest cost
                    lar_cost_pa = pa if fitness(pa) > fitness(pb) else pb


def select_parent(p):
    """
    given a population, select two parents randomly from the population
    :param p:
    :return:
    """
    p1, p2 = random.sample(p, 2)


def fitness(solution):
    return solution.Cost


def crossover(pa, pb):
    """
    crossover two parents, and breed two child
    the chromosome T is a permutation of t required edges (tasks)
    :param pa: parent1
    :param pb: parent2
    :return:
        child1
        child2
    """

    pass


def mutation(solution):
    """
    mutate one solution to the new solution
    :param solution:
    :return: new_solution : the new solution
    """
    new_solution = solution.copy()
    # a simple mutation
    for task in new_solution:
        num_edge = len(task)
        mu_edge = task[num_edge-1]
        inv_edge = (mu_edge[1], mu_edge[0])
        task[num_edge-1] = inv_edge
    return new_solution

