import pandas as pd


def process_upsells(df_nom: pd.DataFrame, df_rules: pd.DataFrame) -> pd.DataFrame:
    """Очищает данные, объединяет таблицы и фильтрует конфликты саморекомендации."""
    required_cols = ['Наименование', 'Подкатегория']
    if not all(col in df_nom.columns for col in required_cols):
        raise ValueError("В первом листе Excel отсутствуют обязательные колонки: Наименование или Подкатегория")

    # Нормализуем ключевую колонку
    if 'Подкатегория' in df_nom.columns:
        df_nom['Подкатегория'] = df_nom['Подкатегория'].astype(str).str.strip()
    if 'Подкатегория' in df_rules.columns:
        df_rules['Подкатегория'] = df_rules['Подкатегория'].astype(str).str.strip()

    # Удаляем дубликаты из правил допродаж
    df_rules_clean = df_rules.drop_duplicates(subset=['Подкатегория', 'Допродажа. Наименование'])

    # INNER JOIN по подкатегории
    df_merged = pd.merge(
        df_nom[['Наименование', 'Подкатегория']],
        df_rules_clean[['Подкатегория', 'Допродажа. Наименование']],
        on='Подкатегория',
        how='inner'
    )
    df_merged.columns = ['препарат', 'категория', 'допродажа']

    # Фильтр "сам себе" (регистронезависимый)
    is_self_sale = df_merged['препарат'].str.lower().str.strip() == df_merged['допродажа'].str.lower().str.strip()
    df_final = df_merged[~is_self_sale].copy()

    return df_final[['препарат', 'допродажа', 'категория']]
