from src.objects.chromosome import Chromosome, Codon
from typing import List, Iterable
from numpy.random import choice
import random
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


class Population:

    def __init__(self, individuals: Iterable[Individual] = []):
        self._individuals = list(individuals)
        self._population_size = len(self._individuals)

    @property
    def individuals(self):
        return self._individuals

    @property
    def population_size(self):
        return self._population_size

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
            probs = [
                item / sum(probs) for item in probs
            ]
        else:
            log.error(f"Method {method} not implemented")
            return tuple(num * [None])
        members = choice(self.individuals, num, p=probs)
        return members


def main():
    chrom = Chromosome([Codon(42)])
    person = Individual(chrom)
    print(person)
    person.random_mutation(.9)
    print(person)
    person.random_mutation(.9)
    print(person)
    person.random_mutation(1)
    print(person)

    print(person)

    def number_ones(chromosomes):
        chrom = chromosomes[0]
        chrom = chrom.codons[0].bitstring
        ans = 0
        for char in chrom:
            if char == "1":
                ans += 1
        return ans

    person.apply(number_ones)
    print(person.fitness)


if __name__ == "__main__":
    main()
