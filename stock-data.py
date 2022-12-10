import sqlite3
import json
import os
import requests

API_KEY = 'fe1a33480750cf3d3a7b0639ba0ef7d0'
BASE_URL = 'https://api.marketstack.com/v1/'
'''
TRADING_DAYS = {
    1993: 253,
    1994: 252,
    1995: 252,
    1996: 254,
    1997: 251,
    1998: 252,
    1999: 252,
    2000: 252,
    2001: 248,
    2002: 252,
    2003: 252,
    2004: 252,
    2005: 252,
    2006: 251,
    2007: 251,
    2008: 253,
    2009: 252,
    2010: 252,
    2011: 252,
    2012: 250,
    2013: 252,
    2014: 252,
    2015: 252,
    2016: 252,
    2017: 251,
    2018: 251,
    2019: 252,
    2020: 253,
    2021: 252
}
'''

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
    return response

def clear_table(data_base, table_name):
    conn = sqlite3.connect(data_base)
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {table_name}')
    conn.commit()

def drop_table(data_base, table_name):
    conn = sqlite3.connect(data_base)
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS {table_name}')
    conn.commit()

def enter_into_database(data, table_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "stock_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, date TEXT, close REAL)')
    # cur.execute(f'DELETE FROM {table_name}')
    for day in data['data']['eod']:
        cur.execute(f'INSERT INTO {table_name} (date, close) VALUES (?, ?)', (day['date'][:10], day['close']))
    conn.commit()

def get_yearly_data(symbol, year):
    for i in range(0, 251, 25):
        data = get_stock_data(symbol, year, offset=i)
        enter_into_database(data, symbol)

if __name__ == "__main__":
    clear_table('stock_data.db', 'DJI')
    get_yearly_data('DJI', '2021')

