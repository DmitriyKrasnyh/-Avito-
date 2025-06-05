"""Command line interface for parsing a single Avito advertisement."""

from __future__ import annotations

import pandas as pd

from parsers.avito import parse_avito
from utils.excel_manager import save_to_excel


def main() -> None:
    url = input("🔗 Введите ссылку на объявление Avito: ").strip()
    data = parse_avito(url)
    if not data:
        print("❌ Не удалось получить данные.")
        return

    df = pd.DataFrame([data])
    output_file = save_to_excel(df)
    print(f"✅ Данные сохранены в {output_file}")


if __name__ == "__main__":
    main()
