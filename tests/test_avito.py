import sys
import os
import types
from unittest.mock import Mock
import xml.etree.ElementTree as ET

sample_html = '''
<html>
  <body>
    <h1 class="title-info-title">Test Apartment</h1>
    <span class="style-item-price-text-_w822 text-text-LurtD text-size-xxl-UPhmI">1 000 ₽</span>
    <span class="style-item-address__string-wt61A">Test Address</span>
    <span class="style-item-address-georeferences-item-TZsrp">Test District</span>
    <ul>
      <li class="params-paramsList__item-appQw">
        <span class="params-paramsList__item-title-appQw">Этаж</span>
        <span class="params-paramsList__item-value-appQw">5 из 10</span>
      </li>
      <li class="params-paramsList__item-appQw">
        <span class="params-paramsList__item-title-appQw">Количество комнат</span>
        <span class="params-paramsList__item-value-appQw">1</span>
      </li>
    </ul>
    <img class="photo-slider-image-ESVjQ" src="http://example.com/photo.jpg" />
  </body>
</html>
'''

class FakeTag:
    def __init__(self, element):
        self.element = element
        self.text = element.text or ""

    def __getitem__(self, item):
        return self.element.get(item)

    def find(self, name=None, class_=None):
        for child in self.element.iter():
            if name and child.tag != name:
                continue
            if class_ and child.get('class') != class_:
                continue
            return FakeTag(child)
        return None

    def find_all(self, name=None, class_=None):
        result = []
        for child in self.element.iter():
            if name and child.tag != name:
                continue
            if class_ and child.get('class') != class_:
                continue
            result.append(FakeTag(child))
        return result

class FakeBeautifulSoup(FakeTag):
    def __init__(self, html, parser):
        root = ET.fromstring(html)
        super().__init__(root)

def create_requests_stub(html):
    module = types.ModuleType("requests")
    Response = type("Response", (), {})
    response = Response()
    response.status_code = 200
    response.text = html
    module.Response = Response
    module.get = Mock(return_value=response)
    return module

def create_bs4_stub():
    module = types.ModuleType('bs4')
    module.BeautifulSoup = FakeBeautifulSoup
    return module

def test_parse_avito_basic(monkeypatch):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    fake_requests = create_requests_stub(sample_html)
    monkeypatch.setitem(sys.modules, "requests", fake_requests)
    monkeypatch.setitem(sys.modules, "bs4", create_bs4_stub())
    from importlib import reload
    import parsers.avito as avito
    reload(avito)

    data = avito.parse_avito('https://www.avito.ru/test')

    assert isinstance(data, dict)
    for key in ['Заголовок', 'Цена', 'Район', 'Адрес']:
        assert key in data
