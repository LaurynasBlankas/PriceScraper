import os
from bs4 import BeautifulSoup
from curl_cffi import requests
from dotenv import load_dotenv

load_dotenv()
url = "https://www.kaina24.lt/p/nukalkinimo-skystis-delonghi-ecodecalk-dlsc500-500-ml/"
page = requests.get(url, impersonate="chrome110")

api_key = os.getenv("api_key")
receiver_id = os.getenv("receiver_id")

def send_telegram(message):
    url_telegram = f"https://api.telegram.org/bot{api_key}/sendMessage"
    payload = {"chat_id": receiver_id, "text": message}
    requests.post(url_telegram, json=payload)

soup = BeautifulSoup(page.text, "html.parser")
new_price = float(soup.find("span", itemprop="lowPrice").text)

try:
    with open("price.txt", "r") as file:
        old_price = float(file.read())
except FileNotFoundError:
    old_price = new_price

if new_price < old_price:
    msg = f"Price dropped!, was - {old_price} EUR, now - {new_price} EUR"
    send_telegram(msg)

elif new_price == old_price:
    msg = f"Price is the same - {new_price} EUR"
    send_telegram(msg)
else:
    msg = f"Price gone up, was - {old_price} EUR, now - {new_price} EUR"
    send_telegram(msg)

if old_price != new_price:
    with open("price.txt", "w") as file:
        file.write(str(new_price))