import functools
import operator

key = [1, 0, 0, 1, 0, 1] # dzielnik XOR
keyLen = len(key)

def decodeCrc(coded, fixed):
    temp = coded.copy()
    for i in range(len(coded) - keyLen + 1):
        if temp[i] == 1:
            for j in range(len(key)):
                temp[i + j] = operator.xor(temp[i+j], key[j])
    crc = temp[len(coded) - keyLen + 1 : ]
    # Przypadek gdy bity CRC sa 0
    how = crc.count(0)
    if how == keyLen - 1:
       return coded[0: len(coded) - keyLen + 1], fixed
    # Przypadek gdy jest przeklamanie w CRC
    if how == keyLen - 2:
        if not fixed:
            for i in range(len(crc)):
                coded[len(coded) - len(crc) + i] = operator.xor(coded[len(coded) - len(crc) + i], crc[i])
            return decodeCrc(coded, True)
    temp = coded.copy()
    return helper(temp, 0), True

def helper(packet, count):
    if count == len(packet):
        return None
    packet.insert(0, packet[-1])
    packet.pop(len(packet) - 1)
    temp = packet.copy()
    for i in range(len(packet) - keyLen + 1):
        if temp[i] == 1:
            for j in range(len(key)):
                temp[i + j] = operator.xor(temp[i+j], key[j])
    crc = temp[len(packet) - keyLen + 1:]
    if crc.count(1) == 1:
        for i in range(len(crc)):
            packet[len(packet) - len(crc) + i] = operator.xor(packet[len(packet) - len(crc) + i], crc[i])
        for x in range(count + 1):
            a = packet[0]
            packet.pop(0)
            packet.append(a)
        return packet[0: len(packet) - keyLen + 1]
    return helper(packet, count + 1)

# dekodowanie (dla powtarzania bitu 3 razy):
# zakładam, że najbardziej prawdopodobne jest wystąpienie pojedyńczego błędu:
# 000 nadano 0
# 010 odebrano 0
# W przypadku gdy wystąpi więcej błędów to pakiet jest nienaprawialny
def decodeMulti(coded, multi):
    # jezeli sa same 0 lub 1 to pakiet jest oznaczany jako poprawnie przeslany
    decoded = []
    fixed = False
    for size in range(0, len(coded), multi):
        # laduje 3 bity pakietu do testu czy sa dobrze przeslane lub wymagaja naprawy
        temp = [coded[size + i] for i in range(multi)]
        if temp.count(0) == multi:
            decoded.append(0)
            continue
        elif temp.count(1) == multi:
            decoded.append(1)
            continue
        # proba naprawy pakietu
        if temp.count(0) > multi /2:
            decoded.append(0)
            fixed = True
        elif temp.count(1) > multi /2:
            decoded.append(1)
            fixed = True
    return decoded, fixed

# HARDCODE
# Dziala dla 11 bitow
def decode_hamming(bits):
    toFix = functools.reduce(operator.xor, [i for i, bit in enumerate(bits) if bit], 0)
    if toFix:
        bits[toFix] = int(not bits[toFix])
    bits.pop(0)
    bits.pop(0)
    bits.pop(0)
    bits.pop(1)
    bits.pop(4)
    return bits, bool(toFix)