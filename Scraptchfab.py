import requests
from bs4 import BeautifulSoup
from datetime import datetime
import unidecode
import pyautogui
from time import sleep

urls = [
    "https://sketchfab.com/3d-models/brain-hologram-09d686a1a1f745cba6b2385d0c831214",
    "https://sketchfab.com/3d-models/desk-props-deluxe-09bf5678a77044e4a4847c9a8a2a2f6d",
    "https://sketchfab.com/3d-models/dna-hologram-c4a30768ac7044f182b4c4a36a7608ca",
    "https://sketchfab.com/3d-models/eye-for-free-740d560f95e748fdb54bc2a77e6f4ad7",
    "https://sketchfab.com/3d-models/anatomy-of-vision-part-2-d1a61b8d8750433fa7d6d91abcb9932c",
    "https://sketchfab.com/3d-models/hand-skeletonskin-e24e96b6bc39423b871b10f098876b8f",
    "https://sketchfab.com/3d-models/foot-skeletonskin-47acc754a2754d73902dab2ec46fd416",
    "https://sketchfab.com/3d-models/human-liver-ffa6a425ecb04b229542a66d8df21e90",
    "https://sketchfab.com/3d-models/human-organs-bced6b6ebded4845bcfb2496a6e6d35c",
    "https://sketchfab.com/3d-models/skull-9118b734cc904d2db5b967a2c1b409f7",
    "https://sketchfab.com/3d-models/realistic-human-stomach-e0f1952de7204654ba469c3e887a029b",
    "https://sketchfab.com/3d-models/human-skeleton-911b9df7e7834175b69b4840ea15e054",
    "https://sketchfab.com/3d-models/realistic-human-heart-3f8072336ce94d18b3d0d055a1ece089",
    "https://sketchfab.com/3d-models/kidney-686992c2a7fb456eaa8997b0366f4062",
    "https://sketchfab.com/3d-models/medicine-organ-the-human-kidney-54bd93f545064617bbef79013efd2192",
    "https://sketchfab.com/3d-models/shrimple-arch-round-b97997962c194e48964f91a5899b464a",
    "https://sketchfab.com/3d-models/blood-vessel-collection-of-thunthu-d0c9a48f2e414157906f46b028e1b8db"
]

sleep(3)

for url in urls:
    response = requests.get(url)
    response.encoding = 'utf-8'  
    soup = BeautifulSoup(response.text, 'html.parser')

    username = soup.find('span', class_='username-wrapper', itemprop='name').text.strip()
    model_name = soup.find('span', class_='model-name__label', itemprop='name').text.strip()
    
    date_section = soup.find('section', class_='model-meta-row publication')
    date_text = date_section.find('div', class_='tooltip tooltip-down').text.strip() # date

    date_text = date_text.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')

    date_obj = datetime.strptime(date_text, '%b %d %Y')

    year = date_obj.year
    month = date_obj.strftime('%B')
    day = date_obj.day

    username = unidecode.unidecode(username)
    model_name = unidecode.unidecode(model_name)

    APA_fields = [username, model_name, "Sketchfab", str(year), month, str(day), url]

    print(APA_fields)
    
    pyautogui.hotkey('alt', '7')
    pyautogui.press('tab', 2)
    pyautogui.write(APA_fields[0])
    pyautogui.press('tab', 3)
    for i in range(1, 7):
        pyautogui.write(APA_fields[i])
        pyautogui.press('tab')
    pyautogui.press('tab', 2)
    pyautogui.press('enter')