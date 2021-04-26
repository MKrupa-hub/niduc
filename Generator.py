import random

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
    # kodowanie jest proste. Dodajemy bity parzystosci na pozycjach potegi 2
    def code_hamming(self, package):
        list = [0,0,0,0]
        package.insert(0, '0')
        for i in range(16):
            if 2**i > 15:
                break
            package.insert(2**i, '0')
        # ustawianie bitow parzystosci
        # ustawienie pierwszego bitu
        for j in range(3, 16, 2):
             if package[j] == '1':
                 list[0] += 1
        if list[0] % 2 == 0:
            package[1] = '0'
        else:
            package[1] = '1'
         # drugi bit, pozycje 3, 6,7, 10,11, 14,15
        for j in range(3, 16, 3):
            if package[j] == '1':
                list[1] += 1
            if j % 2 == 0:
                j += 1
                if package[j] == '1':
                    list[1] += 1
        if list[1] % 2 == 0:
            package[2] = '0'
        else:
            package[2] = '1'
        # trzeci bit, pozycje 5-7, 12-15
        for j in range(5, 15, 5):
            for x in range(2):
                if package[j+x] == '1':
                    list[2] += 1
        if list[2] % 2 == 0:
            package[4] = '0'
        else:
            package[4] = '1'
        # czwarty bit, pozycje 9 -15
        for j in range(8, 16, 1):
             if package[j] == '1':
                 list[3] += 1

        if list[3] % 2 == 0:
            package[8] = '0'
        else:
            package[8] = '1'

        count = 0
        for j in range(1, 16):
            if package[j] == '1':
                count += 1
        if count % 2 == 0:
            package[0] = '0'
        else:
            package[0] = '1'

        return package
