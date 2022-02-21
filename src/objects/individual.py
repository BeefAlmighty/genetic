from src.objects.chromosome import Chromosome, Codon
from typing import List, Iterable
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import choice
import random
import copy
from common_imports import *

log = get_logger(__name__)


class Individual:
    """
    Individuals can be haploid (single chromosome) or diploid (
    two-chromosome).
    """
    def __init__(self, chromosomes: List[Chromosome]):
        if not isinstance(chromosomes, list):
            log.warning("Chromosomes must be a list")
            self._chromosomes = [chromosomes]
        else:
            self._chromosomes = chromosomes
        self._fitness = None

    def __repr__(self):
        if len(self._chromosomes) == 1:
            return self._chromosomes[0].__repr__()
        else:
            ans = ""
            for idx, chrom in enumerate(self._chromosomes):
                ans += f"Chromosome {idx + 1}:" \
                       + chrom.__repr__() + "\n"
            return ans

    @property
    def chromosomes(self):
        return self._chromosomes

    @property
    def fitness(self):
        return self._fitness

    def update_fitness(self, num):
        self._fitness = num
        return None

    def apply(self, func):
        num = func(self.chromosomes)
        self.update_fitness(num)
        return None

    def fuse(self, individual, crossovers):
        """
        Mating of two individuals.  Crossover points for each codon
        within a chromosome are help in crossovers iterable.

        :param individual: Individual to mate with calling individual
        :param crossovers: Points of crossover for fusion
        :return: Pair of new individuals
        """
        chrom1 = self.chromosomes
        chrom2 = individual.chromosomes

        new_chrom1, new_chrom2 = [], []
        for idx, item in enumerate(zip(chrom1, chrom2)):
            temp1, temp2 = item[0].fuse(item[1], [crossovers[idx]])
            new_chrom1.append(temp1)
            new_chrom2.append(temp2)
        return Individual(new_chrom1), Individual(new_chrom2)

    def mutate(self, positions):
        for chrom in self._chromosomes:
            chrom.mutate(positions)
        return

    def random_mutation(self, p_mutate):
        mutation_dict = {}
        n_codons = self.chromosomes[0].num_codons
        length_codons = self.chromosomes[0].codon_lengths
        for idx in range(n_codons):
            mutation_dict[idx] = []
            for item in range(length_codons):
                if random.random() < p_mutate:
                    mutation_dict[idx].append(item)
        self.mutate(mutation_dict)
        return None

    def to_list(self):
        chromes = [item.to_list()[0] for item in self._chromosomes]
        return "".join(chromes)

class Population:

    def __init__(self,
                 individuals: Iterable[Individual] = [],
                 hall_of_fame = None
                 ):
        self._individuals = list(individuals)
        self._population_size = len(self._individuals)
        self._hall_of_fame = hall_of_fame

    @property
    def individuals(self):
        return self._individuals

    @property
    def population_size(self):
        return self._population_size

    @property
    def hall_of_fame(self):
        return self._hall_of_fame

    def to_array(self):
        ans = []
        for person in self._individuals:
            person_list = [int(item) for item in person.to_list()]
            ans.append(person_list)
        return np.array(ans)

    def draw(self, ax, canvas):
        ax.imshow(self.to_array())
        return None

    def add(self, member):
        if not isinstance(member, Iterable):
            member = [member]
        for item in member:
            self._individuals += [item]
            self._population_size += 1
        return None

    def remove(self, member):
        if not isinstance(member, Iterable):
            member = [member]
        for item in member:
            self._individuals.remove(item)
            self._population_size -= 1
        return None

    def apply_fitness(self, func):
        for member in self._individuals:
            member.apply(func)
        return None

    def average_fitness(self):
        ans = 0
        for person in self._individuals:
            ans += person.fitness
        return ans / self._population_size

    def sample_population(self, num, method="roulette"):
        """
        Implements roulette wheel sampling from the population where
        probability of being selected is based on fraction of total
        fitness an individual has.
        :param num: Number of individuals to return
        :param method: Type of sampling to use (roulette is default)
        :return: Tuple of Individual objects drawn from the population
        """
        if method == "roulette":
            probs = list(map(lambda x: x.fitness, self.individuals))
            prob_sum = sum(probs)
            probs = [
                item / prob_sum for item in probs
            ]
        else:
            log.error(f"Method {method} not implemented")
            return tuple(num * [None])
        members = choice(self.individuals, num, p=probs)
        return members

    def evolve_one_step(self,
                        p_cross,
                        p_mutate,
                        fitness_func
                        ):
        replaced = 0
        new_pop = Population(
            [],
        )
        # Assign fitness function to population
        self.apply_fitness(fitness_func)
        # Track fittest people
        if self.hall_of_fame is not None:
            for person in self._individuals:
                self.hall_of_fame.add(person)
        while replaced < self._population_size:
            # Sample the population for mating
            mother, father = self.sample_population(2)
            if random.random() < p_cross:
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
            child1.random_mutation(p_mutate)
            child2.random_mutation(p_mutate)
            # Get fitness of the children
            child1.apply(fitness_func)
            child2.apply(fitness_func)
            # Update the hall of fame if needed
            if self.hall_of_fame:
                self.hall_of_fame.add(child1)
                self.hall_of_fame.add(child2)
            # Remove parents, add children, and update counts
            new_pop.add({child1, child2})
            replaced += 2
        if self._population_size % 2 == 1:
            new_pop.remove(child1)
        self._individuals = new_pop.individuals
        return None

class Fittest:
    """
    Class to maintain the fittest members of a population
    """
    def __init__(self, num):
        self.num = num
        self.queue = self.num * [Individual([Codon(0)])]
        for item in self.queue:
            item.update_fitness(0)

    def __repr__(self):
        ans = "{" + f"\n -- Top {self.num} individuals -- \n"
        for person in self.queue:
            ans += "\t" + person.__repr__() + "\n"
        ans += "}"
        return ans

    def add(self, person: Individual):
        flag = False
        if person.fitness >= self.queue[-1].fitness:
            for idx in range(self.num):
                if self.queue[idx].fitness < person.fitness:
                    last = self.queue[idx:-1]
                    self.queue[idx] = person
                    flag = True
                    break
            if flag:
                self.queue = self.queue[: idx + 1] + last
            return None
        else:
            return None



def main():

    def number_ones(chromosomes):
        chrom = chromosomes[0]
        chrom = chrom.codons[0].bitstring
        ans = 0
        for char in chrom:
            if char == "1":
                ans += 1
        return ans

    nums = choice(range(256), 5)
    pop = Population()
    print("--------- INITIAL POPULATION ----------")
    for item in nums:
        person = Individual([Chromosome([Codon(item)])])
        person.apply(number_ones)
        pop.add(person)

    hof = Fittest(3)
    for person in pop.individuals:
        hof.add(person)

    print(pop.to_array())




if __name__ == "__main__":
    main()
