# https://www.timesjobs.com/
# it'll scrap the python jobs, company names and more info about the job excluding the jobs which contain unfamiliar skills mentioned/input by you

from bs4 import BeautifulSoup
import requests
import time

print('put some skill that you are not familiar with:')
unfamiliar_skills = input('>')
unfamiliar_skill = unfamiliar_skills.split(',')
print(f'Filtering out {unfamiliar_skill}....')

def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text

    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    for index, job in enumerate(jobs):
        published_date = job.find('span', class_ = 'sim-posted').span.text

        if 'few' in published_date:
            company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ','')
            skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')
            more_info = job.header.h2.a['href']
            
            if all(unfamiliar_skill not in skills for unfamiliar_skill in unfamiliar_skill):               
                with open(f'posts/{index}.txt', 'w') as f:   
                    f.write(f"Company Name: {company_name.strip()} \n")
                    f.write(f"Required Skills: {skills.strip()} \n")
                    f.write(f"More Info: {more_info}")

                    print(f'File Saved: {index}')


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)



'''
for unfamiliar_skill in unfamiliar_skill: This is a generator expression that iterates over each skill in the list unfamiliar_skill. In Python, you can use the same variable name for both the iterable and the iterator. So, unfamiliar_skill is both the list of unfamiliar skills and the individual skill within that list during iteration.

unfamiliar_skill not in skills: This checks if the current unfamiliar_skill is not present in the string skills. It returns True if the skill is not found, False otherwise.

all(...): This function returns True if all elements of the iterable inside it are True, and False if any element is False. It's used here to ensure that all unfamiliar skills are not present in the skills string.
'''






























# program given below will exclude only single unfamiliar skill, but in above program you can exclude multiple unfamiliar skills

# from bs4 import BeautifulSoup
# import requests
# import time

# print('put some skill that you are not familiar with:')
# unfamiliar_skill = input('>')
# print(f'Filtering out {unfamiliar_skill}....')

# def find_jobs():
#     html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text

#     soup = BeautifulSoup(html_text, 'lxml')
#     jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

#     # The enumerate() function takes a collection (e.g. a tuple) and returns it as an enumerate object.(enumerate mean mention 'a number of things' one by one)
#     for index, job in enumerate(jobs):
#         published_date = job.find('span', class_ = 'sim-posted').span.text

#         if 'few' in published_date:
#             company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ','')
#             skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')
#             more_info = job.header.h2.a['href']
            
#             if unfamiliar_skill not in skills:
#                 with open(f'posts/{index}.txt', 'w') as f:   
#                     f.write(f"Company Name: {company_name.strip()} \n")
#                     f.write(f"Required Skills: {skills.strip()} \n")
#                     f.write(f"More Info: {more_info}")

#                     print('File Saved')

# if __name__ == '__main__':
#     while True:
#         find_jobs()
#         time_wait = 10
#         print(f'Waiting {time_wait} minutes...')
#         time.sleep(time_wait * 60)


































# This program given below will scrap tha data on CLI. 

# from bs4 import BeautifulSoup
# import requests

# html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text
# # print(html_text)

# soup = BeautifulSoup(html_text, 'lxml')
# jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

# for job in jobs:
#     published_date = job.find('span', class_ = 'sim-posted').span.text

#     if 'few' in published_date:
#         company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ','')
#         skills = job.find('span', class_ = 'srp-skills').text.replace(' ','')
#         more_info = job.header.h2.a['href']
#         print(f"Company Name: {company_name.strip()}")
#         print(f"Required Skills: {skills.strip()}")
#         print(f"More Info: {more_info}")

#         print()
