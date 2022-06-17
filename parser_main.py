import re
import time
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from termcolor import cprint

web_link = 'https://bashesk.ru/corporate/tariffs/unregulated/'
search_str = 'Предельные уровни нерегулируемых цен на электрическую энергию (мощность), поставляемую потребителям (покупателям) ООО "ЭСКБ", (с максимальной мощностью энергопринимающих устройств до 670 кВт) '
search_str = search_str.replace('(', '').replace(')', '')  # Не знаю почему, но когда в строках были символы (), поиск не работал
path = os.path.normpath('C:/WebDrivers/chromedriver.exe')
preferences = {'download.default_directory': f'{os.path.normpath("C:/Users/Egor-/Desktop/Барабаш/Собес/Parsed_docs")}',
               'safebrowsing.enabled': 'false'}


class Parser:

    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.docs = []

    def __enter__(self):
        self.driver = self._create_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()
        return f'{exc_type}: {exc_val}, {exc_tb}'

    def _create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('prefs', preferences)
        # options.add_argument('--headless')
        service = Service(executable_path=self.driver_path)
        driver = Chrome(service=service, options=options)
        driver.maximize_window()
        return driver

    def go_to_web(self, link):
        self.driver.get(link)
        time.sleep(2)

    def set_start_date(self, date):
        self.driver.find_elements(by=By.CLASS_NAME, value='date-picker')[0].send_keys(date)
        time.sleep(2)

    def set_end_date(self, date):
        self.driver.find_elements(by=By.CLASS_NAME, value='date-picker')[1].send_keys(date)
        time.sleep(2)

    def set_filter(self):
        menu = self.driver.find_element(by=By.CLASS_NAME, value='right-menu')
        menu.find_elements(by=By.CLASS_NAME, value='level-2')[0].click()

        time.sleep(2)

    def start_search(self):
        self.driver.find_element(by=By.CLASS_NAME, value='btn-blue').click()
        time.sleep(2)
        files = {}

        table = self.driver.find_element(by=By.CLASS_NAME, value='news-list')
        results = table.find_elements(by=By.CLASS_NAME, value='row')
        for value in results:
            if re.search(search_str, value.text.replace('(', '').replace(')', '')):
                file = value.find_element(by=By.CLASS_NAME, value='col-2')
                link = file.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
                files[value.text[:len(value.text)-17]] = link

        return files

        # try:
        #     while True:
        #         files.append(self._find_values())
        # except EOFError as exc:
        #     print(exc)
        #
        # finally:
        #     for lst in files:
        #         for value in lst:
        #             self.docs.append(value.find_element(by=By.TAG_NAME, value='a').get_attribute('href'))
        #     return self.docs

    def _find_values(self):
        try:
            next_page = None
            # next_page = self.driver.find_element(by=By.CLASS_NAME, value='next')
            last_page = self.driver.find_element(by=By.CLASS_NAME, value='next disabled')
            if next_page:
                print('next')
                next_page.click()
                time.sleep(2)
                return self.driver.find_elements(by=By.CLASS_NAME, value='col-2')
            elif last_page:
                print('last')
                raise Exception
            else:
                print('end')
                raise Exception
        except Exception:
            raise EOFError










with Parser(path) as web_driver:
    web_driver.go_to_web(web_link)
    web_driver.set_filter()
    web_driver.set_start_date('01.07.2019')
    web_driver.set_end_date('01.07.2020')
    docs = web_driver.start_search()
    for key, item in docs.items():
        print(f'{key}: {item}')
        web_driver.go_to_web(item)
        print('Downloaded!')



