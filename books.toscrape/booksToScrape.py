# Scrape Books name from the website https://books.toscrape.com/
import requests
from bs4 import BeautifulSoup
import os
import numpy as np  
import re

url = 'https://books.toscrape.com/'
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'html.parser')
books_list = soup.find('ul', class_='nav nav-list')
book_list = books_list.text.replace(' ','')
books = book_list.split()

anchor_tags = books_list.find_all('a', href=True)
flag = False
with open('allBooks.txt','w') as f:
    for anchor_tag in anchor_tags:
        href = url + anchor_tag.get('href')
        parts = href.split('/')
        specific_part = parts[-2]
        book_name = specific_part.split('_')[0]
        print(book_name)

        f.write(f'Book Type: {book_name} \n')
        f.write(f'{href} \n\n')

book_category = input('Enter your Book category here: ')
found = False  
for book in books:
    if book_category.lower() in book.lower():
        found = True
        break
    else:
        try:
            if re.findall('[ ]|[-]',book_category):
                category = re.sub("[ ]|[-]", "", book_category)     #sub replaces one or many matches with a string
                if category.lower() in book.lower():
                    found = True
                    break
        except IndexError:
            print("Index Error!")

if found:
    print('Found book!')
    print(f'Filtering {book_category} related books....')
    if os.stat('relatedBooks.txt').st_size != 0:
        os.remove('relatedBooks.txt')
    with open('allBooks.txt', 'r') as content:
        all_books = content.readlines()
        for related_book in all_books:
            if book_category in related_book:
                # print(related_book)
                for result in related_book:
                    with open('relatedBooks.txt', 'a+') as f:
                        f.write(f'{result}') 
else:
    print('Not Found!')


with open('relatedBooks.txt','r') as f:
    content = f.readlines()  
    arr = np.array([content])
    
    i = [i for i, line in enumerate(content) if book_category.lower() in line.split()]    #matched booktype line's index
    x = [line for line in content if book_category.lower() in line.split()]     #matched booktype content
    link_index = i[0] + 1
    scraped_link = content[link_index]
    split_link = scraped_link.split('/')[0:-1]
    required_link = ('/').join(split_link)

    url_response = requests.get(required_link)
    htmlContent = url_response.text
    soup2 = BeautifulSoup(htmlContent, 'html.parser')

    alias = soup2.find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
    if os.stat('searchedBooks.txt').st_size != 0:
        os.remove('searchedBooks.txt')
    for li in alias:
        # Title of book and link here:
        book_title = li.h3.string
        print('Book Title:',book_title)

        searched_book_scraped_link = li.h3.a.get('href')
        searched_book_split_link = searched_book_scraped_link.split('/')[3:]
        searched_book_join_link2 = ('/').join(searched_book_split_link)
        
        searched_book_main_link = scraped_link.split('/')[0:-4]
        searched_book_join_link1 = ('/').join(searched_book_main_link)

        searched_book_link = searched_book_join_link1 + '/' + searched_book_join_link2
        print('Book Link:',searched_book_link)



        # Source Image Link here:
        img_tags = li.find('img', class_ = 'thumbnail') 
        source = img_tags.get('src')
        image_source = source.split('/')[4:]
        title_image_source = ('/').join(image_source)
        title_image_source_link = url + title_image_source
        print('Title Image - Source:',title_image_source_link)


        
        
        # book price and stock availability here:
        product_details = li.find('div', class_='product_price')
        
        product_price = product_details.find('p',class_='price_color')
        book_price = product_price.string
        print('Book Price:',book_price)

        product_availability = product_details.find('p',class_='instock availability')
        stock_availability = product_availability.text.strip()
        print('Stock Availability:',stock_availability)



        # rating stars
        rate_class = li.p['class']
        star_rate = rate_class[1]
        # print('Rate Class:',rate_class)
        print('Star Rate:',star_rate)
        print()


        with open('searchedBooks.txt', 'a', encoding='utf-8') as file:
            file.write(f'Book Title: {book_title}\n')
            file.write(f'Book Link: {searched_book_link}\n')
            file.write(f'Title Image Source: {title_image_source_link}\n')
            file.write(f'Book Price: {book_price}\n')
            file.write(f'Star Rate:: {star_rate}\n')
            file.write(f'Stock Availability: {stock_availability}\n\n')