from datetime import datetime
import os
from data_loader import select_input_file, load_excel_data
from processor import process_upsells


def main():
    # Задаем имя папки для результатов
    output_folder = 'Результаты'

    try:
        # 1. Интерактивный выбор файла из папки tests
        input_file = select_input_file('Входные_данные')

        # 2. Загрузка и обработка данных
        df_nom, df_rules = load_excel_data(input_file)
        df_result = process_upsells(df_nom, df_rules)

        # 3. Создаем папку "Результаты", если её ещё нет на диске
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 4. Формируем уникальное имя файла со штампом даты и времени
        # Формат: Результат_ГГГГ-ММ-ДД_ЧЧ-ММ-СС.xlsx (например, Результат_2026-10-30_19-45-12.xlsx)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = os.path.join(output_folder, f'Результат_{timestamp}.xlsx')

        # 5. Сохранение результатов
        df_result.to_excel(output_file, index=False)
        print(f"\n🎉 Таблица успешно сгенерирована в файл: {output_file}")
        print(f"Всего создано уникальных пар для кассы: {len(df_result)}")

    except Exception as e:
        print(f"\n❌ Ошибка при выполнении скрипта: {e}")


if __name__ == '__main__':
    main()
