import sqlite3
import json
import os
import requests

API_KEY = '56f93e3b07e00d30dbd54f68f2830983'

# codes: unemployment rate = UNRATE, consumer sentiment = UMCSENT
def get_econ_data(code, start, end):
    params = {'limit': 25, 'observation_start': start, 'observation_end': end}
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

if __name__ == "__main__":
    print(get_econ_data('UMCSENT', '2020-03-01', '2022-02-28'))