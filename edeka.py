# data manipulation
import pandas as pd

# mathematical computations
import numpy as np

# scrapping data
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

# data visualization
# import matplotlib.pyplot as plt
# import seaborn as sns



# Set up Selenium webdriver 
driver = webdriver.Chrome()
from selenium.webdriver.common.by import By

# Maximize the window
driver.maximize_window()

# page url
url = 'https://www-edeka-de.translate.goog/eh/s%C3%BCdwest/scheck-in-center-kurf%C3%BCrstenanlage-21-23/angebote.jsp?lang=en&_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en-US&_x_tr_pto=wapp&_x_tr_hist=true'

response = requests.get(url)
new_url = 'https://www.edeka.de/eh/s%C3%BCdwest/scheck-in-center-kurf%C3%BCrstenanlage-21-23/angebote.jsp'

new_response = requests.get(new_url)
print(new_response.status_code)
print(response.status_code)
print(response.cookies)
# load page
driver.get(url)

# instantiate beautifulsoup object
soup = BeautifulSoup(new_response.text, "html.parser")

# get all item categories
category_container = soup.find_all('div', {'class':'css-10didr4'})
len(category_container)

# first category
fruits_vegetables = category_container[0]

# items in fruits_vegetables
fruits_container = fruits_vegetables.find_all('div',{'class':'has-size-s css-1olgk07'})
len(fruits_container)

# first item 
first_fruit = fruits_container[0]

#image url
first_fruit_img = first_fruit.find('div',{'class':'css-tbgtq2'}).find('div',{'class':'css-tappbf'}).span.img['srcset']

#item price
first_fruit_price = first_fruit.find('div',{'class':'css-upq47'}).span.text

#item name
first_fruit_name = first_fruit.find('div',{'class':'css-6su6cu'}).span.text
print(first_fruit_name)
# item description
first_fruit_decsription = first_fruit.find('div',{'class':'css-6su6cu'}).p.text

# unit price
first_fruit.find('div',{'class':'css-1gdm77d'}).span.text

for category in category_container:
    items = category.find_all('div', {'class': 'has-size-s css-1olgk07'})

    for item in items:
        try:
            Product_price = item.find('div', {'class': 'css-upq47'}).span.text
        except: Product_price = np.nan
        print(Product_price)

# putting it all together
# create empty list
data = []

# loop over categories
for category in category_container:
    items = category.find_all('div', {'class': 'has-size-s css-1olgk07'})

    # loop through each item
    for item in items:
        try:
            Product_price = item.find('div', {'class': 'css-upq47'}).span.text
            Product_name = item.find('div',{'class':'css-6su6cu'}).span.text
            Product_description = item.find('div', {'class': 'css-6su6cu'}).p.text
            Product_unit_price = item.find('div', {'class': 'css-1gdm77d'}).span.text
        except:
            Product_unit_price = np.nan
            Product_name = np.nan
            Product_description = np.nan
            Product_unit_price = np.nan
        
        data.append({
            'Product_price': Product_price,
            'Product_name': Product_name,
            'Product_description': Product_description,
            'Product_unit_price': Product_unit_price
        })



df = pd.DataFrame(data)
df.shape
df.head()
df.to_csv('edeka_data.csv',index=False)

# # load the page
# html_page = requests.get(url)

# # confirm access granted
# print(html_page.status_code)

# # get page content
# soup = BeautifulSoup(html_page.content,'html.parser')

# category_container = soup.find_all('div',{'class':'css-10didr4'})



