import sqlite3
import json
import os
import requests

API_KEY = 'fe1a33480750cf3d3a7b0639ba0ef7d0'
# BASE_URL = 'https://api.marketstack.com/v1/'

def get_stock_data(index, start, end):
    params = {'access_key': API_KEY, 'date_from': start, 'date_to': end}
    try:
        result = requests.get(f'https://api.marketstack.com/v1/tickers/{index}.INDX/eod', params)
    except:
        print('Error during the API request')
        return
    response = result.json()
    if 'error' in response:
        print('Error during the API request')
        return
    return response


if __name__ == "__main__":
    print(get_stock_data('DJI', '2020-03-01', '2022-03-31'))

