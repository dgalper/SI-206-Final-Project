import sqlite3
import json
import os
import requests

API_KEY = 'fe1a33480750cf3d3a7b0639ba0ef7d0'
BASE_URL = 'https://api.marketstack.com/v1/'

# makes an api call to get stock data –– 25 days at a time
def get_stock_data(symbol, year, offset):
    params = {'access_key': API_KEY, 'limit': 25, 'offset': offset, 'sort': 'ASC', 
                'date_from': f'{year}-01-01', 'date_to': f'{year}-12-31'}
    try:
        result = requests.get(f'https://api.marketstack.com/v1/tickers/{symbol}.INDX/eod', params)
    except:
        print('Error during the API request')
        return
    response = result.json()
    if 'error' in response:
        print('Error during the API request')
        return
    # print(response)
    return response

def clear_table(data_base, table_name):
    conn = sqlite3.connect(data_base)
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {table_name}')
    cur.close()
    conn.commit()

def drop_table(data_base, table_name):
    conn = sqlite3.connect(data_base)
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS {table_name}')
    cur.close()
    conn.commit()

#enters the data returned by get_stock_data() into a table in the database
def enter_stock_data_into_database(data, table_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, date TEXT, open REAL, close REAL)')
    # cur.execute(f'DELETE FROM {table_name}')
    for day in data['data']['eod']:
        cur.execute(f'INSERT INTO {table_name} (date, open, close) VALUES (?, ?, ?)', (day['date'][:10], day['open'], day['close']))
    cur.close()
    conn.commit()

#uses the get_stock_data() and enter_into_database() functions to enter all data for given year in a table
def get_yearly_data(symbol, year):
    table_name = f'{symbol}_{year}_stock'
    # drop_table('all_data.db', table_name)
    full_year_data = []
    for i in range(0, 251, 25):
        data = get_stock_data(symbol, year, offset=i)
        full_year_data.extend(data['data']['eod'])
        # enter_stock_data_into_database(data, table_name)
    # print(full_year_data)
    return full_year_data

#creates a table recording start and end prices for each year after an election from 1993 to 2021
def get_all_data(symbol, year_start, year_end):
    table_name = f'{symbol}_composite_stock'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, year TEXT, start REAL, end REAL, percent_change REAL)')
    cur.execute(f'DELETE FROM {table_name}')
    for year in range(year_start, year_end+1, 4):
        year_data_list = get_yearly_data(symbol, year)
        percent_change = 100 * (year_data_list[-1]['close'] - year_data_list[0]['open']) / year_data_list[0]['open']
        cur.execute(f'INSERT INTO {table_name} (year, start, end, percent_change) VALUES (?, ?, ?, ?)', 
                    (str(year), year_data_list[0]['open'], year_data_list[-1]['close'], percent_change))
    cur.close()
    conn.commit()

if __name__ == "__main__":
    # get_yearly_data('DJI', '2021')
    # clear_table('all_data.db', 'DJI_composite_stock')
    # drop_table('all_data.db', 'DJI_composite_stock')
    get_all_data('DJI', 1993, 2021)


