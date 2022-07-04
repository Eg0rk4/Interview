import re
import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os

"""Задаем необходимые ссылки и доп параметры"""
web_link = 'https://bashesk.ru/corporate/tariffs/unregulated/'
search_str = 'Предельные уровни нерегулируемых цен на электрическую энергию (мощность), поставляемую потребителям (покупателям) ООО "ЭСКБ", (с максимальной мощностью энергопринимающих устройств до 670 кВт) '
search_str = search_str.replace('(', '').replace(')', '')  # Не знаю почему, но когда в строках были символы (), поиск не работал

path = os.path.normpath(f'{os.getcwd()}/web_driver/chromedriver.exe')  # путь к веб драйверу


class Parser:

    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.files = {}

    def __enter__(self):
        """Метод, запускающийся при вызове 'with', запускает создание драйвера"""
        self.driver = self.create_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Метод, срабатывающий при завершении работы 'with', запускает автоматическое закрытие драйвера"""
        self.driver.close()
        self.driver.quit()
        return f'{exc_type}: {exc_val}, {exc_tb}'

    def create_driver(self):
        """Метод отвечающий за создание внб драйвера"""
        # Создаем папку, в которой будут сохранены файлы
        dir_to_save = os.path.normpath(f'{os.getcwd()}/downloads')
        if not os.path.exists(dir_to_save):
            os.mkdir(dir_to_save)
        preferences = {'download.default_directory': f'{os.path.normpath(dir_to_save)}',
                       'safebrowsing.enabled': 'false'}

        # Задаем параметры для драйвера
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('prefs', preferences)
        options.add_argument('--headless')
        service = Service(executable_path=self.driver_path)
        driver = Chrome(service=service, options=options)
        driver.maximize_window()
        return driver

    def go_to_web(self, link):
        """Выполняет переход на веб страницу"""
        self.driver.get(link)
        time.sleep(2)

    def set_start_date(self, date):
        """В строке фильтров задает начальную дату"""
        self.driver.find_elements(by=By.CLASS_NAME, value='date-picker')[0].send_keys(date)
        time.sleep(2)

    def set_end_date(self, date):
        """В строке фильтров задает конечную дату"""
        self.driver.find_elements(by=By.CLASS_NAME, value='date-picker')[1].send_keys(date)
        time.sleep(2)

    def set_filter(self):
        """В боковой стороне сайта выбирает тип тарифа"""
        menu = self.driver.find_element(by=By.CLASS_NAME, value='right-menu')
        menu.find_elements(by=By.CLASS_NAME, value='level-2')[0].click()

        time.sleep(2)

    def start_search(self):
        """Основная функция класса, запускающая алгоритм поиска"""
        self.driver.find_element(by=By.CLASS_NAME, value='btn-blue').click()
        time.sleep(2)
        self.files = {}
        table = self.driver.find_element(by=By.CLASS_NAME, value='news-list')
        results = table.find_elements(by=By.CLASS_NAME, value='row')
        self._prepare_to_download(results)
        self._find_values()

    def _find_values(self):
        """Внутренняя функция, скрытая от пользователя, отвечает за сбор информации на последующих после 1 страницах"""
        while True:
            next_page = self.driver.find_element(by=By.CLASS_NAME, value='next')

            try:
                last_page = self.driver.find_element(by=By.CLASS_NAME, value="next.disabled")
                if last_page:
                    time.sleep(2)
                    table = self.driver.find_element(by=By.CLASS_NAME, value='news-list')
                    results = table.find_elements(by=By.CLASS_NAME, value='row')
                    self._prepare_to_download(results)
                    break
            except Exception:
                pass

            if next_page:
                next_page.click()
                time.sleep(2)
                table = self.driver.find_element(by=By.CLASS_NAME, value='news-list')
                results = table.find_elements(by=By.CLASS_NAME, value='row')
                self._prepare_to_download(results)

    def _prepare_to_download(self, results):
        """Ищет необходимые документы по наименованию (так же недоступная пользователю)"""
        for value in results:
            if re.search(search_str, value.text.replace('(', '').replace(')', '')):
                file = value.find_element(by=By.CLASS_NAME, value='col-2')
                link = file.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
                self.files[value.text[:len(value.text) - 17]] = link


if __name__ == '__main__':
    with Parser(path) as web_driver:
        web_driver.go_to_web(web_link)
        web_driver.set_filter()
        web_driver.set_start_date('01.07.2019')
        web_driver.set_end_date('01.07.2020')
        web_driver.start_search()
        for key, item in web_driver.files.items():
            web_driver.go_to_web(item)
            time.sleep(1)
        print('Downloaded!')
        print('See your files in "downloads" directory')
