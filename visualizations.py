import sqlite3
import json
import os
import numpy as np
import matplotlib.pyplot as plt

import stock_data
import econ_data
import election_data

# stock data visualizations
def stock_data_graphs(symbol):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    table_name = f'{symbol}_composite_stock'
    fetch = cur.execute(f'SELECT {table_name}.year, {table_name}.start, {table_name}.end, Election.winning_party FROM {table_name} INNER JOIN Election ON {table_name}.year = Election.election_year+1')
    data = fetch.fetchall()

    full_name = ''
    if symbol == 'DJI':
        full_name = 'Dow Jones Industrial Average'
    elif symbol == 'IXIC':
        full_name = 'Nasdaq Composite'

    d_x_axis = [x[0] for x in data if x[3] == 'Democratic']
    r_x_axis = [x[0] for x in data if x[3] == 'Republican']
    d_y_axis = [round(100*(x[2]-x[1])/x[1], 2) for x in data if x[3] == 'Democratic']
    r_y_axis = [round(100*(x[2]-x[1])/x[1], 2) for x in data if x[3] == 'Republican']
    
    xticks = [x[0] for x in data]
    fig = plt.figure(figsize=(10,7))
    plt.grid()
    plt.bar(d_x_axis, d_y_axis, color='blue', label=[x[0] for x in data])
    plt.bar(r_x_axis, r_y_axis, color='red', label=[x[0] for x in data])
    plt.xticks(xticks)
    plt.xlabel('First Year after a Presidential Election')
    plt.ylabel(f'Yearly Returns for {symbol} (%)')
    plt.title(f'Percent Returns for the {full_name} ({symbol}) in First Year after a Presidential Election')
    plt.legend(['Democrat', 'Republican'], loc=0)
    plt.show()

# econ data visualizations
def econ_data_graphs(code):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    full_name = ''
    if code == 'UNRATE':
        full_name = 'Unemployment Rate'
    elif code == 'UMCSENT':
        full_name = 'Consumer Sentiment'
    elif code == 'EXPGS':
        full_name = 'Exports of Goods & Services'
    elif code == 'FGEXPND':
        full_name = 'Federal Government Expenditures'
    
    if code == 'UNRATE' or code == 'UMCSENT':
        table_name = f'{code}_composite_econ'
        fetch = cur.execute(f'SELECT {table_name}.year, {table_name}.start, {table_name}.end, Election.winning_party FROM {table_name} INNER JOIN Election ON {table_name}.year = Election.election_year+1')
        data = fetch.fetchall()
        d_y_axis = [round(x[2]-x[1], 2) for x in data if x[3] == 'Democratic']
        r_y_axis = [round(x[2]-x[1], 2) for x in data if x[3] == 'Republican']
    else:
        table_name = f'{code}_composite_econ'
        fetch = cur.execute(f'SELECT {table_name}.year, {table_name}.previous_year_total, {table_name}.current_year_total, Election.winning_party FROM {table_name} INNER JOIN Election ON {table_name}.year = Election.election_year+1')
        data = fetch.fetchall()
        d_y_axis = [round(100*(x[2]-x[1])/x[1], 2) for x in data if x[3] == 'Democratic']
        r_y_axis = [round(100*(x[2]-x[1])/x[1], 2) for x in data if x[3] == 'Republican']
    d_x_axis = [x[0] for x in data if x[3] == 'Democratic']
    r_x_axis = [x[0] for x in data if x[3] == 'Republican']

    xticks = [x[0] for x in data]
    fig = plt.figure(figsize=(10,7))
    plt.grid()
    plt.bar(d_x_axis, d_y_axis, color='blue', label=[x[0] for x in data])
    plt.bar(r_x_axis, r_y_axis, color='red', label=[x[0] for x in data])
    plt.xticks(xticks)
    plt.xlabel('First Year after a Presidential Election')
    add = ' (%)'
    if code == 'UMCSENT':
        add = ''
    plt.ylabel(f'Yearly Change in {code}{add}')
    if code == 'UNRATE' or code == 'UMCSENT':
        plt.title(f'Change in {full_name} ({code}) in First Year after a Presidential Election')
    else:
        plt.title(f'Percent Change in {full_name} ({code}) in First Year after a Presidential Election')
    plt.legend(['Democrat', 'Republican'], loc=0)
    plt.show()

def vis_main():
    stock_data_graphs('DJI')
    stock_data_graphs('IXIC')
    econ_data_graphs('UNRATE')
    econ_data_graphs('UMCSENT')
    econ_data_graphs('EXPGS')
    econ_data_graphs('FGEXPND')

if __name__ == "__main__":
    vis_main()
