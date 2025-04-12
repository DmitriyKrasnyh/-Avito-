import requests
from bs4 import BeautifulSoup
import random
import time

# Список User-Agent'ов для ротации
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

# Заголовки запроса
HEADERS = {
    "User-Agent": random.choice(USER_AGENTS),
    "Accept-Language": "ru,en;q=0.9",
    "Referer": "https://www.google.com/",
}

# URL для парсинга недвижимости во Владимире
URL = "https://www.avito.ru/vladimir/nedvizhimost"

# Создаем сессию для хранения cookies
session = requests.Session()
session.headers.update(HEADERS)

# Запрос к Авито
response = session.get(URL)
time.sleep(random.uniform(2, 5))  # Делаем рандомную задержку

# Проверяем успешность запроса
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Ищем блоки объявлений
    listings = soup.find_all("div", class_="iva-item-content-rejJg")  # Класс может меняться!

    for item in listings[:5]:  # Выведем 5 объявлений для теста
        title = item.find("h3")
        price = item.find("meta", itemprop="price")
        link = item.find("a", class_="link-link-MbQDP")

        if title and price and link:
            print(f"📌 Заголовок: {title.text.strip()}")
            print(f"💰 Цена: {price['content']} р.")
            print(f"🔗 Ссылка: https://www.avito.ru{link['href']}\n")
else:
    print(f"Ошибка {response.status_code}: Авито заблокировало запрос.")
