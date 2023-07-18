import pandas as pd
import numpy as np
import spacy


def handle_category_cleaning(x):
    if x == "OBST & GEMÜSE" or x == 'Obst und Gemüse' or x == 'Obst & Gemüse' or x == 'Obst, Gemüse, Pflanzen' or x == 'Pflanzen':
        return 'Fruits, vegetables, plants'

    elif x == 'KNABBERN & NASCHEN' or x == 'Süßigkeiten & Snacks' or x == 'Süßes & Salziges' or x == 'Kaffee, Tee, Süßwaren, Knabberartikel' or x == 'SONSTIGES' or x == 'Feinkost, Konserven' or x == 'Grundnahrungsmittel':
        return 'Coffee, tea, confectionery, snacks'

    elif x == 'Fleisch, Geflügel, Wurst' or x == 'Fisch' or x == 'FLEISCH & WURST' or x == 'Frische & Convenience' or x == 'FISCH & MEERESFRÜCHTE' or x == 'Fleisch und Wurst':
        return 'Meat, poultry, sausage & Fish'

    elif x == 'GETRÄNKE' or x == 'Getränke' or x == 'Alkoholfreie Getränke' or x == 'Bier' or x == 'Wein & Spirituosen' or x == 'Leckere Cocktails für jeden Geschmack' or x == 'Getränke, Spirituosen':
        return 'Beverages, spirits'

    elif x == 'Drogerie, Tiernahrung' or x == 'Drogerie' or x == 'Tier' or x == 'DROGERIE' or x == 'TIERNAHRUNG' or x == 'Drogerie & Haushalt' or x == '':
        return 'Drugstore and Pet Food'


    elif x == 'Frühstück' or x == 'Tiefkühl' or x == 'TIEFKÜHL' or x == 'Kühlregal' or x == 'Tiefkühlkost':
        return 'Frozen'

    elif x == 'Kochen & Backen' or x == '' or x == '' or x == '':
        return 'Cooking and Baking'

    elif x == 'Kühlung' or x == 'Molkereiprodukte, Fette' or x == 'MOLKEREI & KÄSE' or x == '':
        return 'Dairy'

    elif x == 'Haushalt' or x == 'Praktische Gartenprodukte' or x == 'Heim, Haus' or x == 'Putz- und Haushaltshelfer' or x == 'Haushalt & Wohnen':
        return 'HouseHold'


    elif x == 'Topangebote' or x == 'Highlights der Woche' or x == 'GRUNDNAHRUNG' or x == 'Unsere Knüller' or x == 'Europäische Spezialitäten zum Sparpreis' or x == 'Framstag' or x == 'Butcher´s by Penny' or x == 'Food-Highlights für alle' or x == 'Alles für den Grillabend' or x == 'Weitere Angebote' or x == 'Spart bei euren Lieblingsmarken':
        return 'Top Offers'

    elif x == 'Freizeit & Mode' or x == 'Sport & Freizeit' or x == 'Bekleidung, Auto, Freizeit, Spiel' or x == 'Markenbekleidung für Kinder':
        return 'Leisure, Sports & Fashion'

    elif x == 'Kinderwelt' or x == '' or x == '' or x == '':
        return 'Kids World'

    elif x == 'Elektro, Büro, Medien' or x == '' or x == '' or x == '':
        return 'Electronics, Office and Media'

    elif x == 'NON-FOOD' or x == 'Sprudeln mit Sodastream' or x == '':
        return 'Others'
    else:
        return x


def handle_price_clean(x):
    x = str(x)
    try:
        return float(x.replace('*', '').replace(' ', '').replace('€', '').replace(',', '.').replace('.–', ''))
    except:
        return 0


def handle_price_threshold(x):
    if x < data.price.quantile(0.25):
        return 'Cheaper Product'
    elif data.price.quantile(0.25) <= x <= data.price.quantile(0.50):
        return 'Affordable Product'
    else:
        return 'Expensive Product'


# nlp = spacy.load('en_core_web_sm')
nlp = spacy.load('de_core_news_sm')


def text_preprocessing(text):
    '''Converting text into stemming '''

    documents = nlp(text.lower())
    tokens = [each for each in documents]
    return ' '.join([each.lemma_ for each in tokens])


data = pd.read_csv(f'Merged All Offers/2023-07-12.csv')

data.drop(index=data[data.category == 'category'].index, inplace=True)
data.drop(index=data[data['product_name'].isna()].index, inplace=True)

data.product_information = data.product_information.fillna('No Product Information')
data.product_quantity = data.product_quantity.fillna('No Product Quantity')
data.price = data.price.fillna(0)
if data.product_link.isna().sum() < 10:
    data.dropna(axis=0, subset=['product_link'], inplace=True)
data.drop_duplicates(inplace=True)
data = data[(data.category != 'PAYBACK Punkte Highlights') & (data.category != 'Dein Markt für italienischen Genuss')]

data.category = data.category.apply(handle_category_cleaning)
data.price = data.price.apply(handle_price_clean)
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
data.price_threshold = data.price.apply(handle_price_threshold)
data.product_information = data.product_information.apply(lambda x: x.replace('\n', ' '))
data.product_quantity = data.product_quantity.apply(lambda x: x.replace('\n', ' '))
data.offer_duration = data.offer_duration.apply(lambda x: x.strip())
data.tag_label = data.tag_label.apply(lambda x: x.strip())

data['text_preprocessed'] = data['product_name'] + ' ' + data['payback_points'] + ' ' + data[
    'payback_condition'] + ' ' + data['product_quantity'] + ' ' + data['tag_label'] + ' ' + data[
                                'product_information'] + ' ' + data['category'] + ' ' + data.price_threshold
data['text_preprocessed'] = data['text_preprocessed'].apply(lambda x: x.replace('\n', ' '))
data['text_preprocessed'] = data['text_preprocessed'].apply(text_preprocessing)
data.to_csv(f'Merged All Offers/2023-07-12.csv',index=False)