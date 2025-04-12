import pandas as pd
from parsers.avito import parse_avito, get_districts
from utils.excel_manager import save_to_excel

def get_user_input():
    # Ввод города
    city = input("🔍 Введите ваш город: ").strip()

    # Парсим районы
    print("\n📍 Загружаем районы...")
    districts = get_districts(city)
    
    if not districts:
        print("❌ Не удалось найти районы. Проверьте название города.")
        return city, None

    print("\n📌 Доступные районы:")
    for idx, district in enumerate(districts, 1):
        print(f"{idx}. {district}")

    # Выбор района
    while True:
        try:
            choice = int(input("\nВведите номер района: "))
            if 1 <= choice <= len(districts):
                selected_district = districts[choice - 1]
                break
            else:
                print("❌ Неверный номер. Выберите из списка.")
        except ValueError:
            print("❌ Введите цифру.")

    return city, selected_district

def main():
    city, district = get_user_input()

    if not district:
        print("❌ Парсинг отменен.")
        return

    print(f"\n🔎 Ищем квартиры в {city}, район: {district}...\n")

    # Парсим данные
    avito_data = parse_avito(city, district)

    if not avito_data:
        print("❌ Данные не найдены.")
        return

    # Конвертируем в DataFrame
    df = pd.DataFrame(avito_data)

    # Сохраняем в Excel
    save_to_excel(df)

    print("✅ Данные сохранены в Excel!")

if __name__ == "__main__":
    main()
