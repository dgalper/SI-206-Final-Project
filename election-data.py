import sqlite3
import json
import os
import requests
import re
from bs4 import BeautifulSoup
# returns the winning party for a given election year
def get_winning_party(year):
    # fix error where 2008 isn't able to be scraped
    if year == "2008":
        return "Democratic"
    url = f"https://www.presidency.ucsb.edu/statistics/elections/{year}"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    regex_winner = r"winner"
    td_tag = soup.find_all("td")
    for i in range(len(td_tag)):
        if re.search(regex_winner,str(td_tag[i])):
            winning_party = td_tag[i - 1].text.strip()
    return winning_party
# return a list of dicts of year and winning party for the given years 
def compile_election_data(start_year, end_year):
    year_winner_list = []
    year = start_year
    while year <= end_year:
        year_winner_dict = {}
        year_winner_dict[year] = get_winning_party(year)
        year_winner_list.append(year_winner_dict)
        year = int(year)
        year += 4
        year = str(year)
    return year_winner_list
# open db, create a table and add the data to it, limit to 25 items using start_num and end_num
def enter_into_database(db_name, table_name ,year_winner_list, start_index, end_index):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, election_year INTEGER, winning_party TEXT)')
    while start_index <= end_index:
        year = list(year_winner_list[start_index])[0]
        # print(year)
        winning_party = year_winner_list[start_index][year]
        # print(winning_party)
        cur.execute(f'INSERT INTO {table_name} (election_year, winning_party) VALUES (?, ?)', (year, winning_party))
        start_index += 1
    conn.commit()

# drop table if needed
def drop_table(data_base, table_name):
    conn = sqlite3.connect(data_base)
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS {table_name}')
    conn.commit()
        
def elections_main():
    #print(get_winning_party("1904"))
    drop_table("all_data.db", "Election")
    year_winner_list = compile_election_data("1904","2020")
    len_year_winner_list = (len(year_winner_list))
    last_index = len_year_winner_list - 1
    enter_into_database("all_data.db", "Election" ,year_winner_list, 0, 24)
    enter_into_database("all_data.db", "Election" ,year_winner_list, 25, last_index)

if __name__ == "__main__":
    elections_main()
    


     

 