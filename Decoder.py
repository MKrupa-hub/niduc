import functools
import operator

key = [1, 0, 0, 1, 0, 1] # dzielnik XOR
keyLen = len(key)

def getCrc(packet):
    temp = packet.copy()
    for i in range(len(packet) - keyLen + 1):
        if temp[i] == 1:
            for j in range(len(key)):
                temp[i + j] = operator.xor(temp[i+j], key[j])
    return temp[len(packet) - keyLen + 1 : ]

def decodeCrc(coded):
    crc = getCrc(coded)
    how = crc.count(1)
    # Przypadek gdy bity CRC sa 0
    if how == 0:
       return coded[0: len(coded) - keyLen + 1], False
    # Przypadek gdy jest przeklamanie (1 jedynka) w CRC
    if how == 1:
        temp = coded.copy()
        for i in range(len(crc)):
            # dodaje policzone crc do oryginalnego
            temp[len(temp) - len(crc) + i] = operator.xor(temp[len(temp) - len(crc) + i], crc[i])
        return temp, True
    temp = coded.copy()
    if how >= 2:
        # Teraz przypadek gdy sa 2 jedynki
        # przesuwamy pakiet do momentu az po dzieleniu w CRC bedzie tylko 1 jedynka
        for i in range(len(temp)):
            temp.insert(0, temp[-1])
            temp.pop(len(temp) - 1)
            crcToAdd = getCrc(temp)
            if crcToAdd.count(1) == 1:
                toCheck = temp.copy()
                for j in range(len(crc)):
                    # dodaje policzone crc do oryginalnego
                    toCheck[len(toCheck) - len(crcToAdd) + j] = operator.xor(toCheck[len(toCheck) - len(crcToAdd) + j], crcToAdd[j])
                # odwracam przesuniecie
                for x in range(i+1):
                    a = toCheck[0]
                    toCheck.pop(0)
                    toCheck.append(a)
                # moze jest szansa, ze istnieja dwa takie kody CRC co maja tylko 1 jedynke
                # jednakze tylko jeden jest prawdziwy
                # SPRAWDZMY!
                checkCrc = getCrc(toCheck)
                if checkCrc.count(1) == 0:
                    return toCheck[ : len(toCheck) - keyLen + 1], True
    return temp[0: len(temp) - keyLen + 1], True

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