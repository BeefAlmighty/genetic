from common_imports import *

log = get_logger(__name__)


class Encoder:
    """
    Class for encoding and decoding byte strings.  String length is
    the main parameter needed.
    """

    def __init__(self, max_len=8, base=2):
        self._len = max_len
        self._base = base
        self.max_num = self.find_max_num()

    def find_max_num(self):
        temp = 1
        bases = [temp]
        for idx in range(self._len - 1):
            temp *= self._base
            bases.append(temp)
        return (self._base - 1) * sum(bases)

    def encode_num_to_bitstring(self, num):
        if num > self.max_num:
            log.error(f"Can only encode numbers as big as "
                      f"{self.max_num} -- ")
            return ""
        ans = self._len * ["0"]
        max_exp = self._len - 1
        temp = self._base ** max_exp
        for idx in range(self._len):
            if temp > num:
                temp /= self._base
                max_exp -= 1
            else:
                ans[self._len - max_exp - 1] = str(int(num // temp))
                num -= temp
                max_exp -= 1
                temp /= self._base
        return "".join(ans)

    def decode_bitstring_to_num(self, string):
        if len(string) != self._len:
            log.error(f"Bit string must be {self._len} "
                      f"characters long -- ")
            return None
        else:
            ans = 0
            for idx in range(self._len):
                if string[idx] != "0":
                    ans += int(string[idx]) * self._base ** (
                            self._len - idx - 1)
            return ans


def main():
    enc = Encoder(max_len=8)
    print(enc.encode_num_to_bitstring(3))
    print(enc.encode_num_to_bitstring(15))
    print(enc.encode_num_to_bitstring(12))
    print(enc.decode_bitstring_to_num("00010101"))


if __name__ == "__main__":
    main()
