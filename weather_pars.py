import requests 
import bs4 
url = 'https://world-weather.ru/' 
s = requests.get(url) 
soup = bs4.BeautifulSoup(s.text, 'html.parser') 
def show_weather(): 
    weather = soup.find('div', class_='loc-now-temp') 
    return weather.text