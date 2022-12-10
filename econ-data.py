import sqlite3
import json
import os
import requests

API_KEY = '56f93e3b07e00d30dbd54f68f2830983'

# codes: unemployment rate = UNRATE, consumer sentiment = UMCSENT, Federal Funds Rate = DFF
def get_econ_data(code, start, end, limit):
    params = {'limit': limit, 'observation_start': start, 'observation_end': end}
    try:
        result = requests.get(f'https://api.stlouisfed.org/fred/series/observations?series_id={code}&api_key={API_KEY}&file_type=json', params)
    except:
        print('Error during API request')
        return
    response = result.json()
    if 'error_code' in response:
        print('Error during API request')
        return
    return response

def enter_econ_data_into_database(data, table_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, date TEXT, value REAL)')
    for observation in data['observations']:
        cur.execute(f'INSERT INTO {table_name} (date, value) VALUES (?, ?)', (observation['date'], observation['value']))
    conn.commit()

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

def get_all_data(code, start_year, end_year):
    for y in range(start_year, end_year+1, 4):
        data = get_econ_data(code, f'{y}-01-01', f'{y}-12-31', limit=12)
        enter_econ_data_into_database(data,f'{code}_econ')

if __name__ == "__main__":

    clear_table('all_data.db', 'UNRATE')
    get_all_data('UNRATE', 1949, 2021)

    clear_table('all_data.db', 'UMCSENT')
    get_all_data('UMCSENT', 1949, 2021)

    clear_table('all_data.db', 'DFF')
    get_all_data('DFF', 1949, 2021)