from src.utils import helpers as h
from common_imports import *

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

    def get_bitstring(self):
        return self._bitstring

    def encode(self):
        return self.encoder.encode_num_to_bitstring(self._num)

    def decode(self):
        return self.encoder.decode_bitstring_to_num(self._num)

    def mutate(self, position):
        temp = list(self._bitstring)
        if temp[position] == "0":
            temp[position] = "1"
        else:
            temp[position] = "0"
        self._bitstring = "".join(temp)
        return None

    def fuse(self,
             codon,
             crosspoint):
        if len(codon) != self.__len__():
            log.error("Cannot fuse codons of different length")
            return None, None
        elif crosspoint < 1 or crosspoint > self.__len__():
            log.error("Crossing over out of bounds!")
            return None, None
        crosspoint -= 1
        first_half_1 = self._bitstring[:crosspoint]
        first_half_2 = codon.get_bitstring()[:crosspoint]
        second_half_1 = self._bitstring[crosspoint:]
        second_half_2 = codon.get_bitstring()[crosspoint:]
        codon_1 = Codon(bitstring=first_half_1 + second_half_2,
                        length=self.__len__())
        codon_2 = Codon(bitstring = first_half_2 + second_half_1,
                        length=self.__len__())
        return codon_1, codon_2



class Chromosome:
    """
    Chromosome class.  The chromosome is mostly a wrapper for a codon
    in case of a single codon, but keeps codons isolated in case of
    multiple codons.
    """
    def __init__(self, codons: list=[]):
        self._codons = codons

    def __repr__(self):
        ans = ""
        for codon in self._codons:
            ans += codon.get_bitstring() + " | "
        return ans.rstrip(" | ")

    def get_codons(self):
        return self._codons


def main():
    cod1 = Codon(42)
    print(cod1)
    cod2 = Codon(15)
    print(cod2)

    print(cod1.fuse(cod2, 0))

    # chrom = Chromosome([cod1])
    # print(chrom)

if __name__ == "__main__":
    main()
