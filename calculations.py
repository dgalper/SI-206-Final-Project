import sqlite3
import json
import os
import csv

#stock data calculations
def average_returns(symbol):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    fhand = open('calculations.text', 'w')

    table_name = f'{symbol}_composite_stock'
    fetch = cur.execute(f'SELECT year, start, end FROM {table_name}')
    data = fetch.fetchall()
    fhand.write(f'Returns for {symbol} in the year after Presidential Elections\n')
    fhand.write('--------------------------------------------------------\n')
    total = 0
    for i in range(len(data)):
        returns = round(100 * (data[i][2] - data[i][1]) / data[i][1], 2)
        total += returns
        year = data[i][0]
        fhand.write(f'{year}: {returns}%\n')
    fhand.write(f'Average: {total/len(data)}%\n\n')
    fhand.close()

def stock_data_calculations():
    average_returns('DJI')

#Elections results calculations
def elections_calculations():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    fetch = cur.execute(f'SELECT * FROM Election WHERE winning_party = "Republican"')
    data = fetch.fetchall()
    republican_winners = len(data)

    fetch = cur.execute(f'SELECT * FROM Election WHERE winning_party = "Democratic"')
    data = fetch.fetchall()
    democrat_winners = len(data)

    fhand = open('calculations.text', 'a')
    fhand.write('Past 30 Presidential Election Results\n')
    fhand.write('-------------------------------------\n')
    fhand.write(f'Republican Winners: {republican_winners}\n')
    fhand.write(f'Democrat Winners: {democrat_winners}\n\n')
    fhand.close()

def run_calculations():
    stock_data_calculations()
    elections_calculations()

if __name__ == "__main__":
    run_calculations()