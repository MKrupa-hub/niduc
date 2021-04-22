import random


class Generator:
    string_bits = ''
    size = 0
    string_bitsToCode = []
    string_codedBits = []

    def __init__(self, size, length):
        self.size = size
        self.string_bits = self._generate(size)
        self._packing(length)

    # generuje string bitów 0, 1
    # IMO wygodniej będzie się to ciąć na packet
    @staticmethod
    def _generate(size):
        temp = []
        for i in range(0, size):
            temp.append(str(random.randint(0, 1)))
        return ''.join(temp)

    # tutaj tniemy string bitów na pakiety i bity zakwalifikowane do pakietu wrzucamy do tymczasowej listy
    # PROBLEM:
    # długość stringu jest za długa/krótka i nie da się stworzyć pełnych pakietów
    def _packing(self, length):
        # pętla skacze co długość pakietu aż do końca stringa BITS
        # zakładam, że size jest wielokrotnością długości BITS
        count = 0
        for i in range(0, len(self.string_bits), length):
            self.string_bitsToCode.append(self.string_bits[i: i + length])

    # proste potrajanie/ poczwarzanie a nawet popiątnianie bitów!
    def multiple_bit(self, multiple):
        for i in range(len(self.string_bitsToCode)):
            package = self.string_bitsToCode[i]
            temp = ''
            for j in range(len(package)):
                if package[j] == '0':
                    temp += ('0' * multiple)
                else:
                    temp += ('1' * multiple)
            self.string_codedBits.append(temp)

    def show(self):
        print("Bits to code: " + str(self.string_bitsToCode) + "\n")
        print(self.string_codedBits)

