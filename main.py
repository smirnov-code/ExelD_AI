from data_loader import load_excel_data
from processor import process_upsells


def main():
    input_file = 'tests/Допродажа для обработки_test.xlsx'
    output_file = 'Номенклатура_и_допродажи_(результат).xlsx'

    try:
        # Красиво вызываем функции из импортированных модулей
        df_nom, df_rules = load_excel_data(input_file)
        df_result = process_upsells(df_nom, df_rules)

        df_result.to_excel(output_file, index=False)
        print(f"Таблица успешно сгенерирована в файл: {output_file}")
        print(f"Всего создано уникальных пар для кассы: {len(df_result)}")

    except Exception as e:
        print(f"❌ Ошибка при выполнении скрипта: {e}")


if __name__ == '__main__':
    main()
