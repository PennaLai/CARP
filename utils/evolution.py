import time
import random
from CARP_solver import Solution

class EvoSolves:

    def __init__(self, graph, p, evo_time, seed):
        self.graph = graph
        self.population = p
        self.best_solution = p[0]
        self.start_time = time.time()
        self.evo_time = evo_time
        self.seed = seed
        if self.seed:
            random.seed(self.seed)

    def evolutionary(self, p):
        """
        given a population P, and select parents to
        make a better fitness child
        :param p: population (path-scanning random solution)
        :return:
        """
        while True:  # if time allow, do it
            if time.time() - self.start_time > self.evo_time - 2:
                break
            pa, pa_index = self.select_parent(p)
            pb, pb_index = self.select_parent(p)
            child1 = self.crossover(pa, pb)
            child2 = self.crossover(pb, pa)
            best_child = select_child(child1, child2)
            if fitness(pa) > fitness(pb):
                worse_parent, worse_index = pa, pa_index
            else:
                worse_parent, worse_index = pb, pb_index
            if fitness(best_child) < min(fitness(pa), fitness(pb)):  # if the child is better the worse one, replace it
                if fitness(best_child) < fitness(self.best_solution):
                    self.best_solution = best_child
                # replace the parent which have largest cost
                if fitness(best_child) < fitness(worse_parent):
                    p[worse_index] = best_child  # replace its father
        return p

    def mutation(self):
        pass

    def all_flip_mutation(self, solution):
        """
        mutate one solution to the new solution
        this time, we flip every edge to find a better solution, return a new solution that must not bad than previous one
        :param solution:
        :return: new_solution : the new solution
        """
        new_route = solution.Route.copy()
        cost = solution.Cost
        new_cost = 0
        # a simple mutation
        for task in new_route:
            edge_index = 0
            for edge in task:
                inv_edge = (edge[1], edge[0])
                task[edge_index] = inv_edge
                new_cost = self.graph.calculate_cost(new_route)
                if new_cost >= cost:
                    task[edge_index] = edge  # if worse, change back and nothing happen
                else:
                    cost = new_cost
                edge_index += 1
        new_cost = self.graph.calculate_cost(new_route)
        return Solution(Route=new_route, Cost=new_cost)

    def flip_mutation(self, solution):
        route = solution.Route
        r1 = random.randint(0, len(route))
        r2 = random.randint(0, len(route[r1]))
        edge = route[r1][r2]
        flip = (edge[1], edge[0])
        route[r1][r2] = flip
        cost = self.graph.calculate_cost(route)
        return Solution(Route=route, Cost=cost)

    def single_insertion_mutation(self):
        pass

    def swap_mutation(self):
        pass

    def population_mutate(self):
        """
        this function just to mutate every solution in the population
        it cost lot of time, and it may be no use for the answer
        so it just a extra function
        :return:
        """
        index = 0
        for p in self.population:
            self.population[index] = self.mutation(p)
            index += 1

    def select_parent(self, p):
        """
        given a population, we assume that the population is ordered with the cost from low to high
        select two parents randomly from the population
        :param p: population
        :return: two parent
        """
        total_cost = sum([x.Cost for x in p])
        r = random.randint(0, total_cost)
        acc_cost = 0
        index = 0
        for i in p:
            acc_cost += i.Cost
            if r <= acc_cost:
                return i, index
            index += 1


    def crossover(self, pa, pb):
        """
        crossover two parents, and breed two child
        the chromosome T is a permutation of t required edges (tasks)
        we keep the consecutive genes of pa, and use pb to fill the remain task
        :param pa: parent1 that give a consecutive genes
        :param pb: parent2 give the remain genes
        :return:
            child
        """
        free_edge = [edge for edge in self.graph.edge_set.keys() if self.graph.edge_set[edge].Demand != 0]
        child_route = []
        a_route = pa.Route
        b_route = pb.Route
        # the pa part
        pa_route_num = len(a_route)
        r = random.randint(0, pa_route_num-1)
        pa_gene_task = a_route[r]
        # capacity
        capa = self.graph.capa
        # remove the edge from free_edge, the left edge still need to add in
        for edge in pa_gene_task:
            right_direction_edge = edge if edge in self.graph.edge_set else (edge[1], edge[0])
            if right_direction_edge in free_edge:
                free_edge.remove(right_direction_edge)
        child_route.append(pa_gene_task)
        # the pb part
        child_route.append([])
        route_cap = capa

        for task in b_route:
            for edge in task:
                if not free_edge:  # if free edge is empty break
                    break
                # correct the direction and query their demand
                right_direction_edge = edge if edge in self.graph.edge_set else (edge[1], edge[0])
                if right_direction_edge not in free_edge:
                    continue
                demand = self.graph.edge_set[right_direction_edge].Demand
                if route_cap - demand >= 0:  # add in
                    child_route[-1].append(edge)
                else:  # if this task can not pack it, create new task, renew the route_cap
                    child_route.append([])
                    child_route[-1].append(edge)
                    route_cap = capa
                free_edge.remove(right_direction_edge)
                route_cap -= demand
        cost = self.graph.calculate_cost(child_route)
        solution = Solution(Route=child_route, Cost=cost)
        return solution


def select_child(child1, child2):
    return child1 if fitness(child1) < fitness(child2) else child2

def fitness(solution):
    return solution.Cost







