import pandas as pd


def process_upsells(df_nom: pd.DataFrame, df_rules: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Выполняет очистку данных, реляционное объединение таблиц по подкатегориям,
    фильтрацию конфликтов саморекомендации и поиск препаратов без допродаж.

    Args:
        df_nom (pd.DataFrame): Датафрейм номенклатуры.
        df_rules (pd.DataFrame): Датафрейм правил.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]:
            - Первый датафрейм: Успешно сформированные пары для кассы.
            - Второй датафрейм: Список препаратов, для которых не нашлось допродаж.
    """

    df_nom = df_nom.dropna(subset=['Наименование']).copy()
    df_rules = df_rules.dropna(subset=['Подкатегория', 'Допродажа. Наименование']).copy()

    if 'Подкатегория' in df_nom.columns:
        df_nom['Подкатегория'] = df_nom['Подкатегория'].astype(str).str.strip()
    if 'Подкатегория' in df_rules.columns:
        df_rules['Подкатегория'] = df_rules['Подкатегория'].astype(str).str.strip()

    df_rules_clean = df_rules.drop_duplicates(subset=['Подкатегория', 'Допродажа. Наименование'])

    df_merged = pd.merge(
        df_nom[['Наименование', 'Подкатегория']],
        df_rules_clean[['Подкатегория', 'Допродажа. Наименование']],
        on='Подкатегория',
        how='left'
    )
    df_merged.columns = ['препарат', 'категория', 'допродажа']

    # Отделяем препараты, для которых вообще не нашлось правил допродаж (у них в колонке 'допродажа' стоит NaN)
    no_upsell_mask = df_merged['допродажа'].isna()
    df_no_upsell = df_merged[no_upsell_mask][['препарат', 'категория']].drop_duplicates().copy()

    # Из основной таблицы убираем эти пустые строки
    df_valid = df_merged[~no_upsell_mask].copy()

    # Фильтр "сам себе" (регистронезависимый)
    is_self_sale = df_valid['препарат'].str.lower().str.strip() == df_valid['допродажа'].str.lower().str.strip()
    df_final = df_valid[~is_self_sale].copy()

    # Наводим порядок в столбцах
    df_final = df_final[['препарат', 'допродажа', 'категория']]

    return df_final, df_no_upsell

