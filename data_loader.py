import os
import pandas as pd


def select_input_file(folder_path: str = 'tests') -> str:
    """
        Интерактивно сканирует папку и запрашивает у пользователя выбор файла.

        Args:
            folder_path (str): Путь к директории с исходными файлами. По умолчанию 'tests'.

        Returns:
            str: Полный относительный путь к выбранному Excel-файлу.

        Raises:
            FileNotFoundError: Если папка пуста или в ней нет файлов формата .xlsx.
        """

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        raise FileNotFoundError(
            f"Папка '{folder_path}' не найдена. Мы создали её. "
            f"Пожалуйста, положите туда исходные Excel-файлы и запустите скрипт снова."
        )

    files = [f for f in os.listdir(folder_path)
             if f.endswith('.xlsx') and not f.startswith('~$')]

    if not files:
        raise FileNotFoundError(f"В папке '{folder_path}' нет доступных Excel-файлов (.xlsx).")

    print("\n📋 Доступные файлы для обработки:")
    for idx, file_name in enumerate(files, start=1):
        print(f"[{idx}] {file_name}")

    while True:
        try:
            choice = input(f"\nВведите номер файла (1-{len(files)}): ").strip()
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(files):
                selected_file = os.path.join(folder_path, files[choice_idx])
                print(f"✅ Выбран файл: {files[choice_idx]}")
                return selected_file
            else:
                print(f"❌ Неверный номер. Введите число от 1 до {len(files)}.")
        except ValueError:
            print("❌ Пожалуйста, введите корректное число.")


def load_excel_data(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Загружает номенклатуру и правила допродаж из листов выбранного Excel-файла.

    Args:
        file_path (str): Путь к целевому Excel-файлу для чтения.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Кортеж из двух датафреймов:
            - Первый: Таблица номенклатуры (препараты).
            - Второй: Таблица правил (сопутствующие товары).
    """

    df_nom = pd.read_excel(file_path, sheet_name=0)
    df_rules = pd.read_excel(file_path, sheet_name=1)

    df_nom.columns = df_nom.columns.str.strip()
    df_rules.columns = df_rules.columns.str.strip()

    return df_nom, df_rules
