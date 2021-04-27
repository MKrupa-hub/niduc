from Generator import Generator
from Decoder import Decoder
import functools
import random

gene = Generator()
deco = Decoder()

multi = 3 # ile bitow powtarzany
length = 11 # dlugosc pakietu
test = 10 # do testu przesylu. Ile pakietow wysylamy

good = 0
fixedPacket = 0
fixedNotGood = 0
undetected = 0
# 11001011011
package = ['1','1','0','0','1','0','1','1','0','1','1']
package2 = ['1','0','0','0','1','0','1','0','0','1','1','1','0','1','1','0']

# pac = gene.packing(3)
#
coded = gene.code_hamming(package)
# print("hamming: ", coded)

decoded = deco.decode_hamming(coded)


# Kanal transmisyjny BSC
# mamy zakodowany pakiet, przysylamy go przez kanal
# jest prawdopodobienstwo ze zamienimy bit w pakiecie na przeciwny
for j in range(test):
    packet = gene.packing(length)
    coded = gene.code_hamming(packet)
    for i in range(len(coded)):
        if random.random() < 0.1:
            if coded[i] == '0':
                coded[i] = '1'
            else:
                coded[i] = '0'
    decoded, fixed = deco.decode_hamming(coded)
    # Petla poniezej zamienia pakiet ze stringow na int
    # potrzeba do hamminga
    for i in range(len(packet)):
        if packet[i] == '1':
            packet[i] = 1
        elif packet[i] == '0':
            packet[i] = 0
    # Musimy teraz ocenic ile pakietow zostalo przeslanych bez bledow, ile mialo bledy i czy udalo sie je naprawic. ORAZ ile niewykrytych bledow wystapilo
    if fixed:
        # Wystapila naprawa przy dekoderze. Sprawdzam czy naprawil poprawnie. Robie to przez pSorowanie listy przed i po wysyle
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

print('Bez bledow: ' + str(good) +
      '\nNaprawione: ' + str(fixedPacket) +
      '\nNienaprawione: ' + str(fixedNotGood) +
      '\nNiewykryte: ' + str(undetected))