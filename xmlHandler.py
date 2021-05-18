from openpyxl import Workbook
from openpyxl import load_workbook

message = ['Min value', '25th percentile', '50th percentile', '75th percentile', 'Max value']


def calculateAverage(wb, sheetNames, columnname, sample):
    calc = wb[sheetNames[1]]
    wb.active = calc
    calc['A2'] = 'Count'
    calc['A3'] = 'Average'
    calc['A4'] = 'Standard dev.'
    calc['A6'] = 'Quartile'
    for i in range(1, len(columnname) + 1):
        calc[chr(65+ i) + '1'] = str(columnname[i -1])
        calc[chr(65 + i) + '2'] = '=SUM(' + str(sheetNames[0]) + '!' + chr(64 + i) + str(2) + ':' + chr(64 + i) + str((sample + 1)) + ')'
        calc[chr(65 + i) + '3'] = '=AVERAGE(' + str(sheetNames[0]) + '!' + chr(64 + i) + str(2) + ':' + chr(64 + i) + str((sample + 1)) + ')'
        calc[chr(65 + i) + '4'] = '=STDEV(' + str(sheetNames[0]) + '!' + chr(64 + i) + str(2) + ':' + chr(64 + i) + str((sample + 1)) + ')'
        for quartile in range(5):
            calc['A' + str((quartile + 7))] = quartile
            calc[chr(65 + i) + str((7+quartile))] = '=QUARTILE(' + str(sheetNames[0]) + '!' + chr(64 + i) + str(2) + ':' + chr(64 + i) + str((sample + 1)) + ',' + 'A' + str((7 + quartile)) +')'
            calc['F' + str((7+quartile))] = message[quartile]