import os
from bs4 import BeautifulSoup
from curl_cffi import requests
from dotenv import load_dotenv
import json

load_dotenv()
url = "https://www.senukai.lt/p/akustine-dailylente-marbet-270-cm-x-30-cm-x-1-8-cm/r1jj"
page = requests.get(url, impersonate="chrome110")

api_key = os.getenv("api_key")
receiver_id = os.getenv("receiver_id")

def send_telegram(message):
    url_telegram = f"https://api.telegram.org/bot{api_key}/sendMessage"
    payload = {"chat_id": receiver_id, "text": message}
    requests.post(url_telegram, json=payload)

soup = BeautifulSoup(page.text, "html.parser")

def get_price(soup):
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            items = data if isinstance(data, list) else [data]
            for item in items:
                if item.get("@type") == "Product":
                    return item["offers"]["price"]
        except (json.JSONDecodeError, KeyError):
            continue
    return None

new_price = get_price(soup)

try:
    with open("price.txt", "r") as file:
        old_price = round(float(file.read()), 2)
except FileNotFoundError:
    old_price = new_price

if new_price < old_price:
    msg = f"Price dropped!, was - {old_price} EUR, now - {new_price} EUR"
    send_telegram(msg)

# elif new_price == old_price:
#     msg = f"Price is the same - {new_price} EUR"
#     send_telegram(msg)

if new_price > old_price:
    msg = f"Price gone up, was - {old_price} EUR, now - {new_price} EUR"
    send_telegram(msg)

if old_price != new_price:
    with open("price.txt", "w") as file:
        file.write(str(new_price))