import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.filters import filter_by_price


def test_filter_by_price():
    data = [
        {"Цена": "1000"},
        {"Цена": "2000"},
        {"Цена": "3000"},
    ]
    result = filter_by_price(data, 1500, 2500)
    assert len(result) == 1
    assert result[0]["Цена"] == "2000"
