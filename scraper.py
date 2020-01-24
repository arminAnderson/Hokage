import requests
from bs4 import BeautifulSoup

#page = requests.get("http://192.168.100.56:8080/#/")
#print(page)
soup = BeautifulSoup(open("Code Ninjas - Progress Tracking.html"), 'html.parser')
#print(soup)
print(soup.find_all("tr"))