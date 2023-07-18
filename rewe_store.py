import csv
import datetime as datetime

import pandas
import requests
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, \
    InvalidArgumentException
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

import time
import os
from store_details import rewe_store_address, rewe_urls

URL = 'https://www.rewe.de/angebote/heidelberg/831040/rewe-markt-grenzhoefer-weg-29'


class ScrapeRewe:
    def __init__(self, *args):
        self.wait = None

        self.current_page_url = ''
        self.start_time = datetime.datetime.now()
        self.COOKIE_BUTTON_CLICKED = False
        self.URL = args[0]
        self.product_name = ''
        self.product_image = ''
        self.payback_points = ''
        self.product_link = ''
        self.payback_condition = ''
        self.product_quantity = 'Keine Mengenangaben'
        self.tag_label = ''
        self.price = ''
        self.product_information = ''
        self.store = args[1]

        self.offer_number = ''
        self.offer_duration = ''
        self.content_category = ''
        self.STORE_NAME = 'Rewe'
        self.buttons = None
        self.chrome_options = uc.ChromeOptions()
        # self.chrome_options = Options()
        # service = Service(executable_path=r'chromedriver')
        self.chrome_options.add_argument("--window-size=1440, 900")
        self.chrome_options.add_argument('--start-maximized')
        # self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # self.chrome_options.add_experimental_option("useAutomationExtension", False)
        # self.chrome_options.add_argument(
        #     "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
        self.chrome_options.headless = True
        # self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        self.driver = uc.Chrome(options=self.chrome_options)
        self.driver.get(self.URL)
        
        self.wait = WebDriverWait(self.driver, 10)
        time.sleep(5)
        self.handle_cookie_button()
        self.page_source = None

    def handle_quit(self):
        self.driver.quit()

    def handle_cookie_button(self):

        while not self.COOKIE_BUTTON_CLICKED:
            time.sleep(4)
            try:
                clickable = self.wait.until(EC.element_to_be_clickable(
                    (By.ID, 'uc-btn-accept-banner')))
            except (NoSuchElementException, TimeoutException):
                print('NoSuchElementException')
            else:

                try:
                    clickable.click()
                except:
                    self.COOKIE_BUTTON_CLICKED = False
                else:
                    self.COOKIE_BUTTON_CLICKED = True
        self.handle_show_more_click()

    def handle_show_more_click(self):
        self.buttons = self.driver.find_elements(By.CLASS_NAME, 'sos-category__content-button')
        while self.buttons:
            for index, button in enumerate(self.buttons):
                time.sleep(5)
                try:
                    # Perform the desired action on the button
                    button.click()

                except ElementNotInteractableException:
                    print("Button not found or not interactable within the timeout period.", index)
                # if not self.COOKIE_BUTTON_CLICKED:
                #     self.handle_cookie_click()
            all_buttons = self.driver.find_elements(By.CLASS_NAME, 'sos-category__content-button')
            self.buttons = [button for button in all_buttons if 'block' in button.get_attribute('style')]
        time_taken = datetime.datetime.now() - self.start_time

        print(f'Time Taken', time_taken)
        self.page_source = self.driver.page_source
        self.scrape_from_page_source(self.page_source)

    def save_page_source(self, store_address):
        with open(f'Rewe page source/{store_address.split(",")[1].strip()}/{datetime.datetime.now().date()}.html', 'w',
                  encoding='utf-8') as f:
            f.write(self.page_source)

    def handle_change_product_url(self, offer_number):
        data = pandas.read_csv('product_information.csv', encoding='utf-8')
        if len(data[data.product_id == int(offer_number)]) < 1:
            each = 'https://shop.rewe.de/productList?search=' + offer_number
            try:
                self.driver.get(each)
            except InvalidArgumentException:
                self.product_link = each
            else:
                try:
                    self.product_link = self.driver.find_element(By.CSS_SELECTOR,
                                                                 'a.search-service-productDetailsLink.Product_productDetailsLink__hXXfb').get_attribute(
                        'href')
                except (AttributeError, NoSuchElementException, InvalidArgumentException, InvalidArgumentException):
                    self.product_link = 'https://www.rewe.de/suche/?search=' + offer_number + '&tab=products'
                else:
                    self.driver.get(self.product_link)
                    # time.sleep(1)
                    soup1 = BeautifulSoup(self.driver.page_source, 'html.parser')
                    try:
                        self.product_information = soup1.find('div', class_="pdpr-ProductContent").text
                    except AttributeError:
                        self.product_information = 'Keine Produktinformation'
                    # new_row = pandas.DataFrame( {'product_inforamtion': [product_info.encode('latin-1').decode(
                    # 'utf-8')], 'product_id': [int(offer_number)]})
                    else:
                        new_row = pandas.DataFrame(
                            {'product_information': [self.product_information],
                             'product_id': [int(offer_number)]})
                        data = pandas.concat([data, new_row], ignore_index=True)
                        data.drop_duplicates(inplace=True)
                        data.to_csv('product_information.csv', index=False)


        else:
            self.product_link = 'https://www.rewe.de/angebote/nationale-angebote/#' + offer_number
            self.product_information = data[data.product_id == int(offer_number)]['product_information'].values[0]

    def scrape_from_page_source(self, data):
        # all_stores_page_source = os.listdir(f'{os.getcwd()}/Rewe page source/')
        first_line = True

        # for store in all_stores_page_source:
        #
        #     self.store = store.strip()
        #     with open(f'{os.getcwd()}/Rewe page source/{store}/{datetime.datetime.now().date()}.html', 'r',
        #               encoding='utf-8') as file:
        #         data = file.read()

        soup = BeautifulSoup(data, 'html.parser')
        self.current_page_url = soup.find('meta', property='og:url')['content']
        data = [each.split('?')[0] for each in rewe_urls]
        self.URL = rewe_urls[data.index(self.current_page_url)]
        contents = soup.find_all('div', class_='sos-category__content')
        try:
            self.offer_duration = soup.find('h2', class_='sos-headings__duration').text

        except AttributeError:
            self.offer_duration = ''

        for content in contents:
            self.content_category = content.h2.text
            products = content.find_all('article')

            for product in products:

                try:
                    self.product_name = product.find('h3').text.strip()
                except AttributeError:
                    self.product_name = ''

                try:
                    self.product_image = product.find('img')['src']
                except AttributeError:
                    self.product_image = ''

                try:
                    self.payback_points = product.find('div', class_='cor-payback-points__badge-value').text.strip()
                except AttributeError:
                    self.payback_points = 'Keine Payback-Punkte'

                try:
                    self.payback_condition = product.find('div', class_='cor-payback-title').find_all('span')[
                        -1].text.strip()
                except AttributeError:
                    self.payback_condition = 'Keine Payback-Bedingung'

                try:
                    self.product_quantity = " ".join(
                        [each.text for each in
                         product.find_all('span', class_='cor-offer-information__additional')]).strip()
                except AttributeError:
                    self.product_quantity = 'Keine Mengenangaben'

                try:
                    self.tag_label = product.find('div', class_='cor-offer-price__tag-label').text.strip()
                except AttributeError:
                    self.tag_label = 'Kein Etikett'

                try:
                    self.price = product.find('div', class_='cor-offer-price__tag-price').text.strip()
                except AttributeError:
                    self.price = ''

                try:
                    self.offer_number = product.find('a', class_='cor-offer-information__title-link')[
                        'data-offer-nan']

                except (AttributeError, TypeError):
                    self.offer_number = ''
                    self.product_link = ''
                else:
                    self.handle_change_product_url(self.offer_number)

                with open(f'Rewe Product details/{datetime.datetime.now().date()}.csv', mode='a', newline='',
                          encoding='utf-8') as file:
                    writer = csv.writer(file)

                    if first_line:
                        writer.writerow(["product_name",
                                         "product_image",
                                         "payback_points",
                                         "product_link",
                                         "payback_condition",
                                         "product_quantity",
                                         "tag_label",
                                         "price",
                                         "product_information",
                                         "store_address", 'store', 'category', 'date', 'offer_duration'])
                        first_line = False

                    writer.writerow([self.product_name,
                                     self.product_image,
                                     self.payback_points,
                                     self.product_link,
                                     self.payback_condition,
                                     self.product_quantity,
                                     self.tag_label,
                                     self.price,
                                     self.product_information,
                                     ' '.join(self.store.split(',')[:]), self.STORE_NAME, self.content_category,
                                     datetime.datetime.now().date(), self.offer_duration])
                    print([self.product_name,
                           self.product_image,
                           self.payback_points,
                           self.product_link,
                           self.payback_condition,
                           self.product_quantity,
                           self.tag_label,
                           self.price,
                           self.product_information,
                           ' '.join(self.store.split(',')[:]), self.STORE_NAME, self.content_category,
                           datetime.datetime.now().date(), self.offer_duration])
                    # self.handle_change_product_url()
        self.driver.quit()
