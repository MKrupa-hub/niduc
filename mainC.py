import Generator as gene
import Decoder as deco
import functools
import random

multi = 5 # ile bitow powtarzany
length = 11 # dlugosc pakietu
test = 10000 # do testu przesylu. Ile pakietow wysylamy
probability = 0.05

good = 0
fixedPacket = 0
fixedNotGood = 0
undetected = 0

# pac = gene.packing(13)
# coded = gene.code_crc(pac)
# coded[2] = int(not coded[2])
# decodero, fix = deco.decodeCrc(coded, False)
#
# print("CRC OR : ", pac)
# print("CRC CO : ", coded)
# print("CRC DE : ", decodero, fix)

# Kanal transmisyjny BSC
# mamy zakodowany pakiet, przysylamy go przez kanal
# jest prawdopodobienstwo ze zamienimy bit w pakiecie na przeciwny
for j in range(test):
    packet = gene.packing(length)
    #coded = gene.code_crc(packet)
    coded = gene.code_hamming(packet)
    #coded = gene.multiple_bit(multi, packet)
    for i in range(len(coded)):
        if random.random() < probability:
            coded[i] = int(not coded[i])
    decoded, fixed = deco.decode_hamming(coded)
    #decoded, fixed = deco.decodeMulti(coded, multi)
    #decoded, fixed = deco.decodeCrc(coded, False)
    # Musimy teraz ocenic ile pakietow zostalo przeslanych bez bledow, ile mialo bledy i czy udalo sie je naprawic. ORAZ ile niewykrytych bledow wystapilo
    if fixed:
        # Wystapila naprawa przy dekoderze. Sprawdzam czy naprawil poprawnie. Robie to przez porownanie listy przed i po wysyle
        if packet == decoded:
            fixedPacket += 1
        else:
            fixedNotGood += 1
    else:
        # Nie wystapila naprawa ale moze wystapil niewykryty blada
        if packet == decoded:
            good += 1
        else:
            undetected += 1

#narazie output w konsoli. Potem do pliku CSV sie wpisze
print('Bez bledow: ' + str(good) +
      '\nNaprawione: ' + str(fixedPacket) +
      '\nNienaprawione: ' + str(fixedNotGood) +
      '\nNiewykryte: ' + str(undetected))