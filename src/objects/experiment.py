import copy

from src.objects.individual import Individual, Population
from src.objects.chromosome import Chromosome, Codon
from numpy.random import choice
import random
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
        count = 1
        while count < self.generations:
            replaced = 0
            new_pop = Population([])
            while replaced < self._pop_size:
                # Assign fitness function to population
                self.population.apply_fitness(self.fitness_func)
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
                # Remove parents, add children, and update counts
                new_pop.add({child1, child2})
                replaced += 2
            if self._pop_size % 2 == 1:
                new_pop.remove(child1)
            count += 1
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
    nums = choice(range(256), 21)
    pop = Population()
    print("--------- INITIAL POPULATION ----------")
    for item in nums:
        person = Individual([Chromosome([Codon(item)])])
        person.apply(number_ones)
        pop.add(person)
        print(person)
    print("Initial average fitness: ", pop.average_fitness())


    final_pop = SimpleExperiment(
        population=pop,
        generations=150,
        p_cross=.7,
        p_mutate=.001,
        fitness_func=number_ones
    ).run()

    print("------ FINAL POPULATION ---------")
    final_pop.apply_fitness(number_ones)
    for person in final_pop.individuals:
        print(person)
    print("Final average fitness: ", final_pop.average_fitness())
    print(final_pop.population_size)

if __name__ == "__main__":
    main()
