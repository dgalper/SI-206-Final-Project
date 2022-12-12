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
        print('Error during API request: ' + str(response['error_code']))
    # print(response)
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

def get_monthly_data(code, start_year, end_year):
    drop_table('all_data.db', f'{code}_econ')
    if (code == 'EXPGS'):
        l = 4
    else: 
        l = 12
    for y in range(start_year, end_year+1, 4):
        data = get_econ_data(code, f'{str(y)}-01-01', f'{str(y)}-12-31', limit=l)
        enter_econ_data_into_database(data,f'{code}_econ')

def get_post_election_data(code, start_year, end_year):
    table_name = f'{code}_composite_econ'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, year TEXT, start REAL, end REAL)')
    cur.execute(f'DELETE FROM {table_name}')

    monthly_table_name = f'{code}_econ'
    fetch = cur.execute(f'SELECT date, value FROM {monthly_table_name}')
    year_data_list = fetch.fetchall()

    start_i = 0
    if (code == 'EXPGS'):
        end_i = 3
    else:
        end_i = 11
    for y in range(start_year, end_year+1, 4):
        start = float(year_data_list[start_i][1])
        end = float(year_data_list[end_i][1])
        # percent_change = 100 * (end - start) / start
        cur.execute(f'INSERT INTO {table_name} (year, start, end) VALUES (?,?,?)', 
                        (str(y), start, end))
        if (code == 'EXPGS'):
            start_i += 4
            end_i += 4
        else:
            start_i += 12
            end_i += 12
    conn.commit()

def econ_data_main(get_individual=True, drop_composite=False):
    if get_individual:
        get_monthly_data('UNRATE', 1949, 2021)
        get_monthly_data('UMCSENT', 1981, 2021)
        get_monthly_data('EXPGS', 1957, 2021)

    if drop_composite:
        drop_table('all_data.db', 'UNRATE_composite_econ')
        drop_table('all_data.db', 'UMCSENT_composite_econ')
        drop_table('all_data.db', 'DFF_composite_econ')
    get_post_election_data('UNRATE', 1949, 2021)
    get_post_election_data('UMCSENT', 1981, 2021)
    get_post_election_data('EXPGS', 1957, 2021)

if __name__ == "__main__":
    econ_data_main(get_individual=True, drop_composite=True)