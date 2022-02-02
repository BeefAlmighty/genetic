from src.objects.individual import Individual, Population
from src.objects.chromosome import Chromosome, Codon
from numpy.random import choice
import random
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

    def get_population(self):
        return self._population

    def get_generations(self):
        return self._generations

    def get_fitness_func(self):
        return self._fitness_func

    def get_p_cross(self):
        return self._p_cross

    def get_p_mutate(self):
        return self._p_mutate


class SimpleExperiment(Experiment):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pop_size = self.get_population().get_population_size()

    def run(self):
        count = 1
        while count < self._generations:
            replaced = 0
            while replaced < self._pop_size:
                # Assign fitness function to population
                for member in self._population.get_individuals():
                    member.apply(self._fitness_func)
                # Sample the population for mating
                probs = list(
                    map(lambda x: x.get_fitness(),
                        self._population.get_individuals())
                )
                probs = [
                    item / sum(probs) for item in probs
                ]
                mother, father = choice(
                    self._population.get_individuals(),
                    2,
                    p=probs
                )
                n_codons = mother.get_chromosomes()[0].get_num_codons()
                length_codons = mother.get_chromosomes()[0].get_codon_lengths()

                if random.random() < self._p_cross:
                    # Perform crossover to produce offspring
                    crossovers = choice(
                        list(range(1, length_codons + 1)),
                        n_codons
                    )
                    child1, child2 = mother.fuse(father, crossovers)
                else:
                    child1 = mother
                    child2 = father
                # Perform mutations on each child
                mutation_dict = {}
                for idx in range(n_codons):
                    mutation_dict[idx] = []
                    for item in range(length_codons):
                        if random.random() < self._p_mutate:
                            mutation_dict[idx].append(item)
                child1.mutate(mutation_dict)
                mutation_dict = {}
                for idx in range(n_codons):
                    mutation_dict[idx] = []
                    for item in range(length_codons):
                        if random.random() < self._p_mutate:
                            mutation_dict[idx].append(item)
                child2.mutate(mutation_dict)
                self._population.remove_individual(father)
                self._population.remove_individual(mother)
                self._population.add_individual(child1)
                self._population.add_individual(child2)
                replaced += 2
            count += 1
        return


def number_ones(chromosome):
    chrom = chromosome[0]
    chrom = chrom.get_codons()[0].get_bitstring()
    ans = 0
    for char in chrom:
        if char == "1":
            ans += 1
    return ans


def main():
    nums = choice(range(256), 20)
    pop = Population()
    for item in nums:
        person = Individual([Chromosome([Codon(item)])])
        pop.add_individual(person)
        print(person)
    SimpleExperiment(
        population=pop,
        generations=5,
        p_cross=.7,
        p_mutate=.001,
        fitness_func=number_ones
    ).run()


if __name__ == "__main__":
    main()
