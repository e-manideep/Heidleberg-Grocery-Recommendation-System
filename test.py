# import os
# import time
#
# from selenium.webdriver import ActionChains
#
# print(os.listdir(f'{os.getcwd()}/Rewe page source/'))
#
# from store_details import rewe_store_address, rewe_urls
#
# street_names = [each.split(',')[1] for each in rewe_store_address]
# #
# # import os
# #
# # directory_path = "/path/to/directory"  # Replace with the actual directory path you want to check
# # for each in street_names:
# #     print(f'{os.getcwd()}/Rewe page source/'+ each.strip())
# #     if os.path.exists(f'{os.getcwd()}/Rewe page source/'+ each.strip()):
# #         print("The directory exists.")
# #     else:
# #         try:
# #             os.makedirs(f'{os.getcwd()}/Rewe page source/'+ each.strip())
# #             print("The directory has been created.")
# #         except OSError as e:
# #             print(f"An error occurred while creating the directory: {e}")
# # data = [each.split('?')[0] for each in rewe_urls]
# # print(data)
# # if "https://www.rewe.de/angebote/heidelberg/840442/rewe-markt-am-gruenen-hag-2/" in data:
# #     print(data.index("https://www.rewe.de/angebote/heidelberg/840442/rewe-markt-am-gruenen-hag-2/"))
# #     print('yes')
#
# #
# # a = ['SPECHT\nAspikspezialität\nje 100 g']
# #
# # print(a[0].split('\n')[:-1])
from selenium.common import NoSuchElementException, InvalidArgumentException, WebDriverException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import undetected_chromedriver as uc
#
# driver = uc.Chrome()
# driver.get('https://filiale.kaufland.de/angebote/aktuelle-woche/uebersicht.category=01_Fleisch__Gefl%C3%BCgel__Wurst.html')
# time.sleep(5)
# all_category_link = [each.get_attribute('href') for each in driver.find_elements(By.CSS_SELECTOR,'div#offers-overview-1 a.m-accordion__link')]
# print(all_category_link)
# for each in all_category_link:
#     driver.get(each)
# #     new_url = each.get_attribute('href')
# #     driver.find_element( By.TAG_NAME,'body').send_keys(Keys.CONTROL + 't')
# #
# #     # Switch to the new tab
# #     driver.switch_to.window(driver.window_handles[-1])
# #
# #     # Open a new website in the new tab
# #     driver.get(new_url)
# #     time.sleep(5)
#     # ActionChains(driver).move_to_element(each).perform()
#
#
# input('sdfjka')
# driver.quit()
#
import time

import requests
import undetected_chromedriver
from bs4 import BeautifulSoup
# from lxml import etree
# product_link  = 'https://www.penny.de/angebote/kuehlregal/laetta-halbfettmargarine'

# response = requests.get(product_link)
# print(response.status_code)

# with open('penny.html',encoding='utf-8') as file:
#     response = file.read()
# print(response)
# soup = BeautifulSoup(response,'html.parser')
# all_category = soup.find_element('h2')
# print(len(all_category))
#
#
# try:
#     product_name = soup.find('h1').text.strip()
# except AttributeError:
#     product_name = ''
#
# try:
#     price = soup.find('div',class_='bubble__wrap-inner').find_all('span')[-1].text.strip()
# except AttributeError:
#     price = ''
#
# try:
#     product_image = soup.find('li',id='offer-image-slide-0').img['src']
# except AttributeError:
#     product_image = ''
#
# try:
#     product_information = soup.find('div',class_='detail-block__body rich-text').text.strip()
# except AttributeError:
#     product_information = ''
#
#
# try:
#     tag_label = soup.find('div', class_='detail-block__badges badge__container').span.text
# except AttributeError:
#     tag_label = ''
#
#
# try:
#     product_quantity = soup.find('div',class_='detail-block__subline rich-text').p.text.strip()
# except AttributeError:
#     product_quantity = ''
#
# print(product_name)
# print(price)
# print(product_image)
# print(product_information)
# print(tag_label)
# print(product_quantity)
#


