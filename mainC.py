import Generator as gene
import Decoder as deco
import functools
import random

multi = 3 # ile bitow powtarzany
lengthHamm = 11 # dlugosc pakietu
test = 10 # do testu przesylu. Ile pakietow wysylamy

good = 0
fixedPacket = 0
fixedNotGood = 0
undetected = 0
# 11001011011
# pakiety do testow czy dobrze koduje
package = [1,1,0,0,1,0,1,1,0,1,1]
package2 = [1,0,0,0,1,0,1,0,0,1,1,1,0,1,1,0]

# Kanal transmisyjny BSC
# mamy zakodowany pakiet, przysylamy go przez kanal
# jest prawdopodobienstwo ze zamienimy bit w pakiecie na przeciwny
for j in range(test):
    packet = gene.packing(lengthHamm)
    coded = gene.code_hamming(packet)
    for i in range(len(coded)):
        if random.random() < 0.05:
            coded[i] = int(not coded[i])
    decoded, fixed = deco.decode_hamming(coded)
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

# narazie output w konsoli. Potem do pliku CSV sie wpisze
print('Bez bledow: ' + str(good) +
      '\nNaprawione: ' + str(fixedPacket) +
      '\nNienaprawione: ' + str(fixedNotGood) +
      '\nNiewykryte: ' + str(undetected))