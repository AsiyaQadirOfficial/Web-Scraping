# Extract Free proxies list in real time (continuous updating data)

import requests
from bs4 import BeautifulSoup
import time

url = 'https://free-proxy-list.net/'

r = requests.get(url)
content = r.content

soup = BeautifulSoup(content, 'html.parser')

def ip_addr():
    with open('proxies.txt','w') as f:
        table_data = soup.find_all('table', class_='table table-striped table-bordered')
        for table in table_data:
            td_first_column = table.select('tr td:nth-child(1)')
        
            for td in td_first_column:
                td_data = td.text

                #to print data in file 
                f.write(td_data + '\n')
                print(td_data)


if __name__ == '__main__':
    while True:
        ip_addr()
        time_wait = 600
        print(f'waiting for {time_wait} sec...','\n')
        time.sleep(time_wait)