from datetime import datetime
import os
import pandas as pd
from data_loader import select_input_file, load_excel_data
from processor import process_upsells


def main():
    output_folder = 'Результаты'
    try:
        input_file = select_input_file('Входные_данные')
        df_nom, df_rules = load_excel_data(input_file)
        df_result = process_upsells(df_nom, df_rules)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = os.path.join(output_folder, f'Результат_{timestamp}.xlsx')

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df_result.to_excel(writer, index=False)

            # Получаем доступ к листу openpyxl для настройки ширины
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']

            # Перебираем все колонки и подбираем ширину
            for col_idx, col in enumerate(df_result.columns, start=1):
                col_letter = chr(64 + col_idx)
                worksheet.column_dimensions[col_letter].width = 40

        print(f"\n🎉 Таблица успешно сгенерирована в файл: {output_file}")
        print(f"Всего создано уникальных пар для кассы: {len(df_result)}")

    except Exception as e:
        print(f"\n❌ Ошибка при выполнении скрипта: {e}")


if __name__ == '__main__':
    main()
