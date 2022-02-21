import copy
import time
from src.objects.individual import Individual, Population, Fittest
from src.objects.chromosome import Chromosome, Codon
from numpy.random import choice
import random
from tqdm import tqdm
from copy import deepcopy
from common_imports import *

log = get_logger(__name__)


class Experiment:

    def __init__(self,
                 population,
                 generations,
                 p_cross,
                 p_mutate,
                 fitness_func):
        self._population = population
        self._generations = generations
        self._p_cross = p_cross
        self._p_mutate = p_mutate
        self._fitness_func = fitness_func

    @property
    def population(self):
        return self._population

    @property
    def generations(self):
        return self._generations

    @property
    def fitness_func(self):
        return self._fitness_func

    @property
    def p_cross(self):
        return self._p_cross

    @property
    def p_mutate(self):
        return self._p_mutate


class SimpleExperiment(Experiment):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pop_size = self.population.population_size

    @property
    def pop_size(self):
        return self._pop_size

    def run(self):
        new_pop = Population(
            [],
            hall_of_fame=self.population.hall_of_fame
        )
        for _ in tqdm(range(self.generations)):
            replaced = 0
            new_pop = Population(
                [],
                hall_of_fame=new_pop.hall_of_fame
            )
            # Assign fitness function to population
            self.population.apply_fitness(self.fitness_func)
            # Track fittest people
            if self.population.hall_of_fame is not None:
                for person in self.population.individuals:
                    self.population.hall_of_fame.add(person)
            while replaced < self._pop_size:
                # Sample the population for mating
                mother, father = self.population.sample_population(2)
                if random.random() < self.p_cross:
                    # Perform crossover to produce offspring
                    n_codons = mother.chromosomes[0].num_codons
                    length_codons = mother.chromosomes[0].codon_lengths
                    crossovers = choice(
                        list(range(1, length_codons + 1)),
                        n_codons
                    )
                    child1, child2 = mother.fuse(father, crossovers)
                else:
                    child1 = copy.deepcopy(mother)
                    child2 = copy.deepcopy(father)
                # Perform mutations on each child
                child1.random_mutation(self.p_mutate)
                child2.random_mutation(self.p_mutate)
                # Get fitness of the children
                child1.apply(self.fitness_func)
                child2.apply(self.fitness_func)
                # Update the hall of fame if needed
                if self.population.hall_of_fame:
                    self.population.hall_of_fame.add(child1)
                    self.population.hall_of_fame.add(child2)
                # Remove parents, add children, and update counts
                new_pop.add({child1, child2})
                replaced += 2
            if self._pop_size % 2 == 1:
                new_pop.remove(child1)
        final_pop = new_pop
        return final_pop


class VisualSimpleExperiment(Experiment):

    def __init__(self, ax, canvas, time_interval, **kwargs):
        super().__init__(**kwargs)
        self._pop_size = self.population.population_size
        self.canvas = canvas
        self.ax = ax
        self.time_interval = time_interval

    @property
    def pop_size(self):
        return self._pop_size

    def run(self):
        new_pop = Population(
            [],
            hall_of_fame=self.population.hall_of_fame
        )
        for _ in tqdm(range(self.generations)):
            replaced = 0
            new_pop = Population(
                [],
                hall_of_fame=new_pop.hall_of_fame
            )
            # Assign fitness function to population
            self.population.apply_fitness(self.fitness_func)
            # Track fittest people
            if self.population.hall_of_fame is not None:
                for person in self.population.individuals:
                    self.population.hall_of_fame.add(person)
            while replaced < self._pop_size:
                # Sample the population for mating
                mother, father = self.population.sample_population(2)
                if random.random() < self.p_cross:
                    # Perform crossover to produce offspring
                    n_codons = mother.chromosomes[0].num_codons
                    length_codons = mother.chromosomes[0].codon_lengths
                    crossovers = choice(
                        list(range(1, length_codons + 1)),
                        n_codons
                    )
                    child1, child2 = mother.fuse(father, crossovers)
                else:
                    child1 = copy.deepcopy(mother)
                    child2 = copy.deepcopy(father)
                # Perform mutations on each child
                child1.random_mutation(self.p_mutate)
                child2.random_mutation(self.p_mutate)
                # Get fitness of the children
                child1.apply(self.fitness_func)
                child2.apply(self.fitness_func)
                # Update the hall of fame if needed
                if self.population.hall_of_fame:
                    self.population.hall_of_fame.add(child1)
                    self.population.hall_of_fame.add(child2)
                # Remove parents, add children, and update counts
                new_pop.add({child1, child2})
                replaced += 2
            if self._pop_size % 2 == 1:
                new_pop.remove(child1)
            new_pop.draw(self.ax, self.canvas)
            time.sleep(self.time_interval)
        final_pop = new_pop
        return final_pop


def number_ones(chromosome):
    chrom = chromosome[0]
    chrom = chrom.codons[0].bitstring
    ans = 0
    for char in chrom:
        if char == "1":
            ans += 1
    return ans


def main():

    # Initialize the population
    nums = choice(range(256), 25)
    pop = Population(hall_of_fame=Fittest(5))
    fit = lambda x:  number_ones(x)
    print("--------- INITIAL POPULATION ----------")
    for item in nums:
        person = Individual([Chromosome([Codon(item)])])
        person.apply(fit)
        pop.add(person)
    print("Initial average fitness: ", pop.average_fitness())

    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)  # create axis
    ax.axis('off')

    final_pop = VisualSimpleExperiment(
        ax,
        None,
        .1,
        population=pop,
        generations=100,
        p_cross=.9,
        p_mutate=.001,
        fitness_func=fit
    ).run()

    print("------ FINAL POPULATION ---------")
    final_pop.apply_fitness(fit)
    print("Final average fitness: ", final_pop.average_fitness())
    for person in final_pop.individuals:
        print(person)

if __name__ == "__main__":
    main()
