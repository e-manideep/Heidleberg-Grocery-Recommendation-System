import time
from datetime import datetime, timedelta

import os

import pandas

from edeka_heidelberg import Edeka_Scraping
from kaufland_heidelberg import Kaufland
from penny import Penny_Scraping
from rewe_store import ScrapeRewe
from store_details import rewe_store_address, rewe_urls, edeka_url, edeka_address, penny_urls, penny_address, \
    kaufland_address


def scrape_all_store_offers():
    while f'{datetime.now().date()}.csv' not in os.listdir(os.getcwd() + '/Merged All Offers/'):
        if f'{datetime.now().date()}.csv' not in os.listdir(os.getcwd() + '/Kaufland/'):

            for address in kaufland_address:
                pin_code = address.split(' ')[-2]
                kaufland = Kaufland(pin_code, address)

                kaufland.init_scraping()

        time.sleep(5)
        if f'{datetime.now().date()}.csv' not in os.listdir(os.getcwd() + '/Rewe Product details/'):

            scrape_rewe = ''
            for index, each in enumerate(rewe_urls):
                store_address = rewe_store_address[index]

                scrape_rewe = ScrapeRewe(each, store_address)

        time.sleep(5)
        if f'{datetime.now().date()}.csv' not in os.listdir(os.getcwd() + '/Edeka Product details/'):
            for index, each_link in enumerate(edeka_url):
                Edeka_Scraping(edeka_address[index], each_link)

        time.sleep(5)

        if f'{datetime.now().date()}.csv' not in os.listdir(os.getcwd() + '/Penny Product details/'):

            for index, each_url in enumerate(penny_urls):
                penny = Penny_Scraping(each_url, penny_address[index])
                penny.init_scraping()

        try:
            merge_all_store_csv()
        except:
            print('not merged.')


def merge_all_store_csv():
    folder_to_open = ['Edeka Product details', 'Kaufland', 'Penny Product details', 'Rewe Product details']
    all_variables = []
    for index, each in enumerate(folder_to_open):
        globals()[f"data{index}"] = pandas.read_csv(f"{each}/{datetime.now().date()}.csv")
        all_variables.append(globals()[f'data{index}'])

    data = pandas.concat(all_variables, ignore_index=True)
    data.to_csv(f'Merged All Offers/{datetime.now().date()}.csv', index=False)


start_time = datetime.now()
scrape_all_store_offers()

# merge_all_store_csv()

print(datetime.now() - start_time)
# scrape_rewe = ScrapeRewe(rewe_urls[1], rewe_store_address[1].split(',')[1])
# scrape_rewe.handle_cookie_button()
# scrape_rewe.scrape_from_page_source()
# scrape_rewe.driver.quit()
