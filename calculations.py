import sqlite3
import json
import os

def average_returns(symbol):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()

    table_name = f'{symbol}_composite_stock'
    # cur.execute(f'ALTER TABLE {table_name} ADD (change REAL, percent_change REAL)')
    data = cur.execute(f'SELECT * FROM {table_name}')
    print(data.fetchall())

def stock_data_calculations():
    average_returns('DJI')

if __name__ == "__main__":
    stock_data_calculations()