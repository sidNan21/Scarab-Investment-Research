import iexfinance.stocks as iexfinance
import csv

companies = []
with open('sp.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if(row[0] != 'Symbol'):
            companies.append(row[0])

with open('nasdaq.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if(row not in companies):
            if(row[0] != 'Symbol'):
                companies.append(row[0])
file = open('companies.txt', 'w')
for company in companies:
    file.write(company+"\n")
