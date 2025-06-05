"""Utilities for parsing apartment pages on Avito."""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Optional

import requests
from bs4 import BeautifulSoup

import config


def parse_avito(url: str, *, headers: Optional[dict[str, str]] = None) -> Optional[Dict[str, Any]]:
    """Parse a single Avito advertisement page.

    Parameters
    ----------
    url: str
        Link to the Avito advertisement.
    headers: dict[str, str] | None
        Optional HTTP headers. If not provided ``config.HEADERS`` is used.

    Returns
    -------
    dict | None
        Parsed advertisement data or ``None`` when the page cannot be retrieved.
    """
    req_headers = headers or config.HEADERS

    try:
        response = requests.get(url, headers=req_headers, timeout=10)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", class_="title-info-title")
    title = title_tag.text.strip() if title_tag else "Не указано"

    price_tag = soup.find(
        "span",
        class_="style-item-price-text-_w822 text-text-LurtD text-size-xxl-UPhmI",
    )
    price = re.sub(r"[^\d]", "", price_tag.text) if price_tag else "0"

    address_tag = soup.find("span", class_="style-item-address__string-wt61A")
    address = address_tag.text.strip() if address_tag else "Не указан"

    district_tag = soup.find("span", class_="style-item-address-georeferences-item-TZsrp")
    district = district_tag.text.strip() if district_tag else "Не указан"

    details: Dict[str, str] = {}
    info_blocks = soup.find_all("li", class_="params-paramsList__item-appQw")
    for block in info_blocks:
        key_tag = block.find("span", class_="params-paramsList__item-title-appQw")
        value_tag = block.find("span", class_="params-paramsList__item-value-appQw")
        if key_tag and value_tag:
            key = key_tag.text.strip()
            value = value_tag.text.strip()
            details[key] = value

    deposit = "Не указан"
    commission = "Не указана"
    utilities = "Не указаны"

    for condition in info_blocks:
        text = condition.text
        if "Залог" in text:
            deposit = text.split(":")[-1].strip()
        elif "Комиссия" in text:
            commission = text.split(":")[-1].strip()
        elif "ЖКУ" in text:
            utilities = text.split(":")[-1].strip()

    photo_tags = soup.find_all("img", class_="photo-slider-image-ESVjQ")
    photos = [tag["src"] for tag in photo_tags] if photo_tags else []

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
        "Фото": photos,
    }

    return data
