import matplotlib.pyplot as plt
import math
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

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

    hist_bins = math.ceil(math.sqrt(sample))
    plt.hist(goodHis, bins = hist_bins)
    plt.xlabel('Liczba pakietów')
    plt.ylabel('Liczba wystąpień')
    plt.savefig('his.jpg')
    plt.show()
    
    img = Image('his.jpg')
    img.height = 390
    img.width = 450
    calc.add_image(img, 'H1')
    wb.save(sheetNames[0])
    
    plt.boxplot(goodHis,vert=False)
    plt.xlabel('Liczba pakietów')
    plt.savefig('box.jpg')
    plt.show()
    
    img2 = Image('box.jpg')
    img2.height = 390
    img2.width = 450
    calc.add_image(img2, 'P1')
    wb.save(sheetNames[0])

    wb.save(dest_fileName)
