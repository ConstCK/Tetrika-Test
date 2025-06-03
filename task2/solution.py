from bs4 import BeautifulSoup
from config import logger
import csv
import requests

from constants import BASE_URL




class AnimalParser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.buffer = []
        self.animals_counter = dict()

    def _get_pages(self) -> None:
        """получение страниц с удаленного адреса и запись данных в буфер"""
        logger.info('Получение страниц с удаленного адреса...')
        try:
            current_url = f'{self.url}wiki/Категория:Животные_по_алфавиту'

            while True:
                self._get_data(current_url)
                response = requests.get(current_url)
                soup = BeautifulSoup(response.text, 'html.parser')
                next_page_link = soup.find('a', string='Следующая страница')

                if not next_page_link:
                    logger.info(f'Завершение получения данных...')
                    break

                current_url = f'https://ru.wikipedia.org{next_page_link['href']}'

        except requests.exceptions.ConnectionError:
            return 'Произошла ошибка при получении страницы...'

    def _get_data(self, url: str) -> None:
        """Получение животных с указанной страницы и добавление данных в буфер"""

        logger.info(f'Получение животных с {url} и добавление данных в буфер...')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for i in soup.select('div.mw-category-group ul li a'):
            if i.attrs.get('title') and not i.attrs.get('title').startswith('Категория'):   
                self.buffer.append(i.get('title'))

    def _calculate_animals(self) -> None:
        """Получение количества животных на каждую букву алфавита и запись в словарь"""
        logger.info(f'Подсчет количества животных на каждую букву алфавита...')
        for animal in self.buffer:
            self.animals_counter[animal[0].upper()] = self.animals_counter.get(animal[0].upper(), 0) + 1

        logger.info(f'Подсчет количества животных на каждую букву алфавита завершен...')
        return self.animals_counter

    def _write_data_to_file(self, filename: str) -> None:
        """Запись данных о количестве животных для каждой буквы алфавита в файл"""
        logger.info(f'Запись данных о количестве животных в файл...')
        with open(filename, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Буква', 'Количество животных'])            
            writer.writeheader()
            for letter, count in self.animals_counter.items():
                writer.writerow({'Буква': letter, 'Количество животных': count})
        logger.info(f'Запись данных о количестве животных в файл завершена...')

    def run_parser(self) -> None:
        logger.info(f'Запуск процесса парсинга данных...')
        self._get_pages()
        self._calculate_animals()
        self._write_data_to_file('animals_counter.csv')
        logger.info(f'Процесс парсинга данных завершен...')


a = AnimalParser(BASE_URL)
a.run_parser()
