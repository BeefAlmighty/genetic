from src.objects.chromosome import Chromosome
from typing import List


class Individual:
    """
    Individuals can be haploid (single chromosome) or diploid (
    two-chromosome).
    """
    def __init__(self, chromosomes: List[Chromosome]):
        self._chromosomes = chromosomes

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


def main():
    pass


if __name__ == "__main__":
    main()
