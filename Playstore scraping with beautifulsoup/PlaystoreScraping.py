from bs4 import BeautifulSoup
import requests
import os

def playstore_apps():
    apps = soup.find_all('div', class_="ULeU3b")
    for app in apps:
        app_name = app.find('span', class_='DdYX5')
        if app_name:
            app_name = app_name.get_text()
        else:
            app_name = "Not Found!"  



        app_link = app.find('a', class_='Si6A0c Gy4nib')
        if app_link:
            app_link = app_link.get('href')
            app_link = 'https://play.google.com' + app_link
        else:
            app_link = "Not Found!"  



        organization_name = app.find('span', class_='wMUdtb')
        if organization_name:
            organization = organization_name.get_text()
        else:
            organization = "Not Found!"  



        rating = app.find('span', class_='w2kbF')
        if rating:
            rating = rating.get_text()
        else:
            rating = "Not Found!"  



        # print(f'App_Name: {app_name}')
        # print(f'App_Link: {app_link}')
        # print(f'Organization: {organization}')
        # print(f'Rating: {rating}')
        # print()


        # if all(value != "Not Found!" for value in [app_name, app_link, organization, rating]):
        if app_name != "Not Found!" and app_name != "Not Found!" and organization != "Not Found!" and rating != "Not Found!":
            with open(f'{query}/{query}.txt', 'a', encoding='utf-8') as file:
                file.write(f'App_Name: {app_name}\n')
                file.write(f'App_Link: {app_link}\n')
                file.write(f'Organization: {organization}\n')
                file.write(f'Rating: {rating}\n\n')



query = "Editors"
url = f"https://play.google.com/store/search?q={query}&c=apps"

html_content = requests.get(url).text 
soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.prettify())


# html file
os.makedirs(query, exist_ok=True)
with open(f"{query}/{query}.html", "w+", encoding='utf-8') as f:
    f.write(str(soup.prettify()))

# home page apps 
with open(f"{query}/{query}.txt", "w+", encoding='utf-8') as f:
    main_page = playstore_apps()



