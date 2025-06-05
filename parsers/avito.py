import requests
from bs4 import BeautifulSoup
import re
import json

# Функция для парсинга страницы Avito
def parse_avito(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://www.avito.ru/",
    "Cookie": "сюда_вставьте_ваши_cookie"
    }



    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Извлекаем заголовок
    title_tag = soup.find("h1", class_="title-info-title")
    title = title_tag.text.strip() if title_tag else "Не указано"
    
    # Извлекаем цену
    price_tag = soup.find("span", class_="style-item-price-text-_w822 text-text-LurtD text-size-xxl-UPhmI")
    price = re.sub(r"[^\d]", "", price_tag.text) if price_tag else "Не указано"
    
    # Извлекаем адрес
    address_tag = soup.find("span", class_="style-item-address__string-wt61A")
    address = address_tag.text.strip() if address_tag else "Не указан"
    
    # Извлекаем район (если указан)
    district_tag = soup.find("span", class_="style-item-address-georeferences-item-TZsrp")
    district = district_tag.text.strip() if district_tag else "Не указан"
    
    # Извлекаем детали квартиры
    details = {}
    info_blocks = soup.find_all("li", class_="params-paramsList__item-appQw")
    for block in info_blocks:
        key_tag = block.find("span", class_="params-paramsList__item-title-appQw")
        value_tag = block.find("span", class_="params-paramsList__item-value-appQw")
        if key_tag and value_tag:
            key = key_tag.text.strip()
            value = value_tag.text.strip()
            details[key] = value
    
    # Извлекаем условия аренды (залог, комиссия, ЖКУ)
    deposit = "Не указан"
    commission = "Не указана"
    utilities = "Не указаны"
    
    rent_conditions = soup.find_all("li", class_="params-paramsList__item-appQw")
    for condition in rent_conditions:
        text = condition.text
        if "Залог" in text:
            deposit = text.split(":")[-1].strip()
        elif "Комиссия" in text:
            commission = text.split(":")[-1].strip()
        elif "ЖКУ" in text:
            utilities = text.split(":")[-1].strip()
    
    # Извлекаем ссылки на фото
    photo_tags = soup.find_all("img", class_="photo-slider-image-ESVjQ")
    photos = [tag["src"] for tag in photo_tags] if photo_tags else []
    
    # Собираем данные в JSON
    data = {
        "Заголовок": title,
        "Цена": f"{price} ₽",
        "Район": district,
        "Адрес": address,
        "Этаж": details.get("Этаж", "Не указан"),
        "Количество комнат": details.get("Количество комнат", "Не указано"),
        "Общая площадь": details.get("Общая площадь", "Не указана"),
        "Площадь кухни": details.get("Площадь кухни", "Не указана"),
        "Жилая площадь": details.get("Жилая площадь", "Не указана"),
        "Санузел": details.get("Санузел", "Не указан"),
        "Ремонт": details.get("Ремонт", "Не указан"),
        "Мебель": details.get("Мебель", "Не указана"),
        "Интернет и ТВ": details.get("Интернет и ТВ", "Не указано"),
        "Залог": deposit,
        "Комиссия": commission,
        "ЖКУ": utilities,
        "Фото": photos
    }
    
    return data

# Пример ссылки на объявление Avito
url = "https://www.avito.ru/vladimir/kvartiry/1-k._kvartira_45_m_1313_et._3463515777"

# Парсим страницу
if __name__ == "__main__":
    result = parse_avito(url)

    # Вывод результата
    print(json.dumps(result, ensure_ascii=False, indent=4))
