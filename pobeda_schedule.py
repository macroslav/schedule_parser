import requests
from bs4 import BeautifulSoup as BS

URL = 'https://vpobede.ru/movies/list/schedule?firstDate=2020-02-14&date=2020-02-14'

PAGE = requests.get(URL).content

schedule_soup = BS(PAGE, 'html.parser').body

schedule = schedule_soup.find('app-root', {'ng-version':'7.2.15'})

print(schedule)
