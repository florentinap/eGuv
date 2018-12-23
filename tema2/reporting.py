import MySQLdb
import MySQLdb.cursors
import numpy as np
import matplotlib.pyplot as plt
import time
from fpdf import FPDF

def getDataFromDB(elem):
    try:
        db = MySQLdb.connect(host = 'localhost', user = 'root', passwd = 'flory95', db = 'egov')
        cursor = db.cursor()
    except Exception as e:
        print(str(e))

    query = 'SELECT ' + elem + ' from smartform'
    result = []

    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        print(str(e))

    try:
        db.close();
    except Exception as e:
        print(str(e))
    
    return result

def payEveryMonth():
    
    result = getDataFromDB('paymonth')
    months = {'Ianuarie': 0, 'Februarie': 0, 'Martie': 0, 'Aprilie': 0, 'Mai': 0, 'Iunie': 0, 'Iulie': 0, 'August': 0, 'Septembrie': 0, 'Octombrie': 0, 'Noiembrie': 0, 'Decembrie': 0}
    
    for r in result:
        if r[0] in months.keys():
            months[r[0]] += 1

    x = np.array(list(months.values()))
    y = np.array(list(months.keys()))
    xticks = list(months.keys())
    
    fig = plt.figure()
    plt.bar(y, x)
    plt.xticks(y, xticks)
    fig.savefig('payEveryMonth.jpg')

def payEveryCamin():
    result = getDataFromDB('camin')
    total = 20
    camin = {'P01': 0, 'P02': 0, 'P03': 0, 'P04': 0, 'P05': 0, 'P06': 0, 'P07': 0, 'P08': 0, 'P09': 0, 'P10': 0}
    rest = {'P01': total, 'P02': total, 'P03': total, 'P04': total, 'P05': total, 'P06': total, 'P07': total, 'P08': total, 'P09': total, 'P10': total}
    totalPlatit = 0
    totalRest = len(rest) * total
    for r in result:
        if r[0] in camin.keys():
            camin[r[0]] += 1
            totalPlatit += 1
            rest[r[0]] -= 1
            totalRest -= 1

    x = np.array(list(camin.values()))
    y = np.array(list(camin.keys()))
    x1 = np.array(list(rest.values()))
    xticks = list(camin.keys())
    
    fig = plt.figure()
    p1 = plt.bar(y, x)
    #p2 = plt.bar(y, x1, bottom = x)
    plt.xticks(y, xticks)
    #plt.legend((p1[0], p2[0]), ('Au platit', 'Rest de plata'))
    fig.savefig('payEveryCamin.jpg')

    labels = ['Au platit', 'Rest de plata']
    sizes = [totalPlatit, totalRest]
    explode = [0, 0]
    fi1, ax1 = plt.subplots()
    ax1.pie(sizes, explode, labels=labels)
    ax1.axis('equal')
    fi1.savefig('restDePlata.jpg')

def sumPerMonth():
    result = getDataFromDB('paymonth, paysum, payextra')
    months = {'Ianuarie': [0, 0, 0], 'Februarie': [0, 0, 0], 'Martie': 0, 'Aprilie': 0, 'Mai': [0, 0, 0], 'Iunie': [0, 0, 0], 'Iulie': [0, 0, 0], 'August': [0, 0, 0], 'Septembrie': [0, 0, 0], 'Octombrie': [0, 0, 0], 'Noiembrie': [0, 0, 0], 'Decembrie': [0, 0, 0]}
    
    for r in result:
        if r[0] in months.keys():
            months[r[0]][0] += 1
            months[r[0]][1] += int(r[1])
            months[r[0]][2] += int(r[2])
    return months

def reporting():
    pdf = FPDF()
    pdf.set_font('arial', size=30)
    pdf.add_page()
    pdf.text(50, 10, 'Document de raportare')
    pdf.set_font('arial', size=12)
    pdf.cell(50, 5, 'Luna', 1, 0, 'L', 0)
    pdf.cell(50, 5, 'Numar plati', 1, 0, 'L', 0)
    pdf.cell(50, 5, 'Suma totala', 1, 0, 'L', 0)
    pdf.cell(50, 5, 'Suma penalizari', 1, 0, 'L', 0)
    pdf.ln()
    
    months = sumPerMonth()    
    for month, val in months.items():
        pdf.cell(50, 5, month, 1, 0, 'L', 0)
        if isinstance(val, list):
            pdf.cell(50, 5, str(val[0]), 1, 0, 'L', 0)
            pdf.cell(50, 5, str(val[1]), 1, 0, 'L', 0)
            pdf.cell(50, 5, str(val[2]), 1, 0, 'L', 0)
        else:
            pdf.cell(50, 5, str(0), 1, 0, 'L', 0)
            pdf.cell(50, 5, str(0), 1, 0, 'L', 0)
            pdf.cell(50, 5, str(0), 1, 0, 'L', 0)
        pdf.ln()
    
    pdf.text(10, 100, 'Numar plati in fiecare luna') 
    pdf.image('payEveryMonth.jpg', 0, 100, 150, 150)
    pdf.add_page()
    pdf.text(10, 20, 'Numar plati per camin')
    pdf.image('payEveryCamin.jpg', 0, 25, 150, 150)
    pdf.image('restDePlata.jpg', 0, 175, 200, 150)
    pdf.output("reporting.pdf", "F")

def main():
    payEveryMonth()
    payEveryCamin()
    
    reporting()

main()
