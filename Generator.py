import random
import functools
import operator

key = [1, 0, 0, 1, 0, 1] # dzielnik XOR

def packing(length):
     package = []
     for i in range(length):
        package.append(random.randint(0,1))
     return package

def multiple_bit(multiple, package):
    temp = []
    for j in range(len(package)):
        if package[j] == 0:
            [temp.append(0) for i in range(multiple)]
        else:
            [temp.append(1) for i in range(multiple)]
    return temp

def code_crc(packet):
    tmp = packet.copy()
    temp = packet.copy() # do ciagu danych dodaje 3 wyzerowane bity
    for i in range(len(key) - 1):
        temp.append(0)
    # jezeli nad najstarsza pozycja dzielnika jest 0 to przesuwam dzielnik w prawo aż do napotkania 1
    for i in range(len(packet)):
        if temp[i] == 1:
            for j in range(len(key)):
                temp[i + j] = operator.xor(temp[i+j], key[j])
    # dodaje bity CRC do pakietu
    size = len(packet)
    for i in range(size, size + len(key) - 1):
        tmp.append(temp[i])
    return tmp

# HARDCODE
# Dziala dla 11 bitowego pakietu
def code_hamming(package):
    parity = [1,2,4,8]
    bits = package.copy()
    bits.insert(0, 0)
    bits.insert(1, 0)
    bits.insert(2, 0)
    bits.insert(4, 0)
    bits.insert(8, 0)
    toSet = functools.reduce(operator.xor, [i for i, bit in enumerate(bits) if bit], 0)
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
