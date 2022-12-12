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
    if (code == 'EXPGS' or code == 'FGEXPND'):
        l = 4
        for y in range(start_year, end_year+1, 4):
            data = get_econ_data(code, f'{str(y-1)}-01-01', f'{str(y-1)}-12-31', limit=l)
            enter_econ_data_into_database(data,f'{code}_econ')
            data = get_econ_data(code, f'{str(y)}-01-01', f'{str(y)}-12-31', limit=l)
            enter_econ_data_into_database(data,f'{code}_econ')
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
    
    if (code == 'EXPGS' or code == 'FGEXPND'):
        quarterly_table_name = f'{code}_econ'
        fetch = cur.execute(f'SELECT date, value FROM {quarterly_table_name}')
        quarterly_data_list = fetch.fetchall()
        cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, year INTEGER, previous_year_total REAL, current_year_total REAL)')
        cur.execute(f'DELETE FROM {table_name}')
        prev_i = 0
        current_i = 4
        for y in range(start_year, end_year+1, 4):
            prev = 0
            for j in range(prev_i, current_i):
                prev += float(quarterly_data_list[j][1])
            current = 0
            for j in range(current_i, current_i+4):
                current += float(quarterly_data_list[j][1])
            cur.execute(f'INSERT INTO {table_name} (year, previous_year_total, current_year_total) VALUES (?,?,?)', 
                            (y, prev, current))
            prev_i += 4
            current_i += 4

    else:
        monthly_table_name = f'{code}_econ'
        fetch = cur.execute(f'SELECT date, value FROM {monthly_table_name}')
        monthly_data_list = fetch.fetchall()
        cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, year INTEGER, start REAL, end REAL)')
        cur.execute(f'DELETE FROM {table_name}')
        start_i = 0
        end_i = 11
        for y in range(start_year, end_year+1, 4):
            start = float(monthly_data_list[start_i][1])
            end = float(monthly_data_list[end_i][1])
            # percent_change = 100 * (end - start) / start
            cur.execute(f'INSERT INTO {table_name} (year, start, end) VALUES (?,?,?)', 
                            (y, start, end))
            start_i += 12
            end_i += 12
    conn.commit()

def econ_data_main(get_individual=True, drop_composite=False):
    if get_individual:
        get_monthly_data('UNRATE', 1949, 2021)
        get_monthly_data('UMCSENT', 1981, 2021)
        get_monthly_data('EXPGS', 1949, 2021)
        get_monthly_data('FGEXPND', 1949, 2021)

    if drop_composite:
        drop_table('all_data.db', 'UNRATE_composite_econ')
        drop_table('all_data.db', 'UMCSENT_composite_econ')
        drop_table('all_data.db', 'EXPGS_composite_econ')
        drop_table('all_data.db', 'FGEXPND_composite_econ')
    get_post_election_data('UNRATE', 1949, 2021)
    get_post_election_data('UMCSENT', 1981, 2021)
    get_post_election_data('EXPGS', 1949, 2021)
    get_post_election_data('FGEXPND', 1949, 2021)

# if __name__ == "__main__":
#     econ_data_main(get_individual=True, drop_composite=True)