import time


class EvoSolves:

    def __init__(self, p, s_time, evo_time=50):
        self.population = p
        self.best_solution = None
        self.start_time = s_time
        self.evo_time = evo_time

    def evolutionary(self, p):
        """
        given a population P, and select parents to
        make a better fitness child
        :param p: population (path-scanning random solution)
        :return:
        """
        # give 60s, and we use 60-10=50s in evolutionary
        while time.time() - self.start_time > self.evo_time:
            while True:  # the k iteration number
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


    def select_parent(self, p):
        """
        given a population, select two parents randoms
        :param p:
        :return:
        """
        pass


def fitness(solution):
    return solution.Cost
    pass


def crossover(pa, pb):
    """
    crossover two parents, and breed two child
    :param pa: parent1
    :param pb: parent2
    :return:
        child1
        child2
    """
    pass

