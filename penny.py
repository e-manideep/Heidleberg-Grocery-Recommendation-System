import csv
import time
from datetime import datetime

import pandas
import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from store_details import penny_urls, penny_address

store = penny_address[0]
URL = penny_urls[0]


class Penny_Scraping:
    def __init__(self, *args):
        self.URL = args[0]
        self.STORE_NAME = "Penny"
        self.product_name = ''
        self.product_image = ''
        self.product_link = ''
        self.product_quantity = ''
        self.tag_label = ''
        self.price = ''
        self.product_information = 'Keine Produktinformation'
        self.store_address = args[1]
        self.payback_points = 'Keine Payback-Punkte'
        self.payback_condition = 'Keine Payback-Bedingung'
        self.category = ''
        self.offer_duration = ''
        self.chrome_options = uc.ChromeOptions()
        # self.chrome_options = Options()
        # service = Service(executable_path=r'chromedriver')
        self.chrome_options.headless = True
        self.chrome_options.add_argument("--window-size=1440, 900")
        self.chrome_options.add_argument('--start-maximized')
        self.driver = uc.Chrome(options=self.chrome_options)


        # self.driver = webdriver.Chrome(service=service,options=self.chrome_options)
        self.driver.get(self.URL)
        self.wait = WebDriverWait(self.driver, 10)
        self.cookie_button_clicked = False
        self.first_line = True

    def init_scraping(self):
        time.sleep(5)
        while not self.cookie_button_clicked:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, '#usercentrics-root').shadow_root
                cookie_button = element.find_element(By.CSS_SELECTOR, 'button.sc-eDvSVe.MQFyp')

            except (NoSuchElementException, TimeoutException):
                print('NoSuchElementException, TimeoutException')

            else:
                self.cookie_button_clicked = True
                cookie_button.click()
        self.handle_store_button_click()

    def handle_store_button_click(self):

        try:
            button = self.driver.find_element(By.CSS_SELECTOR,
                                              'div.market-tile__links a.btn.btn--outlined.t-color--red-penny.market-tile__btn-offers')
        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
            print('couldn\'t find the button')

        else:
            button.click()
            self.start_to_scrape()

    def scrape_product_information(self, response):

        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            self.product_name = soup.find('h1').text.strip()
        except (AttributeError,TypeError):
            self.product_name = ''

        try:
            self.price = soup.find('div', class_='bubble__wrap-inner').find_all('span')[
                -1].text.strip()
        except AttributeError:
            self.price = 0
        try:
            self.payback_points = soup.find('button',class_='tooltip-dialog__btn').text.strip()
        except AttributeError:
            self.payback_points = 'Keine Payback-Punkte'



        try:
            self.product_image = soup.find('img')['src']
        except (AttributeError,TypeError):
            self.product_image = ''

        try:
            self.product_information = soup.find('div',
                                                 class_='detail-block__body rich-text').text.strip()
        except AttributeError:
            self.product_information = 'Keine Produktinformation'

        try:
            self.tag_label = soup.find('div',
                                       class_='detail-block__badges badge__container').span.text
        except AttributeError:
            self.tag_label = 'Kein Etikett'

        try:
            self.product_quantity = soup.find('div',
                                              class_='detail-block__subline rich-text').p.text.strip()
        except AttributeError:
            self.product_quantity = 'Keine Mengenangaben'

    def start_to_scrape(self):
        scroll_speed = 100
        page_height = self.driver.execute_script("return document.body.scrollHeight")

        for scroll in range(0, page_height, scroll_speed):
            self.driver.execute_script(f"window.scrollTo(0, {scroll});")
            time.sleep(0.01)
        try:

            all_sections = self.driver.find_elements(By.CSS_SELECTOR, 'section.js-category-section')
        except AttributeError:
            all_sections = ''
        else:
            for each in all_sections:

                try:
                    self.category = each.find_element(By.TAG_NAME, 'h3').text
                except AttributeError:
                    self.category = ''
                try:
                    self.offer_duration = self.driver.find_element(By.CSS_SELECTOR,
                                                                   '.category-menu__header-week.active').get_attribute(
                        'data-startend')
                except AttributeError:
                    self.offer_duration = ''
                try:
                    products = each.find_elements(By.CSS_SELECTOR, 'div.l-container li')
                except:
                    products = ''
                else:
                    for product in products:
                        try:
                            self.product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        except NoSuchElementException:
                            self.product_link = ''
                        else:
                            data = pandas.read_csv('all_unique_penny_links.csv')

                            if (len(data[data.product_link == self.product_link])) < 1:
                                new_data = pandas.DataFrame({'product_link': [self.product_link]})
                                data = pandas.concat([data, new_data], axis=0, ignore_index=True)
                                data.to_csv('all_unique_penny_links.csv', index=False)

                            try:
                                response = requests.get(self.product_link)
                            except requests.exceptions.ConnectionError:
                                print('lost one product')
                            else:
                                self.scrape_product_information(response)

                                with open(f'Penny Product details/{datetime.now().date()}.csv', mode='a', newline='',
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
                                                         "store_address", 'store', 'category', 'date',
                                                         'offer_duration'])
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
                                                     self.category, datetime.now().date(), self.offer_duration])
                                    print([self.product_name.strip(),
                                           self.product_image,
                                           self.payback_points,
                                           self.product_link,
                                           self.payback_condition,
                                           self.product_quantity,
                                           self.tag_label,
                                           self.price,
                                           self.product_information.encode('utf-8',errors='replace').decode('cp1252',errors='replace').strip(),
                                           self.store_address,
                                           self.STORE_NAME,
                                           self.category, datetime.now().date(), self.offer_duration])
        self.driver.quit()
