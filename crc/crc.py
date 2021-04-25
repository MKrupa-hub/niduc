# Funkcja przyjmuje dane, następnie uzupełnia je zerami do odpowiedniej długości
# Następnie skanuje otrzymane dane i jeśli znajdzie 1, wykonuje operację xor na bitach między danymi, a wielomianem.
# wielomian x^3+x+1
key = ['1', '0', '1', '1']
size = len(key)
error = "Bledny przesyl"

def code_crc(package: list)-> list:
    crc = list.copy(package)
    tmp = list.copy(package)
    for i in range(size - 1):
        tmp.append('0')
    bits = len(crc)
    for i in range(bits):
        if tmp[i] == 1:
            for j in range(len(key)):
                tmp[i + j] = (int(bool(tmp[i + j])) ^ int(bool(key[j]))) # Po przeskanowaniu wszystkich danych, wynik
                # zamieniany jest z wektora na macierz. Funkcja kodująca zwraca wektor zakodowanych danych.
    for i in range(len(key) - 1):
        crc.append(tmp[bits + i])
    return crc


def decode_crc(package: list)-> list:
    tmp = list.copy(package)
    bits = len(package)
    for i in range(bits - size + 1):
        if tmp[i] == 1:
            for j in range(size):
                tmp[i + j] = (int(bool(tmp[i + j])) ^ int(bool(key[j])))
    sum0 = 0
    for i in range(size):
        sum0 = sum0 + int(tmp[bits - 1 - i])

    if sum0 == 0:
        return package[:-(size - 1)] #wyświetla bez dodanych zer #Poprawny pakiet bez zmian
    elif sum0 == 1:
        crc = package[:-(size - 1)]
        #crc.append("Fixed") #do zliczania liczby naprawionych pakietow pozniej
        return crc
    else:
        return error
        #return ["Repeat"] #do zliczania liczby powtórek przesłania pakietow pozniej