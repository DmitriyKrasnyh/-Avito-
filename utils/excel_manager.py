"""Helpers for exporting parsed data to Excel."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import openpyxl
import pandas as pd
import requests
from openpyxl.drawing.image import Image

import config


def save_to_excel(df: pd.DataFrame, output: Path | None = None) -> Path:
    """Save the provided DataFrame to an Excel file with basic charts.

    Parameters
    ----------
    df: pandas.DataFrame
        Parsed apartments information.
    output: pathlib.Path | None
        Destination file path. Uses ``config.OUTPUT_FILE`` by default.

    Returns
    -------
    pathlib.Path
        Path to the saved file.
    """
    destination = Path(output or config.OUTPUT_FILE)
    destination.parent.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Квартиры"

    ws.append(list(df.columns))

    for i, row in df.iterrows():
        ws.append(row.tolist())
        for j in range(3):
            photo_url = row.get(f"Фото {j+1}")
            if not photo_url:
                continue
            try:
                img_data = requests.get(photo_url, timeout=10).content
                img = Image(BytesIO(img_data))
                img.width, img.height = 100, 75
                ws.add_image(img, f"H{i+2}")
            except requests.RequestException:
                pass

    ws_chart = wb.create_sheet("Графики")

    df["Цена"] = df["Цена"].astype(int)
    df_grouped = df.groupby("Район")["Цена"].mean().sort_values()

    chart_path = Path(config.PRICE_CHART_FILE)
    chart_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 5))
    df_grouped.plot(kind="bar", color="skyblue")
    plt.title("Средняя цена аренды по районам")
    plt.ylabel("Цена, ₽")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(chart_path)

    ws_chart.add_image(Image(str(chart_path)), "A1")

    wb.save(destination)
    return destination
