import openpyxl
from openpyxl.drawing.image import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd

OUTPUT_FILE = "output/apartments.xlsx"

def save_to_excel(df):
    print("📂 Сохраняем данные в Excel...")
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Квартиры"

    ws.append(list(df.columns))

    for i, row in df.iterrows():
        ws.append(row.tolist())

        for j in range(3):
            photo_url = row[f"Фото {j+1}"]
            if photo_url:
                try:
                    img_data = requests.get(photo_url).content
                    img = Image(BytesIO(img_data))
                    img.width, img.height = 100, 75
                    ws.add_image(img, f"H{i+2}")
                except:
                    pass

    ws_chart = wb.create_sheet("Графики")

    df["Цена"] = df["Цена"].astype(int)
    df_grouped = df.groupby("Район")["Цена"].mean().sort_values()

    plt.figure(figsize=(10, 5))
    df_grouped.plot(kind="bar", color="skyblue")
    plt.title("Средняя цена аренды по районам")
    plt.ylabel("Цена, ₽")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("output/price_chart.png")

    img_chart = Image("output/price_chart.png")
    ws_chart.add_image(img_chart, "A1")

    wb.save(OUTPUT_FILE)
    print(f"✅ Файл сохранен: {OUTPUT_FILE}")
