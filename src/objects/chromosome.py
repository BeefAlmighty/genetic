from src.utils import helpers as h
from common_imports import *
from typing import Iterable

log = get_logger(__name__)


class Codon:
    """
    Codons will represent small bits of genetic material so that a
    chromosome can, if we so choose, be made of multiple codons.
    """

    def __init__(self,
                 num=0,
                 bitstring="",
                 length=8):
        self.encoder = h.Encoder(max_len=length)
        self._num = num
        if not bitstring:
            self._bitstring = self.encode()
        else:
            self._bitstring = bitstring

    def __repr__(self):
        return self._bitstring

    def __len__(self):
        return len(self._bitstring)

    def get_num(self):
        return self.decode()

    @property
    def bitstring(self):
        return self._bitstring

    def encode(self):
        return self.encoder.encode_num_to_bitstring(self._num)

    def decode(self):
        return self.encoder.decode_bitstring_to_num(self._num)

    def mutate(self, position):
        temp = list(self._bitstring)
        try:
            if temp[position] == "0":
                temp[position] = "1"
            else:
                temp[position] = "0"
            self._bitstring = "".join(temp)
        except KeyError:
            log.error("Position for mutation is out of bounds")
        return None

    def fuse(self,
             codon,
             crosspoint):
        """
        Fuse together two codons with a single crosspoint. Crosspoint
        parameter uses mathematical indexing starting at 1 instead of
        the more common Pythonic 0 based indexing. This means the first
        <crossover> number of characters from each string remain in
        place, so crossing over begins at <crossover>.  If
        <crossover> is equal to 1, the entire codons swap.  Will not
        perform any swap if passed negative crosspoint.

        :param codon: Codon object to be fused to calling object
        :param crosspoint: Location in the bitstring at which to fuse
        :return: Two offspring codons joined by the 2 fusions
        """
        if len(codon) != self.__len__():
            log.error("Cannot fuse codons of different length")
            return None, None
        elif crosspoint < 1 or crosspoint > self.__len__():
            log.error("Crossing over out of bounds!")
            return None, None
        if crosspoint <= 0:
            return self, codon
        crosspoint -= 1
        first_half_1 = self.bitstring[:crosspoint]
        first_half_2 = codon.bitstring[:crosspoint]
        second_half_1 = self.bitstring[crosspoint:]
        second_half_2 = codon.bitstring[crosspoint:]
        codon_1 = Codon(bitstring=first_half_1 + second_half_2,
                        length=self.__len__())
        codon_2 = Codon(bitstring=first_half_2 + second_half_1,
                        length=self.__len__())
        return codon_1, codon_2


class Chromosome:
    """
    Chromosome class.  The chromosome is mostly a wrapper for a codon
    in case of a single codon, but keeps codons isolated in case of
    multiple codons.
    """

    def __init__(self, codons: list = []):
        # Determine that all codons are same length.
        lengths = filter(
            lambda x: x != len(codons[0]),
            map(len, codons)
        )
        assert len(list(lengths)) == 0
        self._codons = codons
        self._num_codons = len(codons)
        self._codon_lengths = len(codons[0])

    def __repr__(self):
        ans = ""
        for codon in self._codons:
            ans += codon.bitstring + " | "
        return ans.rstrip(" | ")

    @property
    def codons(self):
        return self._codons

    @property
    def num_codons(self):
        return self._num_codons

    @property
    def codon_lengths(self):
        return self._codon_lengths

    def fuse(self,
             chrom,
             crossovers: Iterable):
        """
        Fusion of two chromosome with the calling chromosome. Fusion
        consists of fusing all the constituent codons at the given
        crossover locations.

        :param chrom: Chromosome to fuse to calling chromosome
        :param crossovers: Iterable of locations to cross in the
        codons.
        :return: Pair of fused chromosomes.
        """
        if self._num_codons != len(chrom.codons) \
                or self.codon_lengths != chrom.codon_lengths \
                or len(crossovers) != self.num_codons:
            log.error("Cannot fuse incompatible chromosomes")
            return None, None
        codon_list_1 = []
        codon_list_2 = []
        for item in zip(self.codons,
                        chrom.codons,
                        crossovers):
            cod1, cod2 = item[0].fuse(item[1], item[2])
            codon_list_1.append(cod1)
            codon_list_2.append(cod2)
        return Chromosome(codon_list_1), Chromosome(codon_list_2)

    def mutate(self, positions: dict):
        """
        Mutate codons within a chromosome at given positions.
        :param positions: dictionary of positions to mutate each
        codon.  Key value pairs are (codon_index, [positions])
        :return: None
        """
        codons = self.codons
        for codon in positions:
            for position in positions[codon]:
                codons[codon].mutate(position)
        return None

def main():
    cod1 = Codon(0)
    cod2 = Codon(255)
    # print("First codon: ", cod1)
    # print("Second codon: ", cod2)
    # print("Fusion: ", cod1.fuse(cod2, 8))

    #
    # cod1 = Codon(42)
    # print("First codon: ", cod1)
    # cod2 = Codon(15)
    # print("Second codon: ", cod2)
    #
    # print("Fusion of codons: ", cod1.fuse(cod2, 3))

    chrom1 = Chromosome([cod1, cod2])
    print("First Chromosome: ", chrom1)

    chrom2 = Chromosome([Codon(13), Codon(81)])
    print("Second Chromosome: ", chrom2)

    print("Fusion of chromosomes: ", chrom1.fuse(chrom2, [2, 6]))
    chrom2.mutate({0: [1, 3], 1: [0, 1]})
    print("Mutation: ", chrom2)

if __name__ == "__main__":
    main()
