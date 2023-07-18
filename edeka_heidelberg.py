import csv
import time
from datetime import datetime

import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Edeka_Scraping:
    def __init__(self, store, store_link):
        # self.chrome_options = uc.ChromeOptions()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--window-size=1440, 900")
        self.chrome_options.add_argument('--start-maximized')
        service = Service(executable_path=r'chromedriver')
        # self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        self.chrome_options.headless = True
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        # self.driver = uc.Chrome(options=self.chrome_options)
        self.store_address = store
        self.payback_points = 'Keine Payback-Punkte'
        self.payback_condition = 'Keine Payback-Bedingung'
        self.first_line = True
        self.product_name = ''
        self.product_image = ''
        self.product_link = store_link
        self.product_quantity = ''
        self.tag_label = ''
        self.price = ''
        self.product_information = 'Keine Produktinformation'
        self.offer_duration = ''
        self.STORE_NAME = 'EDEKA'
        self.category = ''
        self.driver.get(store_link)
        time.sleep(5)
        self.wait = WebDriverWait(self.driver, 10)
        self.cookie_button_click()
        self.driver.quit()

    def cookie_button_click(self):
        try:
            cookie_button = self.wait.until(EC.element_to_be_clickable((By.ID, 'popin_tc_privacy_button')))
        except (NoSuchElementException, TimeoutException):
            print('error')
        else:
            cookie_button.click()
        self.handle_scraping()

    def handle_scraping(self):

        try:
            all_offers_click = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.css-qtdpxz')))
        except (NoSuchElementException, TimeoutException):
            print('all button_erorr')
        else:
            self.driver.get(all_offers_click.get_attribute('href'))
            scroll_speed = 100
            time.sleep(5)
            scroll_height = self.driver.execute_script('return document.body.scrollHeight')
            for scroll in range(0, scroll_height, scroll_speed):
                self.driver.execute_script(f'window.scrollTo(0,{scroll})')
                time.sleep(0.01)

            try:
                time.sleep(5)
                all_section = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid=teaserwall-headline-section]')
            except (NoSuchElementException, TimeoutException):
                print('NO SUch element')
            else:
                for each_section in all_section:
                    each_section = each_section.find_element(By.CSS_SELECTOR, '.css-79elbk')

                    try:
                        self.category = each_section.find_element(By.CSS_SELECTOR, 'h2.css-8amn6y').text

                    except (NoSuchElementException, TimeoutException):
                        self.category = ''

                    try:
                        all_products = each_section.find_elements(By.CSS_SELECTOR, '.has-size-s.css-1olgk07')

                    except (NoSuchElementException, TimeoutException):
                        print('NO SUch element')
                    else:
                        for each_product in all_products:
                            try:
                                self.price = each_product.find_element(By.CSS_SELECTOR, 'div.css-upq47 span').text
                            except NoSuchElementException:
                                self.price = ''
                            try:
                                self.product_name = each_product.find_element(By.CSS_SELECTOR,
                                                                              'div.css-6su6cu span').text
                            except NoSuchElementException:
                                self.product_name = ''
                            try:
                                self.product_quantity = each_product.find_element(By.CSS_SELECTOR,
                                                                                  'div.css-6su6cu p').text
                            except NoSuchElementException:
                                self.product_quantity = 'Keine Mengenangaben'
                            try:
                                self.tag_label = each_product.find_element(By.CSS_SELECTOR, 'div.css-1ytub8b span').text
                            except NoSuchElementException:
                                self.tag_label = 'Kein Etikett'
                            try:
                                self.offer_duration = each_product.find_element(By.XPATH,
                                                                                '//*[@id="__next"]/div/div[7]/div/div/div/div[1]/ul/li[1]/div').text
                            except NoSuchElementException:
                                self.offer_duration = 'Keine Angebotsdauer'
                            try:
                                self.product_image = each_product.find_element(By.CSS_SELECTOR,
                                                                               'div.css-tappbf img').get_attribute(
                                    'src')
                            except NoSuchElementException:
                                self.product_image = ''
                            with open(f'Edeka Product details/{datetime.now().date()}.csv', mode='a', newline='',
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
                                                     "store_address", 'store', 'category', 'date', 'offer_duration'])
                                    self.first_line = False

                                writer.writerow([self.product_name.strip(),
                                                 self.product_image,
                                                 self.payback_points,
                                                 "/".join(self.product_link.split('/')[:-1]) + '/angebote.jsp',
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
                                       "/".join(self.product_link.split('/')[:-1]) + '/angebote.jsp',
                                       self.payback_condition,
                                       self.product_quantity,
                                       self.tag_label,
                                       self.price,
                                       self.product_information.strip(),
                                       self.store_address,
                                       self.STORE_NAME,
                                       self.category, datetime.now().date(), self.offer_duration])
