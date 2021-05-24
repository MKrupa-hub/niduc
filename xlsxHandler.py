import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl import load_workbook

message = ['Min value', '25th percentile', '50th percentile', '75th percentile', 'Max value']

def handle(sheetNames, columnname, sample, result, dest_fileName):
    wb = Workbook()
    sheet = wb.active
    sheet.title = sheetNames[0]
    sheet.cell(row=1, column=1).value = columnname[0]
    sheet.cell(row=1, column=2).value = columnname[1]
    sheet.cell(row=1, column=3).value = columnname[2]
    sheet.cell(row=1, column=4).value = columnname[3]
    for row in range(2, sample + 2):
        for column in range(1, 5):
            sheet.cell(column = column, row = row).value = result[row - 2][column - 1]
    wb.create_sheet(sheetNames[1], 1)
    calc = wb[sheetNames[1]]
    wb.active = calc
    calc['A2'] = 'Count'
    calc['A3'] = 'Average'
    calc['A4'] = 'Median'
    calc['A5'] = 'Standard dev.'
    calc['A7'] = 'Quartile'
    for i in range(1, len(columnname) + 1):
        calc[chr(65 + i) + '1'] = str(columnname[i -1])
        calc[chr(65 + i) + '2'] = '=SUM(' + str(sheetNames[0]) + '!' + chr(64 + i) + str(2) + ':' + chr(64 + i) + str((sample + 1)) + ')'
        calc[chr(65 + i) + '3'] = '=AVERAGE(' + str(sheetNames[0]) + '!' + chr(64 + i) + str(2) + ':' + chr(64 + i) + str((sample + 1)) + ')'
        calc[chr(65 + i) + '4'] = '=MEDIAN(' + str(sheetNames[0]) + '!' + chr(64 + i) + str(2) + ':' + chr(64 + i) + str((sample + 1)) + ')'
        calc[chr(65 + i) + '5'] = '=STDEV(' + str(sheetNames[0]) + '!' + chr(64 + i) + str(2) + ':' + chr(64 + i) + str((sample + 1)) + ')'
        for quartile in range(5):
            calc['A' + str((quartile + 8))] = quartile
            calc[chr(65 + i) + str((8+quartile))] = '=QUARTILE(' + str(sheetNames[0]) + '!' + chr(64 + i) + str(2) + ':' + chr(64 + i) + str((sample + 1)) + ',' + 'A' + str((8 + quartile)) +')'
            calc['F' + str((8+quartile))] = message[quartile]
    # histogram
    goodHis = []
    [goodHis.append(result[x][0]) for x in range(sample)]

    plt.hist(goodHis, bins=10)
    plt.show()

    wb.save(dest_fileName)