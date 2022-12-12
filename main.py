import sqlite3
import json
import os
import requests
import re
from bs4 import BeautifulSoup
import numpy as np

import stock_data
import econ_data
import election_data
import calculations as calc

def clear_database():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_name = dir_path + '/' + "all_data.db"

    # drop stock tables
    for year in range(1993, 2022, 4):
        stock_data.drop_table(file_name, f'DJI_{year}_stock')
        stock_data.drop_table(file_name, f'IXIC_{year}_stock')
    stock_data.drop_table(file_name, 'DJI_composite_stock')
    stock_data.drop_table(file_name, 'IXIC_composite_stock')

    # drop econ tables
    codes = ['UNRATE', 'UMCSENT', 'EXPGS', 'FGEXPND']
    for code in codes:
        econ_data.drop_table(file_name, f'{code}_econ')
        econ_data.drop_table(file_name, f'{code}_composite_econ')

    # drop election table
    election_data.drop_table(file_name, 'Election')

    # clear calculations file
    open("calculations.text", "w").close()

def main(start_fresh = False):
    if start_fresh:
        clear_database()
        election_data.elections_main()
        stock_data.stock_data_main()
        econ_data.econ_data_main()
        calc.run_calculations()
    else:
        election_data.elections_main()
        stock_data.stock_data_main(False, True)
        econ_data.econ_data_main(False, True)
        calc.run_calculations()

if __name__ == "__main__":
    main(start_fresh=True)
    
