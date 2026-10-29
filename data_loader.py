import os
import pandas as pd


def load_excel_data(file_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Загружает номенклатуру и правила допродаж из Excel файла."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Исходный файл не найден по пути: {file_path}")

    df_nom = pd.read_excel(file_path, sheet_name=0)
    df_rules = pd.read_excel(file_path, sheet_name=1)

    # Очищаем заголовки от случайных пробелов
    df_nom.columns = df_nom.columns.str.strip()
    df_rules.columns = df_rules.columns.str.strip()

    return df_nom, df_rules
