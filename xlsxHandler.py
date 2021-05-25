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

    plt.boxplot(goodHis,vert=False)
    plt.xlabel('Liczba pakietów')
    plt.savefig('box.jpg')
    plt.show()
    img2 = Image('box.jpg')
    img2.height = 390
    img2.width = 450
    calc.add_image(img2, 'P1')

    goodHis2 = []
    [goodHis2.append(result[x][1]) for x in range(sample)]

    plt.hist(goodHis2, bins=hist_bins)
    plt.xlabel('Liczba pakietów')
    plt.ylabel('Liczba wystąpień')
    plt.savefig('his2.jpg')
    plt.show()
    img3 = Image('his2.jpg')
    img3.height = 390
    img3.width = 450
    calc.add_image(img3, 'H23')

    plt.boxplot(goodHis2, vert=False)
    plt.xlabel('Liczba pakietów')
    plt.savefig('box2.jpg')
    plt.show()
    img4 = Image('box2.jpg')
    img4.height = 390
    img4.width = 450
    calc.add_image(img4, 'P23')

    goodHis3 = []
    [goodHis3.append(result[x][2]) for x in range(sample)]

    plt.hist(goodHis3, bins=hist_bins)
    plt.xlabel('Liczba pakietów')
    plt.ylabel('Liczba wystąpień')
    plt.savefig('his3.jpg')
    plt.show()
    img5 = Image('his3.jpg')
    img5.height = 390
    img5.width = 450
    calc.add_image(img5, 'H45')

    plt.boxplot(goodHis3, vert=False)
    plt.xlabel('Liczba pakietów')
    plt.savefig('box3.jpg')
    plt.show()
    img6 = Image('box3.jpg')
    img6.height = 390
    img6.width = 450
    calc.add_image(img6, 'P45')

    goodHis4 = []
    [goodHis4.append(result[x][3]) for x in range(sample)]

    plt.hist(goodHis4, bins=hist_bins)
    plt.xlabel('Liczba pakietów')
    plt.ylabel('Liczba wystąpień')
    plt.savefig('his4.jpg')
    plt.show()
    img7 = Image('his4.jpg')
    img7.height = 390
    img7.width = 450
    calc.add_image(img7, 'H67')

    plt.boxplot(goodHis4, vert=False)
    plt.xlabel('Liczba pakietów')
    plt.savefig('box4.jpg')
    plt.show()
    img8 = Image('box4.jpg')
    img8.height = 390
    img8.width = 450
    calc.add_image(img8, 'P67')

    wb.save(dest_fileName)
