import time
from datetime import datetime, timedelta

import os

import pandas
import spacy

from edeka_heidelberg import Edeka_Scraping
from kaufland_heidelberg import Kaufland
from penny import Penny_Scraping
from rewe_store import ScrapeRewe
from store_details import rewe_store_address, rewe_urls, edeka_url, edeka_address, penny_urls, penny_address, \
    kaufland_address


nlp = spacy.load('de_core_news_lg')

def handle_price_threshold(x,data):

    if x > 0:
        if x < data.price.quantile(0.25):
            return 'Cheaper Product'
        elif x >= data.price.quantile(0.25) and x <= data.price.quantile(0.50):
            return 'Affordable Product'
        else:
            return 'Expensive Product'
    else:
        return 'Recipe'


def text_preprocessing(text):
    """Converting text into stemming """

    documents = nlp(text.lower())
    tokens = [each for each in documents]
    return ' '.join([each.lemma_ for each in tokens])


def handle_tag_label(x):
    x = x.replace('-', '').replace('%', '')
    try:
        x = float(x)
    except:
        return x
    else:
        if x < 25:
            return 'Normales Angebot'
        elif x >= 25 and x <= 50:
            return 'moderates Angebot'
        else:
            return 'Blockbuster Angebot'


def handle_category_cleaning(x):
    if x == "OBST & GEMÜSE" or x == 'Obst und Gemüse' or x == 'Obst & Gemüse':
        return 'OBST & GEMÜSE'

    elif x == 'Pflanzen' or x == 'Obst, Gemüse, Pflanzen':
        return 'Pflanzen'

    elif x == 'KNABBERN & NASCHEN' or x == 'Süßigkeiten & Snacks' or x == 'Süßes & Salziges' or x == 'SONSTIGES' or x == 'Feinkost, Konserven' or x == 'Grundnahrungsmittel':
        return 'KNABBERN & NASCHEN Knabberartikel'

    elif x == 'Fleisch, Geflügel, Wurst' or x == 'Fisch' or x == 'FLEISCH & WURST' or x == 'Frische & Convenience' or x == 'FISCH & MEERESFRÜCHTE' or x == 'Fleisch und Wurst':
        return 'Fleisch, Geflügel, Wurst Fisch'

    elif x == 'GETRÄNKE' or x == 'Getränke' or x == 'Bier' or x == 'Wein & Spirituosen' or x == 'Leckere Cocktails für jeden Geschmack':
        return 'Wein & Spirituosen GETRÄNKE Leckere Cocktails für jeden Geschmack'

    elif x == 'Drogerie, Tiernahrung' or x == 'Drogerie' or x == 'Tier' or x == 'DROGERIE' or x == 'TIERNAHRUNG' or x == 'Drogerie & Haushalt' or x == '':
        return 'Drogerie, Tiernahrung Drogerie Tier'


    elif x == 'Frühstück' or x == 'Tiefkühl' or x == 'TIEFKÜHL' or x == 'Kühlregal' or x == 'Tiefkühlkost':
        return 'Frühstück Kühlregal'



    elif x == 'Kühlung' or x == 'Molkereiprodukte, Fette' or x == 'MOLKEREI & KÄSE':
        return 'Kühlung Molkereiprodukte, Fette KÄSE'

    elif x == 'Haushalt' or x == 'Praktische Gartenprodukte' or x == 'Heim, Haus' or x == 'Putz- und Haushaltshelfer' or x == 'Haushalt & Wohnen':
        return 'Haushalt  Heim, Haus'


    elif x == 'Topangebote' or x == 'Highlights der Woche' or x == 'GRUNDNAHRUNG' or x == 'Unsere Knüller' or x == 'Europäische Spezialitäten zum Sparpreis' or x == 'Framstag' or x == 'Butcher´s by Penny' or x == 'Food-Highlights für alle' or x == 'Alles für den Grillabend' or x == 'Weitere Angebote' or x == 'Spart bei euren Lieblingsmarken':
        return 'Topangebote'

    elif x == 'Freizeit & Mode' or x == 'Sport & Freizeit' or x == 'Bekleidung, Auto, Freizeit, Spiel' or x == 'Markenbekleidung für Kinder':
        return 'Freizeit & Mode Sport  Bekleidung, Auto, Freizeit, Spiel'

    elif x == 'NON-FOOD' or x == 'Sprudeln mit Sodastream' or x == '':
        return 'weitere Produkte'

    elif x == 'Alkoholfreie' or x == 'Getränke, Spirituosen' or x == 'Kaffee, Tee, Süßwaren, Knabberartikel':
        return 'Alkoholfreie Kaffee, Tee'
    elif x == 'extra-rabatte mit der Kaufland Card':
        return 'exklusiv Angebot der Kaufland Card'
    else:
        return x


def handle_price_clean(x):
    x = str(x)
    try:
        return float(x.replace('*', '').replace(' ', '').replace('€', '').replace(',', '.').replace('.–', ''))
    except:
        return 0


if f'text_preprocessed_{datetime.now().date()}.csv' not in os.listdir(os.getcwd()):
    print('yes')


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
    data = pandas.read_csv(f'Merged All Offers/{datetime.now().date()}.csv')
    data.drop(index=data[data.category == 'category'].index, inplace=True)
    data.drop(index=data[data['product_name'].isna()].index, inplace=True)

    data.product_information = data.product_information.fillna('No Product Information')
    data.product_quantity = data.product_quantity.fillna('No Product Quantity')
    data.price = data.price.fillna(0)
    data.offer_duration = data.offer_duration.apply(lambda x: x.strip())
    data.tag_label = data.tag_label.apply(lambda x: x.strip())

    data.dropna(axis=0, subset=['product_link'], inplace=True)
    data.drop_duplicates(inplace=True)

    data = data[
        (data.category != 'PAYBACK Punkte Highlights') & (data.category != 'Dein Markt für italienischen Genuss')]
    data.category = data.category.apply(handle_category_cleaning)
    data.tag_label = data.tag_label.apply(handle_tag_label)
    data.price = data.price.apply(handle_price_clean)
    data['date'] = pandas.to_datetime(data['date'], format='%Y-%m-%d')
    data_price_threshold = data.price.apply(lambda x: handle_price_threshold(x,data))
    data['price_threshold'] = data_price_threshold
    data.product_information = data.product_information.apply(lambda x: x.replace('\n', ' '))
    data.product_quantity = data.product_quantity.apply(lambda x: x.replace('\n', ' '))

    price_threshold_de = data.price_threshold.map(
        {"Cheaper Product": "Budget", "Expensive Product": "Premium", "Affordable Product": "Mittelklasse"})

    data['price_threshold_de'] = price_threshold_de
    data['text_preprocessed'] = data['product_name'] + ' ' + data['payback_points'] + ' ' + data['payback_condition'] + ' ' + data['product_quantity'] + ' ' + data['tag_label'] +  ' ' + data['product_information'] + ' ' + data['category'] + ' ' + data.price_threshold_de
    data['text_preprocessed'] = data['text_preprocessed'].apply(lambda x: str(x).replace('\n', ' '))
    print(data['text_preprocessed'].isna().sum())
    print(data.isnull().sum())
    if f'text_preprocessed_{datetime.now().date()}.csv' not in os.listdir(os.getcwd()):
        data.to_csv(f'text_preprocessed_{datetime.now().date()}.csv', index=False,encoding='latin-1')


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
