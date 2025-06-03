import unittest
from unittest.mock import patch, MagicMock
import csv
import os
from solution import AnimalParser
from constants import ANIMALS, BASE_URL, DATA


class TestAnimalParser(unittest.TestCase):
    def setUp(self):
        self.test_url = BASE_URL
        self.parser = AnimalParser(self.test_url)

    def test_initialization(self):
        """Тест на инициализацию парсера"""
        self.assertEqual(self.parser.url, self.test_url)
        self.assertEqual(self.parser.buffer, [])
        self.assertEqual(self.parser.animals_counter, {})

    def test_calculate_animals(self):
        """Тест на подсчет количества животных"""
        self.parser.buffer = ANIMALS
        self.parser._calculate_animals()

        expected_result = {'А': 2, 'Б': 1, 'В': 1}
        self.assertEqual(self.parser.animals_counter, expected_result)

    def test_write_data_to_file(self):
        """Тест на запись в файл"""
        self.parser.animals_counter = DATA
        test_filename = 'test_animals_counter.csv'

        self.parser._write_data_to_file(test_filename)
        self.assertTrue(os.path.exists(test_filename))

        with open(test_filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0]['Буква'], 'А')
            self.assertEqual(rows[0]['Количество животных'], '2')

        os.remove(test_filename)

    @patch('solution.requests.get')
    def test_get_data(self, mock_get):
        """Тест на парсинг мок страницы"""
        mock_response = MagicMock()
        mock_response.text = '''
        <div class="mw-category-group">
            <ul>
                <li><a title="Антилопа">Антилопа</a></li>
                <li><a title="Буйвол">Буйвол</a></li>
                <li><a title="Категория:Млекопитающие">Млекопитающие</a></li>
            </ul>
        </div>
        '''
        mock_get.return_value = mock_response

        self.parser._get_data(self.test_url)

        self.assertEqual(len(self.parser.buffer), 2)
        self.assertIn('Антилопа', self.parser.buffer)
        self.assertIn('Буйвол', self.parser.buffer)
        self.assertNotIn('Млекопитающие', self.parser.buffer)


if __name__ == '__main__':
    unittest.main()
