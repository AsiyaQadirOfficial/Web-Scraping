# Scrape Books name from the website https://books.toscrape.com/
import requests
from bs4 import BeautifulSoup
import os

url = 'https://books.toscrape.com/'

html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'html.parser')
books_list = soup.find('ul', class_='nav nav-list')
book_list = books_list.text.replace(' ','')
books = book_list.split()

# for book in books:
#     print(book)

anchor_tags = books_list.find_all('a', href=True)
flag = False
with open('allBooks.txt','w') as f:
    for anchor_tag in anchor_tags:
        href = url + anchor_tag.get('href')
        parts = href.split('/')
        specific_part = parts[-2]
        # book_name = specific_part[0:-3]
        book_name = specific_part.split('_')[0]
        print(book_name)
        f.write(f'Book Type: {book_name} \n')
        f.write(f'Link: {href} \n\n')

book_type = input('Enter your Book type here: ')
found = False  
for book in books:
    mybook = book.lower()
    if book_type.lower() in mybook:
        found = True
        break

if found:
    print('Found book!')
    print(f'Filtering {book_type} related books....')
    if os.stat('relatedBooks.txt').st_size != 0:
        os.remove('relatedBooks.txt')
    with open('allBooks.txt', 'r') as content:
        all_books = content.readlines()
        for searched_book in all_books:
            if book_type in searched_book:
                print(searched_book)
                for result in searched_book:
                    with open('relatedBooks.txt', 'a+') as f:
                        f.write(f'{result}')   

else:
    print('Not Found!')

