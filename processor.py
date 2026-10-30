import pandas as pd


def process_upsells(df_nom: pd.DataFrame, df_rules: pd.DataFrame) -> pd.DataFrame:
    """
    Выполняет очистку данных, реляционное объединение таблиц по подкатегориям
    и фильтрацию логических конфликтов саморекомендации.

    Args:
        df_nom (pd.DataFrame): Датафрейм номенклатуры с обязательными
            колонками 'Наименование' и 'Подкатегория'.
        df_rules (pd.DataFrame): Датафрейм правил сопутствующих товаров
            с обязательными колонками 'Подкатегория' и 'Допродажа. Наименование'.

    Returns:
        pd.DataFrame: Очищенная матрица рекомендаций с тремя колонками
            ['препарат', 'допродажа', 'категория'], отсортированная и
            готовая к выгрузке в Excel.
    """

    required_cols = ['Наименование', 'Подкатегория']
    if not all(col in df_nom.columns for col in required_cols):
        raise ValueError("В первом листе Excel отсутствуют обязательные колонки: Наименование или Подкатегория")

    if 'Подкатегория' in df_nom.columns:
        df_nom['Подкатегория'] = df_nom['Подкатегория'].astype(str).str.strip()
    if 'Подкатегория' in df_rules.columns:
        df_rules['Подкатегория'] = df_rules['Подкатегория'].astype(str).str.strip()

    df_rules_clean = df_rules.drop_duplicates(subset=['Подкатегория', 'Допродажа. Наименование'])

    df_merged = pd.merge(
        df_nom[['Наименование', 'Подкатегория']],
        df_rules_clean[['Подкатегория', 'Допродажа. Наименование']],
        on='Подкатегория',
        how='inner'
    )
    df_merged.columns = ['препарат', 'категория', 'допродажа']

    is_self_sale = df_merged['препарат'].str.lower().str.strip() == df_merged['допродажа'].str.lower().str.strip()
    df_final = df_merged[~is_self_sale].copy()

    return df_final[['препарат', 'допродажа', 'категория']]