# driver.get(product_link)
# try:
#     product_name = driver.find_element(By.TAG_NAME,'h1').text.strip()
# except AttributeError:
#     product_name = ''
#
# try:
#     price = driver.find_elements(By.CSS_SELECTOR,'div.bubble__wrap-inner span')[-1].text.strip()
# except AttributeError:
#     price = ''
#
# try:
#     product_image = driver.find_elements(By.CSS_SELECTOR,'li#offer-image-slide-0').img['src']
# except AttributeError:
#     product_image = ''
#
# try:
#     product_information = driver.find_elements(By.CSS_SELECTOR,'div.detail-block__body rich-text').text.strip()
# except AttributeError:
#     product_information = ''
#
# try:
#     tag_label = driver.find_elements(By.CSS_SELECTOR,'div.detail-block__badges badge__container').span.text
# except AttributeError:
#     tag_label = ''
#
# try:
#     product_quantity = driver.find_elements(By.CSS_SELECTOR,'div.detail-block__subline.rich-text').p.text.strip()
# except AttributeError:
#     product_quantity = ''
#

# with open('penny.html',encoding='utf-8') as file:
#     data = file.read()
#

import pandas as pd
import datetime

from edeka_heidelberg import Edeka_Scraping
from kaufland_heidelberg import Kaufland
from store_details import *
from rewe_store import ScrapeRewe

# scrape_rewe = ScrapeRewe()
# scrape_rewe.URL = rewe_urls[0]
# scrape_rewe.handle_cookie_button()
# print(scrape_rewe.handle_change_product_url("7032776"))

# response = requests.get('https://shop.rewe.de/p/rewe-beste-wahl-buchen-grillholzkohle-2-5kg/8544640')
# soup = BeautifulSoup(response.content,'html.parser')
# print(soup.find('a',class_='lr-breadcrumbs__link lr-breadcrumbs__back'))

# data = pd.read_csv('Penny Product details/2023-07-06.csv')
# print(data.shape)
# data.product_link.drop_duplicates().to_csv('all_unique_penny_links.csv',index=False)
# data.product_link.drop_na
#
#
# print(data.shape)
# print(data.drop(index=data[data.product_link == 'product_link'].index, inplace=True))
# data.to_csv('all_unique_kaufland_links.csv')
#
# print(data.product_link.to_list())
# product_link = 'https://filiale.kaufland.de/angebote/aktuelle-woche/uebersicht/detail.so_id=00867035.html'


# data.drop(['Unnamed: 0.1', 'Unnamed: 0'],axis=1,inplace=True)
# data.to_csv('all_unique_penny_links.csv',index=False)

# response = requests.get('https://www.amazon.in/s?k=books+for+kids&crid=20EHPDK5FY7WS&sprefix=books+for+%2Caps%2C480&ref=nb_sb_noss_2',headers={
#     'User-Agents': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
# })
# print(response.status_code)
# soup = BeautifulSoup(response.content,'html.parser')
# print(soup.find_all('div',class_='sg-col-inner'))
# for address in kaufland_address:
#     pin_code = address.split(' ')[-2]
#     kaufland = Kaufland()
#     kaufland.store_pin_code = pin_code
#     kaufland.store_address = address
#     kaufland.init_scraping()

# for index, each in enumerate(rewe_urls):
#     store_address = rewe_store_address[index]
#     scrape_rewe = ScrapeRewe(each, store_address)
# page_source = ''
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, \
    InvalidArgumentException
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# service = Service(executable_path=r'chromedriver')
# chrome_options.add_argument("--window-size=1440, 900")
# chrome_options.add_argument('--start-maximized')
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(service=service, options=chrome_options)
# # self.driver = uc.Chrome(options=self.chrome_options)
# driver.get('https://shop.rewe.de/productList?search=106641')
# driver.implicitly_wait(10)
#
# print(driver.find_element(By.CSS_SELECTOR,'a.search-service-productDetailsLink.Product_productDetailsLink__hXXfb').get_attribute('href'))

import sys

with open('penny.html') as file:
    response = file.read()
soup = BeautifulSoup(response, 'html.parser')
payback_points = soup.find('div', class_="pdpr-ProductContent").text.encode('cp1252').decode('utf-8')



print(payback_points)

