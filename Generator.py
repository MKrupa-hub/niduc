import random
import functools
import operator

key = ['1', '0', '1', '1'] # dzielnik XOR
size = len(key)

def XOR(a, b):
    if a == b:
        return '0'
    if a != b:
        return '1'


class Generator:
    def __init__(self):
        pass

    def packing(self, length):
        package = []
        for i in range(length):
            package.append(str(random.randint(0,1)))
        return package

    def multiple_bit(self, multiple, package):
        temp = []
        for j in range(len(package)):
            if package[j] == '0':
                [temp.append('0') for i in range(multiple)]
            else:
                [temp.append('1') for i in range(multiple)]
        return temp

    def code_crc(self, package):
        crc = package.copy() # kopia pakietu
        tmp = package.copy() # do ciagu danych dodaje 3 wyzerowane bity
        for i in range(size - 1):
            tmp.append('0')
        bits = len(crc) # dlugosc orginalnego ciagu
        # jezeli nad najstarsza pozycja dzielnika jest 0 to przesuwam dzielnik w prawo aż do napotkania 1
        for i in range(bits):
            if tmp[i] == '1':
                for j in range(len(key)):
                    tmp[i + j] = XOR(tmp[i+j], key[j]) # XOR pomiedzy dzielnikiem a danymi
        for i in range(len(crc), len(crc)+len(key) - 1):
            crc.append(tmp[i])
        return crc

    # dziala dla 11 bitow w pakiecie
    def code_hamming(self, package):
        parity = [1,2,4,8]
        bits = []
        for i in range(len(package)):
            if package[i] == '1':
                bits.append(1)
            elif package[i] == '0':
                bits.append(0)
        bits.insert(0, 0)
        bits.insert(1, 0)
        bits.insert(2, 0)
        bits.insert(4, 0)
        bits.insert(8, 0)
        toSet = functools.reduce(operator.xor, [i for i, bit in enumerate(bits) if bit])
        for i in range(5):
            if toSet & (1 << i):
                bits[parity[i]] = int(not bits[parity[i]])
        # teraz ustawiam bit 0
        count = 0
        for i in range(1, len(bits)):
            if bits[i] == 1:
                count += 1
        if count % 2 != 0:
            bits[0] = 1
        return bits
