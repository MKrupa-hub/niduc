import Generator as gene
import Decoder as deco
import csv
import random

def write_result(fileName, type):
    with open(fileName, 'w', newline='') as file:
        fieldnames = [columnname[0], columnname[1], columnname[2], columnname[3]]
        write = csv.DictWriter(file, fieldnames=fieldnames)
        write.writeheader()
        for k in range(sample):
            result = [0, 0, 0, 0]
            for j in range(test):
                packet = gene.packing(length)
                if type == 0:
                    coded = gene.code_hamming(packet)
                if type == 1:
                    coded = gene.multiple_bit(multi, packet)
                if type == 2:
                    coded = gene.code_crc(packet)
                for i in range(len(coded)):
                    if random.random() < probability:
                        coded[i] = int(not coded[i])
                if type == 0:
                    decoded, fixed = deco.decode_hamming(coded)
                if type == 1:
                    decoded, fixed = deco.decodeMulti(coded, multi)
                if type == 2:
                    decoded, fixed = deco.decodeCrc(coded)
                # Musimy teraz ocenic ile pakietow zostalo przeslanych bez bledow, ile mialo bledy i czy udalo sie je naprawic. ORAZ ile niewykrytych bledow wystapilo
                if fixed:
                    # Wystapila naprawa przy dekoderze. Sprawdzam czy naprawil poprawnie. Robie to przez porownanie listy przed i po wysyle
                    if packet == decoded:
                        result[0] = result[0] + 1
                    else:
                        result[1] = result[1] + 1
                else:
                    # Nie wystapila naprawa ale moze wystapil niewykryty blada
                    if packet == decoded:
                        result[2] = result[2] + 1
                    else:
                        result[3] = result[3] + 1
            write.writerow({columnname[0]: result[2], columnname[1]: result[0], columnname[2]: result[1], columnname[3]: result[3]})

columnname = ['Good', 'Fixed', 'Fixed not', 'Undetected']
fileNames = ['_hamming.csv', '_multi.csv', '_crc.csv']
multi = 5 # ile bitow powtarzany
length = 11 # dlugosc pakietu
sample = 10 # ile wysylow wykonuje
test = 100 # Ile pakietow wysylamy
probability = 0.05 # prawdopodobienstwo przeklamania bitu

# Kanal transmisyjny BSC
# mamy zakodowany pakiet, przysylamy go przez kanal
# jest prawdopodobienstwo ze zamienimy bit w pakiecie na przeciwny
write_result(fileNames[0], 0)
write_result(fileNames[1], 1)
write_result(fileNames[2], 2)
