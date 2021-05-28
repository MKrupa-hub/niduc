import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl import load_workbook
import math
from pathlib import Path
import statistics
from scipy.stats import norm
import scipy.optimize as opt
import matplotlib.mlab as mlab
import warnings
import os
from openpyxl.drawing.image import Image

message = ['Min value', '25th percentile', '50th percentile', '75th percentile', 'Max value']

def pdf(x,a, mu, sigma):
    return a * math.e ** ((-1 / 2) * (((x - mu) / sigma) ** 2))

def handle(sheetNames, columnname, sample, result, dest_fileName):
    warnings.filterwarnings('ignore')
    wb = Workbook()
    sheet = wb.active
    sheet.title = sheetNames[0]
    sheet.cell(row=1, column=1).value = columnname[0]
    sheet.cell(row=1, column=2).value = columnname[1]
    sheet.cell(row=1, column=3).value = columnname[2]
    sheet.cell(row=1, column=4).value = columnname[3]
    for row in range(2, sample + 2):
        for column in range(1, 5):
            sheet.cell(column=column, row=row).value = result[row - 2][column - 1]
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

    for iter in range(4):
        goodHis = []
        [goodHis.append(result[x][iter]) for x in range(sample)]
        mean = statistics.mean(goodHis)
        std = statistics.stdev(goodHis)
        quantiles = statistics.quantiles(goodHis, n=6, method='inclusive')
        iqr = quantiles[3] - quantiles[1]
        box = plt.boxplot(quantiles, vert=False)
        plt.title(columnname[iter])
        plt.xlabel('Liczba pakietów przesłanych')
        plt.savefig(columnname[iter] + 'box.jpg')
        plt.close()
        img = Image(columnname[iter] + 'box.jpg')
        img.height = 390
        img.width = 450
        calc.add_image(img, ('H' + str(((iter+1) * 20))))
        # plt.show()

        counts, bins, bars = plt.hist(goodHis, bins=20)
        x = []
        for i in range(len(bins) - 1):
            x.append((bins[i] + bins[i + 1]) / 2)
        y = counts
        params, cov = opt.curve_fit(pdf, x, y, p0=[max(y), quantiles[2], iqr / 1.349])
        plt.plot(x, pdf(x, params[0], params[1], params[2]))
        plt.title(columnname[iter])
        plt.xlabel('Liczba pakietów przesłanych')
        plt.ylabel('Liczba wystąpień')
        plt.savefig(columnname[iter] + 'hist.jpg')
        plt.close()  # +
        img = Image(columnname[iter] + 'hist.jpg')
        img.height = 390
        img.width = 450
        calc.add_image(img, ('P' + str(((iter +1) * 20))))
        # plt.show()
    wb.save(dest_fileName)
