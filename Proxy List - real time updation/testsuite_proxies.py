import requests
from bs4 import BeautifulSoup

url = 'https://free-proxy-list.net/'

r = requests.get(url)
content = r.content
# print(content)


soup = BeautifulSoup(content, 'html.parser')
# print(soup)

# write the soup content in html file 
# with open('proxylist.html','w') as htmlcont:
#     htmlcont.write(str(soup))


# lets try to fetch ip addresses

with open('proxies.txt','w') as f:
    table_data = soup.find_all('table', class_='table table-striped table-bordered')
    for table in table_data:
    # this will print first row
    # row = table.tr.text
    # print(row)

    # this will print first cell data
    # data = table.td.text
    # print(data)
    
    # this will print all tr
    # tr_data = table.find_all('tr')
    # print(tr_data)

    # this will print all td
    # td_data = table.find_all(['td'])
    # print(td_data) 

    # this will select first column containing all free proxies
        # first_column = soup.select('tr td:first-child').text            
        # print(first_column)
        
        # we can also write ( td:first-child ) as ( td:nth-child(1) ) 
        td_first_column = table.select('tr td:nth-child(1)')

        # for td in td_first_column:
        #     td_data = f.write(td.text)
        #     print(td_data)

        for td in td_first_column:
            td_data = td.text
            proxies = f.write(td_data + '\n')
            print(td_data)

            # output = ('\n').join([proxies])
            # print(f'''
            #         {proxies}
            #         ''')




















