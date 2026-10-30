from datetime import datetime
import os
import pandas as pd
from data_loader import select_input_file, load_excel_data
from processor import process_upsells


def main() -> None:
    """
    Главная управляющая функция (точка входа в приложение).

    Координирует процесс интерактивного выбора файла, загрузки данных,
    запуска бизнес-логики сопоставления и выгрузки структурированной
    отчетности в формате Excel.

    Args:
        None

    Returns:
        None
    """

    output_folder = 'Результаты'
    try:
        input_file = select_input_file('Входные_данные')
        df_nom, df_rules = load_excel_data(input_file)
        df_result, df_no_upsell = process_upsells(df_nom, df_rules)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = os.path.join(output_folder, f'Результат_{timestamp}.xlsx')

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df_result.to_excel(writer, index=False)

            worksheet = writer.sheets['Sheet1']

            for col_idx, col in enumerate(df_result.columns, start=1):
                col_letter = chr(64 + col_idx)
                worksheet.column_dimensions[col_letter].width = 40

        print(f"\n🎉 Таблица успешно сгенерирована в файл: {output_file}")
        print(f"Всего создано уникальных пар для кассы: {len(df_result)}")
        input("\n🎉 Обработка успешно завершена! Нажмите Enter для выхода...")

        missing_count = len(df_no_upsell)
        print(f"Препаратов без настроенных допродаж: {missing_count}")

        if 0 < missing_count <= 10:
            print("\n⚠️ Список препаратов без допродаж:")
            for idx, name in enumerate(df_no_upsell['препарат'], start=1):
                print(f"  [{idx}] {name}")
        elif missing_count > 10:
            err_file = os.path.join(output_folder, f'Препараты_без_допродаж_{timestamp}.xlsx')
            with pd.ExcelWriter(err_file, engine='openpyxl') as err_writer:
                df_no_upsell.to_excel(err_writer, index=False)
                err_sheet = err_writer.sheets['Sheet1']
                for col_idx in range(1, len(df_no_upsell.columns) + 1):
                    col_letter = chr(64 + col_idx)
                    err_sheet.column_dimensions[col_letter].width = 40
            print(f"⚠️ Более 10 препаратов без пар! Список выгружен в: {err_file}")

    except KeyboardInterrupt:
        print("\n\n👋 Выполнение скрипта прервано пользователем. Всего доброго!")
        input("\n🎉 Обработка успешно завершена! Нажмите Enter для выхода...")
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении скрипта: {e}")
        input("\n🎉 Обработка успешно завершена! Нажмите Enter для выхода...")


if __name__ == '__main__':
    main()
