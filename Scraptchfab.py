import requests
from bs4 import BeautifulSoup

APA_fields = []

url = 'https://sketchfab.com/3d-models/foot-skeletonskin-47acc754a2754d73902dab2ec46fd416'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

APA_fields.append(soup.find('span', class_='username-wrapper', itemprop='name').text.strip()) # username
APA_fields.append(soup.find('span', class_='model-name__label', itemprop='name').text.strip()) # model name
APA_fields.append("Sketchfab")

date_section = soup.find('section', class_='model-meta-row publication')
APA_fields.append(date_section.find('div', class_='tooltip tooltip-down').text.strip()) # date

print(APA_fields)