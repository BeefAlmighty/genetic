from src.objects.chromosome import Chromosome
from typing import List, Iterable


class Individual:
    """
    Individuals can be haploid (single chromosome) or diploid (
    two-chromosome).
    """
    def __init__(self, chromosomes: List[Chromosome]):
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

    def get_chromosomes(self):
        return self._chromosomes

    def update_fitness(self, num):
        self._fitness = num
        return None

    def apply(self, func):
        num = func(self._chromosomes)
        self.update_fitness(num)
        return None

    def get_fitness(self):
        return self._fitness

    def fuse(self, individual, crossovers):
        """
        Mating of two individuals.  Crossover points for each codon
        within a chromosome are help in crossovers iterable.

        :param individual: Individual to mate with calling individual
        :param crossovers: Points of crossover for fusion
        :return: Pair of new individuals
        """
        chrom1 = self.get_chromosomes()
        chrom2 = individual.get_chromosomes()

        new_chrom1, new_chrom2 = [], []
        for idx, item in enumerate(zip(chrom1, chrom2)):
            temp1, temp2 = item[0].fuse(item[1], crossovers[idx])
            new_chrom1.append(temp1)
            new_chrom2.append(temp2)
        return

    def mutate(self, positions):
        for chrom in self._chromosomes:
            chrom.mutate(positions)
        return


class Population:

    def __init__(self, individuals: Iterable[Individual] = []):
        self._individuals = list(individuals)
        self._population_size = len(self._individuals)

    def get_population_size(self):
        return self._population_size

    def add_individual(self, individual: Individual):
        self._individuals += [individual]
        self._population_size += 1
        return None

    def remove_individual(self, individual):
        self._individuals.remove(individual)
        self._population_size -= 1
        return None

    def get_individuals(self):
        return self._individuals

def main():
    pass


if __name__ == "__main__":
    main()
