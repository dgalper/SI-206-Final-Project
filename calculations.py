import sqlite3
import json
import os
import csv
import numpy as np

#stock data calculations
def average_returns(symbol):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    fhand = open('calculations.text', 'a')

    table_name = f'{symbol}_composite_stock'
    fetch = cur.execute(f'SELECT year, start, end FROM {table_name}')
    data = fetch.fetchall()
    full_name = ''
    if (symbol == 'DJI'):
        full_name = 'Dow Jones Industrial Average'
    elif (symbol == 'IXIC'):
        full_name = 'Nasdaq Composite'
    fhand.write(f'Returns for {symbol} ({full_name}) in the year after Presidential Elections\n')
    fhand.write('---------------------------------------------------------------------------------------\n')
    
    total = 0
    for i in range(len(data)):
        returns = round(100 * (data[i][2] - data[i][1]) / data[i][1], 2)
        total += returns
        year = data[i][0]
        fhand.write(f'{year}: {returns}%\n')
    fhand.write(f'Average: {round(total/len(data), 2)}%\n\n')
    fhand.close()

def stock_volatility(symbol):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    full_name = ''
    if (symbol == 'DJI'):
        full_name = 'Dow Jones Industrial Average'
    elif (symbol == 'IXIC'):
        full_name = 'Nasdaq Composite'
    fhand = open('calculations.text', 'a')
    fhand.write(f'Standard deviation of daily close prices for {symbol} ({full_name}) in the year after Presidential Elections\n')
    fhand.write('------------------------------------------------------------------------------------------------------------------------\n')

    for year in range(1993, 2022, 4):
        table_name = f'{symbol}_{year}_stock'
        
        fetch = cur.execute(f'SELECT date, close FROM {table_name}')
        data = fetch.fetchall()
        close_prices = [x[1] for x in data]
        std = round(np.std(close_prices), 2)
        fhand.write(f'{year}: {std}\n')
    fhand.write('\n')
    fhand.close()

def stock_data_calculations():
    average_returns('DJI')
    stock_volatility('DJI')
    average_returns('IXIC')
    stock_volatility('IXIC')

#econ data calculations
def average_change(code):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    fhand = open('calculations.text', 'a')

    table_name = f'{code}_composite_econ'
    fetch = cur.execute(f'SELECT year, start, end FROM {table_name}')
    data = fetch.fetchall()
    full_name = ''
    if (code == 'UNRATE'):
        full_name = 'Unemployment Rate'
    elif (code == 'UMCSENT'):
        full_name = 'Consumer Sentiment'
    elif (code == 'EXPGS'):
        full_name = 'Exports of Goods and Services'
    elif (code == 'FGEXPND'):
        full_name = 'Federal Government Expenditures'
    fhand.write(f'Change in {full_name} in the year after Presidential Elections\n')
    fhand.write('--------------------------------------------------------------------\n')

    total = 0
    for i in range(len(data)):
        if (code == 'EXPGS' or code == 'FGEXPND'):
            change = round(100 * (data[i][2] - data[i][1]) / data[i][1], 2)
        else:
            change = round(data[i][2] - data[i][1], 2)
        total += change
        year = data[i][0]
        fhand.write(f'{year}: {change}')
        if (code == 'UNRATE' or code=='EXPGS' or code == 'FGEXPND'):
            fhand.write('%')
        fhand.write('\n')
    fhand.write(f'Average: {round(total/len(data), 2)}')
    if (code == 'UNRATE' or code == 'EXPGS' or code == 'FGEXPND'):
        fhand.write('%')
    fhand.write('\n\n')
    fhand.close()

def econ_data_calculations():
    average_change('UNRATE')
    average_change('UMCSENT')
    average_change('EXPGS')
    average_change('FGEXPND')

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
    fhand = open('calculations.text', 'w')
    fhand.write('ELECTIONS CALCULATIONS\n')
    fhand.write('**********************\n\n')
    fhand.close()
    elections_calculations()

    fhand = open('calculations.text', 'a')
    fhand.write('\nSTOCK DATA CALCULATIONS\n')
    fhand.write('***********************\n\n')
    fhand.close()
    stock_data_calculations()

    fhand = open('calculations.text', 'a')
    fhand.write('\nECONOMIC DATA CALCULATIONS\n')
    fhand.write('**************************\n\n')
    fhand.close()
    econ_data_calculations()

if __name__ == "__main__":
    run_calculations()