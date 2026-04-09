from bs4 import BeautifulSoup
from curl_cffi import requests


url = "https://www.kaina24.lt/p/nukalkinimo-skystis-delonghi-ecodecalk-dlsc500-500-ml/"
page = requests.get(url, impersonate="chrome110")

api_key = os.getenv("api_key")
receiver_id = os.getenv("receiver_id")

def send_telegram(message):
    url_telegram = f"https://api.telegram.org/bot{api_key}/sendMessage"
    payload = {"chat_id": receiver_id, "text": message}
    requests.post(url_telegram, json=payload)

soup = BeautifulSoup(page.text, "html.parser")
low_price = float(soup.find("span", itemprop="lowPrice").text)

if low_price < 8.83:
    msg = f"Price dropped!, price is - {low_price} EUR"
    send_telegram(msg)

# elif low_price == 8.83:
#     print(f"Price didn't change, still {low_price} EUR")
# else:
#     print("Price has gone up")
