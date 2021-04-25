from Generator import Generator
from Decoder import Decoder
import idk

import functools
import random

gene = Generator()
deco = Decoder()

multi = 3 # ile bitow powtarzany
length = 3 # dlugosc pakietu
test = 10 # do testu przesylu. Ile pakietow wysylamy

good = 0
fixedPacket = 0
fixedNotGood = 0
undetected = 0

# Kanal transmisyjny BSC
# mamy zakodowany pakiet, przysylamy go przez kanal
# jest prawdopodobienstwo ze zamienimy bit w pakiecie na przeciwny
# elo
# przesylamy 10 pakietow po 3 bity kazdy
for j in range(test):
    packet = gene.packing(length)
    coded = gene.multiple_bit(multi, packet)
    for i in range(len(coded)):
        if random.random() < 0.1:
            if coded[i] == '0':
                coded[i] = '1'
            else:
                coded[i] = '0'
    decoded, fixed = deco.decodeMulti(coded, multi)
    # Musimy teraz ocenic ile pakietow zostalo przeslanych bez bledow, ile mialo bledy i czy udalo sie je naprawic. ORAZ ile niewykrytych bledow wystapilo
    if fixed:
        # Wystapila naprawa przy dekoderze. Sprawdzam czy naprawil poprawnie. Robie to przez porowanie listy przed i po wysyle
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q, packet, decoded), True):
            fixedPacket += 1
        else:
            fixedNotGood += 1
    else:
        # Nie wystapila naprawa ale moze wystapil niewykryty blada
        if functools.reduce(lambda x, y : x and y, map(lambda p, q: p == q, packet, decoded), True):
            good += 1
        else:
            undetected += 1
    print(packet)
    print(str(idk.code_crc(packet)))
    print(str(idk.decode_crc(good, fixedPacket, fixedNotGood, packet)))

print(
    'Bez bledow: ' + str(good) +
    '\nNaprawione: ' + str(fixedPacket) +
    '\nNienaprawione: ' + str(fixedNotGood) +
    '\nNiewykryte: ' + str(undetected))