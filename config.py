"""Project configuration values."""

# Cookie string for authenticated Avito requests. Replace with your own if needed.
AVITO_COOKIE: str = ""

# Default HTTP headers used for Avito requests
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.avito.ru/",
    "Cookie": AVITO_COOKIE,
}

# Output paths
OUTPUT_FILE = "output/apartments.xlsx"
PRICE_CHART_FILE = "output/price_chart.png"
