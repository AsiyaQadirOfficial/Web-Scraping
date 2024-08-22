from bs4 import BeautifulSoup
import requests
import os

def playstore_apps():
    apps = soup.find_all('div', class_="ULeU3b")
    for app in apps:
        app_name = app.find('span', class_='DdYX5')
        app_name = app_name.get_text() if app_name else "Not Found!"  
        # print(f'App_Name: {app_name}')


        app_link = app.find('a', class_='Si6A0c Gy4nib')
        if app_link:
            app_link = app_link.get('href')
            app_link = 'https://play.google.com' + app_link
        else:
            app_link = "Not Found!"  
        # print(f'App_Link: {app_link}')


        organization = app.find('span', class_='wMUdtb')
        organization.get_text() if organization else "Not Found!"  
        # print(f'Organization: {organization}')


        rating = app.find('span', class_='w2kbF')
        rating = rating.get_text() if rating else "Not Found!"  
        # print(f'Rating: {rating}')
        # print()


        if app_name != "Not Found!" and app_link != "Not Found!" and organization != "Not Found!" and rating != "Not Found!":
            with open(f'{query}/{query}.txt', 'a', encoding='utf-8') as file:
                file.write(f'App_Name: {app_name}\n')
                file.write(f'App_Link: {app_link}\n')
                file.write(f'Organization: {organization}\n')
                file.write(f'Rating: {rating}\n\n')



def app_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup.prettify())


        current_url = url

            
        app_name = soup.find('h1', class_='Fd93Bb F5UCq p5VxAd') 
        if app_name:
            app_name = app_name.get_text() 
        else:
            app_name = soup.find('h1', class_='Fd93Bb F5UCq xwcR9d') 
            if app_name:
                app_name = app_name.get_text() 
            else:
                app_name = soup.find('h1', class_='Fd93Bb ynrBgc xwcR9d') 
                if app_name:
                    app_name = app_name.get_text() 
                else:
                    app_name = 'Not Found!'
        # print(f'App_Name: {app_name}')


        org_name = soup.find('div', class_='Vbfug auoIOc')
        org_name = org_name.get_text() if org_name else 'Not Found!'
        # print(f'Organization: {org_name}')



        developer = soup.find_all('div', class_='Vbfug auoIOc')
        for dev_link in developer:
            dev_link = dev_link.a['href']
            if dev_link:
                dev_link = 'https://play.google.com' + dev_link
            else:
                dev_link = 'Not Found!'
        # print(f'Developer_Page_Link: {dev_link}')


        rating = soup.find('div', class_='TT9eCd')
        rating = rating.get_text() if rating else 'Not Found!'
        # print(f'Rating: {rating}')


        reviews = soup.find('div', class_='g1rdde')
        reviews = reviews.get_text() if reviews else 'Not Found!'
        # print(f'Reviews: {reviews}')


        website = soup.find('a', class_='Si6A0c RrSxVb')
        website = website.get('href') if website else 'Not Found!'
        # print(f'Website: {website}')
        

        support_email = soup.find('div', class_='pSEeg')
        support_email = support_email.get_text() if support_email else 'Not Found!'
        # print(f'Support_Email: {support_email}\n')



        if all(value != 'Not Found!' for value in [app_name, org_name, dev_link, reviews, website, support_email]):
            with open(f'{query}/app_details.txt', 'a+', encoding='utf-8') as file:
                file.write(f'App_Link: {current_url}\n')
                file.write(f'App_Name: {app_name}\n')
                file.write(f'Rating: {rating}\n')
                file.write(f'Reviews: {reviews}\n')
                file.write(f'Website: {website}\n')
                file.write(f'Support_Email: {support_email}\n')
                file.write(f'Organization_Name: {org_name}\n')
                file.write(f'Developer_Page_Link: {dev_link}\n\n')
                file.write('--------------------------------------\n\n')

    except Exception as e:
        print(f"Failed to process URL {url}: {e}")


def developer_apps():
    pass


query = "Editors"
url = f"https://play.google.com/store/search?q={query}&c=apps"

html_content = requests.get(url).text 
soup = BeautifulSoup(html_content, 'html.parser')
# print(soup.prettify())


os.makedirs(query, exist_ok=True)
with open(f"{query}/{query}.html", "w+", encoding='utf-8') as f:
    f.write(str(soup.prettify()))


with open(f"{query}/{query}.txt", "w+", encoding='utf-8'):
    home_page = playstore_apps()


with open(f'{query}/{query}.txt','r') as f:
    content = f.readlines()
    with open(f'{query}/app_details.txt', 'w+', encoding='utf-8') as f:

        for data in content:
            try:
                if 'App_Link' in data:
                    urls = data.split('App_Link: ')[1:]
                    # urls = '\n'.join(urls)
                    # apk = data.split('=')[1]
                    # print(f'urls: {urls}')

                    for url in urls:
                        url = url.strip()
                        # print(len(url))
                        # print(f'url: {url}')

                        if url:
                            app_page = app_details(url)
                        else:
                            print(f"Invalid URL found: {url}")
            except Exception as e:
                print(f"An error occurred: {e}")



