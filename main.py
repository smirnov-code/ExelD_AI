import pandas as pd

# 1. Загружаем данные с двух разных листов
excel_file = 'tests/Допродажа для обработки_test.xlsx'
df_nomenclature = pd.read_excel(excel_file, sheet_name=0)
df_upsell_rules = pd.read_excel(excel_file, sheet_name=1)

# Очищаем текстовые поля от скрытых пробелов в начале и конце строк
for df in [df_nomenclature, df_upsell_rules]:
    df.columns = df.columns.str.strip()
    if 'Подкатегория' in df.columns:
        df['Подкатегория'] = df['Подкатегория'].astype(str).str.strip()

# Убираем дубликаты из правил допродаж, если они там случайно задвоились
df_upsell_rules = df_upsell_rules.drop_duplicates(subset=['Подкатегория', 'Допродажа. Наименование'])

# 2. Делаем INNER JOIN по подкатегории
df_result = pd.merge(
    df_nomenclature[['Наименование', 'Подкатегория']],
    df_upsell_rules[['Подкатегория', 'Допродажа. Наименование']],
    on='Подкатегория',
    how='inner'
)

# Переименовываем столбцы под финальный формат
df_result.columns = ['препарат', 'категория', 'допродажа']

# 3. УМНЫЙ ФИЛЬТР: Препарат не должен предлагать сам себя
# Переводим в нижний регистр для точного сравнения (на случай разного регистра)
is_self_sale = df_result['препарат'].str.lower().str.strip() == df_result['допродажа'].str.lower().str.strip()
df_final = df_result[~is_self_sale].copy()

# Наводим финальный порядок столбцов (препарат + допродажа + категория)
df_final = df_final[['препарат', 'допродажа', 'категория']]

# 4. Сохраняем в новый файл
output_file = 'Номенклатура_и_допродажи_(результат).xlsx'
df_final.to_excel(output_file, index=False)

print(f"Таблица успешно сгенерирована в файл: {output_file}")
print(f"Всего создано уникальных пар для кассы: {len(df_final)}")
