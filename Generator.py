import random

class Generator:
    def __init__(self):
        pass

    def packing(self, length):
        package = []
        for i in range(length):
            package.append(str(random.randint(0,1)))
        return package

    def multiple_bit(self, multiple, package):
        temp = []
        for j in range(len(package)):
            if package[j] == '0':
                [temp.append('0') for i in range(multiple)]
            else:
                [temp.append('1') for i in range(multiple)]
        return temp