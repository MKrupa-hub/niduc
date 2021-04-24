

class Decoder:
    def __init__(self):
        pass

     # dekodowanie (dla powtarzania bitu 3 razy):
     # zakładam, że najbardziej prawdopodobne jest wystąpienie pojedyńczego błędu:
     # 000 nadano 0
     # 010 odebrano 0
     # W przypadku gdy wystąpi więcej błędów to pakiet jest nienaprawialny
    def decodeMulti(self, coded, multi):
        # jezeli sa same 0 lub 1 to pakiet jest oznaczany jako poprawnie przeslany
        decoded = []
        fixed = False
        for size in range(0, len(coded), multi):
            # laduje 3 bity pakietu do testu czy sa dobrze przeslane lub wymagaja naprawy
            temp = [coded[size + i] for i in range(multi)]
            lis = ''.join(temp)
            if ('0' * multi) in lis:
                decoded.append('0')
                continue
            if ('1' * multi) in lis:
                decoded.append('1')
                continue
            # proba naprawy pakietu
            test = 0
            for x in range(len(temp)):
                if temp[x] == '0':
                    test += 1
                else:
                    test -= 1
            if test == 1:
                decoded.append('0')
                fixed = True
            elif test == -1:
                decoded.append('1')
                fixed = True
        return decoded, fixed