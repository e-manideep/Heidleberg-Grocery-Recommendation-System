import csv
import datetime
import os
import time

import pandas
import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium import webdriver


class Kaufland:
    def __init__(self, *args):
        self.STORE_NAME = "Kaufland"
        self.COOKIE_BUTTON_CLICKED = False
        self.first_line = True
        self.URL = 'https://filiale.kaufland.de/angebote/aktuelle-woche/uebersicht.category=01_Fleisch__Gefl%C3' \
                   '%BCgel__Wurst.html '
        self.product_name = ''
        self.product_image = ''
        self.payback_points = 'Keine Payback-Punkte'
        self.payback_condition = 'Keine Payback-Bedingung'
        self.product_link = ''
        self.product_quantity = ''
        self.tag_label = ''
        self.price = '0'
        self.product_information = 'Keine Produktinformation'
        self.store_pin_code = args[0]
        self.store_address = args[1]
        self.category = ''
        self.from_to_date = ''
        # self.chrome_options = uc.ChromeOptions()
        self.chrome_options = Options()
        self.chrome_options.headless = True
        # self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.79")
        self.chrome_options.add_argument("--window-size=1440, 900")
        self.chrome_options.add_argument('--start-maximized')
        service = Service(executable_path=r'chromedriver')
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        # self.driver = uc.Chrome(options=self.chrome_options)
        self.driver.get(self.URL)
        self.wait = WebDriverWait(self.driver, 10)
        print(self.driver.get_cookies())

    def get_product_information(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            self.product_information = soup.find('div',
                                                 class_='t-offer-detail__description').text
        except AttributeError:
            self.product_information = 'Keine Produktinformation'

        try:
            self.product_image = soup.find('div', class_='o-slider__list').find('img')['src']
        except (AttributeError, TypeError):

            self.product_image = ''

        try:

            self.price = soup.find('div', class_='a-pricetag__price').text
        except AttributeError:

            self.price = ''
        try:

            product_subtitle = soup.find('h2',
                                         class_='t-offer-detail__subtitle').text.strip()
        except AttributeError:
            product_subtitle = ""

        try:

            self.tag_label = soup.find('div', class_="a-pricetag__discount").text
        except AttributeError:

            self.tag_label = "Kein Etikett"
        try:

            self.from_to_date = soup. \
                find('div', class_="a-eye-catcher a-eye-catcher--secondary").text
        except AttributeError:

            self.from_to_date = ""
        try:

            product_title = soup.find('h1', class_='t-offer-detail__title').text.strip()
        except AttributeError:

            self.product_name = ''
        else:
            self.product_name = product_subtitle + ' ' + product_title
        try:
            product_offer_quantity = soup.find('div',
                                               class_='t-offer-detail__quantity').text
        except AttributeError:

            product_offer_quantity = ''
        try:
            product_basic_quantity = soup.find('div',
                                               class_='t-offer-detail__basic-price').text
        except AttributeError:
            self.product_quantity = 'Keine Mengenangaben'
        else:
            self.product_quantity = product_offer_quantity + ' ' + product_basic_quantity

    def init_scraping(self):
        while not self.COOKIE_BUTTON_CLICKED:
            time.sleep(10)
            try:
                cookie_button = self.driver.find_element(By.CLASS_NAME, 'cookie-alert-extended-button')
            except NoSuchElementException:
                print('No such element Exception')
            else:
                self.COOKIE_BUTTON_CLICKED = True
                try:
                    cookie_button.click()
                except:
                    print('its failed to click cookie button')
                    self.driver.quit()
                else:
                    self.handle_scrape()

    def handle_scrape(self):
        try:
            time.sleep(5)
            branch_button = self.driver.find_element(By.CSS_SELECTOR, 'div.m-store-info__change')
        except NoSuchElementException:
            print('no such element exception')
        else:
            branch_button.click()
            time.sleep(4)
            try:
                input_field = self.wait.until(EC.element_to_be_clickable((By.ID, 'store-search')))
            except (NoSuchElementException, TimeoutException):
                print('no such element exception')
            else:
                input_field.send_keys(self.store_pin_code)
                input_field.send_keys(Keys.ENTER)
                time.sleep(4)
                try:
                    choose_store_button = self.wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR,
                         'div.a-button.a-button--secondary.a-button--full.a-button--storelist-choose a')))
                # print(driver.find_element(By.CLASS_NAME,'a-button a-button--secondary a-button--full
                # a-button--storelist-choose'))
                except (NoSuchElementException, TimeoutException):
                    print('Execption')
                else:

                    choose_store_button.click()
                    time.sleep(3)
                    try:
                        all_category_link = [each.get_attribute('href') for each in
                                             self.driver.find_elements(By.CSS_SELECTOR,
                                                                       '.m-accordion--overview-list .m-accordion__link')
                                             ]

                    except (NoSuchElementException, TimeoutException):
                        print('All_categories exception')
                    else:

                        category_list = [each.text for each in
                                         self.driver.find_elements(By.CSS_SELECTOR,
                                                                   '.m-accordion--overview-list .m-accordion__link')]

                        for index, each_category in enumerate(all_category_link):
                            time.sleep(5)
                            self.driver.get(each_category)
                            self.category = category_list[index]
                            try:
                                all_products = self.wait.until(
                                    EC.presence_of_all_elements_located(
                                        (By.CLASS_NAME, 'g-col.o-overview-list__list-item')))
                            except (NoSuchElementException, TimeoutException):
                                print('all_products_error')
                                all_products = []
                            else:
                                print(all_products, 'all_products')
                            for product in all_products:
                                try:
                                    self.product_link = product.find_element(By.CSS_SELECTOR,
                                                                             'div.m-offer-tile.m-offer-tile--line-through.m-offer-tile--mobile a.m-offer-tile__link.u-button--hover-children') \
                                        .get_attribute('href')
                                except(NoSuchElementException, TimeoutException):
                                    print('product_link error')
                                    self.product_link = ''
                                else:
                                    data = pandas.read_csv('all_unique_kaufland_links.csv')

                                    if (len(data[data.product_link == self.product_link])) < 1:
                                        new_data = pandas.DataFrame({'product_link': [self.product_link]})
                                        data = pandas.concat([data, new_data], axis=0, ignore_index=True)

                                        data.to_csv('all_unique_kaufland_links.csv', index=False)

                                    response = requests.get(self.product_link)
                                    self.get_product_information(response)

                                    with open(f'Kaufland/{datetime.datetime.now().date()}.csv', mode='a', newline='',
                                              encoding='utf-8') as file:
                                        writer = csv.writer(file)

                                        if self.first_line:
                                            writer.writerow(["product_name",
                                                             "product_image",
                                                             "payback_points",
                                                             "product_link",
                                                             "payback_condition",
                                                             "product_quantity",
                                                             "tag_label",
                                                             "price",
                                                             "product_information",
                                                             "store_address", 'store', 'category', 'offer_duration',
                                                             'date'])
                                            self.first_line = False

                                        writer.writerow([self.product_name.strip(),
                                                         self.product_image,
                                                         self.payback_points,
                                                         self.product_link,
                                                         self.payback_condition,
                                                         self.product_quantity,
                                                         self.tag_label,
                                                         self.price,
                                                         self.product_information.strip(),
                                                         self.store_address,
                                                         self.STORE_NAME,
                                                         self.category, self.from_to_date,
                                                         datetime.datetime.now().date()])
                                        print([self.product_name.strip(),
                                               self.product_image,
                                               self.payback_points,
                                               self.product_link,
                                               self.payback_condition,
                                               self.product_quantity,
                                               self.tag_label,
                                               self.price,
                                               self.product_information.strip(),
                                               self.store_address,
                                               self.STORE_NAME,
                                               self.category, self.from_to_date, datetime.datetime.now().date()])
        self.driver.quit()
