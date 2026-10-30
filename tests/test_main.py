import unittest
import pandas as pd
from processor import process_upsells


class TestPharmacyUpsell(unittest.TestCase):

    def setUp(self):
        """Готовим тестовые датафреймы перед каждым тестом."""
        # Симулируем лист Номенклатуры
        self.df_nom = pd.DataFrame({
            'Наименование': ['Магний B6 таб', 'Витамин С шип', 'Презервативы XL'],
            'Подкатегория': ['Препараты магния', 'Витамин С', 'Презервативы']
        })

        # Симулируем лист Правил (с умышленными дублями и самопродажей)
        self.df_rules = pd.DataFrame({
            'Подкатегория': [
                'Препараты магния',
                'Препараты магния',  # Дубликат правила
                'Витамин С',
                'Презервативы'        # Конфликт: презервативы к презервативам
            ],
            'Допродажа. Наименование': [
                'Глицин форте',
                'Глицин форте',
                'Цинк актив',
                'Презервативы XL'
            ]
        })

    def test_successful_merge_and_filters(self):
        """Проверяем базовый merge, удаление дубликатов и фильтр 'сам себе'."""
        result, _ = process_upsells(self.df_nom, self.df_rules)

        # Ожидаем 2 строки:
        # 1. Магний B6 таб -> Глицин форте (категория: Препараты магния)
        # 2. Витамин С шип -> Цинк актив (категория: Витамин С)
        # Презервативы должны отсеяться фильтром "сам себе"
        self.assertEqual(len(result), 2)

        # СТАЛО:
        # Проверяем, что в итоговой таблице нет ни одной строки, где препарат — Презервативы XL
        self.assertNotIn('Презервативы XL', result['препарат'].values)

    def test_empty_input(self):
        """Проверяем, что код не падает, если подать пустые таблицы."""
        empty_nom = pd.DataFrame(columns=['Наименование', 'Подкатегория'])
        empty_rules = pd.DataFrame(columns=['Подкатегория', 'Допродажа. Наименование'])

        result = process_upsells(empty_nom, empty_rules)
        self.assertTrue(result.empty)


if __name__ == '__main__':
    unittest.main()
