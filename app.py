import os
import pickle
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from gensim.models import Word2Vec
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD


# from IPython.display import Image, display, HTML



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
    if x == "OBST & GEMÜSE" or x == 'Obst und Gemüse' or x == 'Obst & Gemüse' or x == 'So lecker schmeckt pflanzlich':
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

    elif x == 'Haushalt' or x == 'Praktische Gartenprodukte'  or x == 'Cleveres Küchenzubehör' or x == 'Heim, Haus' or x == 'Putz- und Haushaltshelfer' or x == 'Haushalt & Wohnen' or x == 'Garten und Baumarkt' or x == 'Outdoor-Mode von Nangaparbat':
        return 'Haushalt  Heim, Haus'


    elif x == 'Topangebote' or x == 'Highlights der Woche'  or x == 'Genuss aus deiner Region' or x == 'Thema der Woche' or x == 'GRUNDNAHRUNG' or x == 'Unsere Knüller' or x == 'Europäische Spezialitäten zum Sparpreis' or x == 'Framstag' or x == 'Butcher´s by Penny' or x == 'Food-Highlights für alle' or x == 'Alles für den Grillabend' or x == 'Weitere Angebote' or x == 'Spart bei euren Lieblingsmarken' or x == '':
        return 'Topangebote'

    elif x == 'Freizeit & Mode' or x == 'Sport & Freizeit' or x == 'Bekleidung, Auto, Freizeit, Spiel' or x == 'Markenbekleidung für Kinder' or x == 'Bettwäsche, Pyjamas und mehr' or x == 'Bademode von Chiemsee':
        return 'Freizeit & Mode Sport  Bekleidung, Auto, Freizeit, Spiel'

    elif x == 'NON-FOOD' or x == 'Sprudeln mit Sodastream' or x == '':
        return 'weitere Produkte'

    elif x == 'Alkoholfreie' or x == 'Getränke, Spirituosen' or x == 'Kaffee, Tee, Süßwaren, Knabberartikel' or x == 'Alkoholfreie Getränke':
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


# @st.cache_data
# def load_df():
#     file_path = os.getcwd() + '/Merged All Offers/2023-07-17.csv'  # Path to the pickle file
#     data = pd.read_csv(os.getcwd() + '/Merged All Offers/2023-07-17.csv')
#     return data
#
#
# @st.cache_data
# def load_vectorizer():
#     file_path = 'tfidf_vectorizer.pkl'  # Path to the pickle file
#     with open(file_path, 'rb') as file:
#         tfidf_vectorizer = pickle.load(file)
#
#     return tfidf_vectorizer
#
#
# # NearestNeighbors
# @st.cache_data
# def load_nn():
#     nn = NearestNeighbors(metric='cosine', algorithm='brute')
#     return nn
#
#
# # nlp = spacy.load('en_core_web_sm')
# @st.cache_data
# def get_nlp():
#     return spacy.load('de_core_news_lg')


nlp = spacy.load('de_core_news_lg')
data = pd.read_csv(f'Merged All Offers/{datetime.now().date()}.csv')
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
data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
data_price_threshold = data.price.apply(lambda x: handle_price_threshold(x,data))
data['price_threshold'] = data_price_threshold
data.product_information = data.product_information.apply(lambda x: x.replace('\n', ' '))
data.product_quantity = data.product_quantity.apply(lambda x: x.replace('\n', ' '))

price_threshold_de = data.price_threshold.map(
    {"Cheaper Product": "Budget", "Expensive Product": "Premium", "Affordable Product": "Mittelklasse"})

data['price_threshold_de'] = price_threshold_de
data['text_preprocessed'] = data['product_name'] + ' ' + data['payback_points'] + ' ' + data['payback_condition'] + ' ' + data['product_quantity'] + ' ' + data['tag_label'] +  ' ' + data['product_information'] + ' ' + data['category'] + ' ' + data.price_threshold_de
data['text_preprocessed'] = data['text_preprocessed'].apply(lambda x: str(x).replace('\n', ' '))


tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['text_preprocessed'])
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf_vectorizer, f)


# svd = TruncatedSVD(n_components=100)
# reduced_matrix = svd.fit_transform(tfidf_matrix)


# # NearestNeighbors
# @st.cache_data
# def load_nn():
#     nn = NearestNeighbors(metric='cosine', algorithm='brute')
#     return nn


nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(tfidf_matrix)


def text_preprocessing(text):
    """Converting text into stemming """

    documents = nlp(text.lower())
    tokens = [each for each in documents]
    return ' '.join([each.lemma_ for each in tokens])


def get_recommendations(product_name, category, pricing, offer, store_address, top_n=20):
    query = product_name

    if category:
        query_category = ' '.join(category)
        query += query_category

    # query_preprocessed = product_name + ' ' + category + ' ' + offer + ' ' + pricing
    query_preprocessed = text_preprocessing(query)

    # Transform the query using the TF-IDF vectorizer
    query_vector = tfidf_vectorizer.transform([query_preprocessed])

    # reduced_matrix = svd.transform(query_vector)
    # Perform the nearest neighbor search
    _, indices = nn.kneighbors(query_vector, n_neighbors=top_n * 2)

    # Return the recommended product names

    # return data[['product_link','category_de','store']].iloc[indices[0]]
    recommended_products = data.iloc[indices[0]]



    # if category:
    #     recommended_products = recommended_products[recommended_products['category'].isin(category)]
    if store_address:
        recommended_products = recommended_products[recommended_products['store_address'].isin(store_address)]
    if len(recommended_products) == 0:
        st.warning("No products matching the filters.")
        return
    if not category:
        st.warning('Please select at least one Category.')
    if not store_address:
        st.warning('Please select at least one Store Address.')

    html_output = "<table>"
    # Track the seen product names
    seen_product_names = set()

    for index, row in recommended_products.iterrows():
        product_name = row['product_name']

        # Skip duplicate product names
        if product_name in seen_product_names:
            continue

        seen_product_names.add(product_name)

        html_output += "<tr>"
        html_output += f"<td><a href='{row['product_link']}' target='_blank'><img src='{row['product_image']}' style='width:150px;height:150px;'></a></td>"
        html_output += "<td>"
        html_output += f"<b>Product Name:</b> {product_name}<br>"
        html_output += f"<b>Price:</b> {row['price']}<br>"
        # html_output += f"<b>Brand:</b> {row['PRODUCT_BRAND']}<br>"

        # Retrieve the stores that carry the product
        stores = data[data['product_name'] == product_name]['store'].tolist()
        # html_output += f"<b>Stores:</b> {', '.join(stores)}<br>"

        html_output += f"<b>Product Quantity:</b> {row['product_quantity']}<br>"
        # html_output += f"<b>Nutritional Tags:</b> {row['nutritional_tags']}<br>"
        html_output += "</td>"
        html_output += "</tr>"

    html_output += "</table>"

    # Display the HTML output
    st.markdown(html_output, unsafe_allow_html=True)
    # return recommended_products


def show_page():
    st.title("Grocery Recommendation App")

    search_query = st.text_input("Search:")
    top_n = st.number_input("Number of recommendations:", min_value=1, max_value=20, value=5)
    selected_category = st.multiselect('Choose the category', ['OBST & GEMÜSE', 'Kühlung Molkereiprodukte, Fette KÄSE',
                                                               'Topangebote', 'Frühstück Kühlregal',
                                                               'Fleisch, Geflügel, Wurst Fisch',
                                                               'Wein & Spirituosen GETRÄNKE Leckere Cocktails für jeden Geschmack',
                                                               'KNABBERN & NASCHEN Knabberartikel',
                                                               'Drogerie, Tiernahrung Drogerie Tier',
                                                               'weitere Produkte',
                                                               'Pflanzen', 'Alkoholfreie Kaffee, Tee',
                                                               'Elektro, Büro, Medien',
                                                               'Haushalt  Heim, Haus',
                                                               'Freizeit & Mode Sport  Bekleidung, Auto, Freizeit, Spiel',
                                                               'Grillartikel zum Sparpreis', 'Cleveres Küchenzubehör',
                                                               'Bettwäsche, Pyjamas und mehr',
                                                               'Genuss aus deiner Region',
                                                               'Outdoor-Mode von Nangaparbat',
                                                               'Extra-Rabatte mit der Kaufland Card',
                                                               'Exklusive Angebote der Kaufland Card',
                                                               'Bademode von Chiemsee',
                                                               'PAYBACK Angebote', 'Mit der REWE App sparen',
                                                               'Kochen & Backen',
                                                               'Alkoholfreie Getränke'])
    selected_store = st.multiselect('Choose the nearby store', ['Penny,Dossenheimer Landstr. 40 69121 Heidelberg',
                                                                'Penny,Bahnhofstr. 9-13 69115 Heidelberg',
                                                                'Penny,Ploeck 13-21 69117 Heidelberg',
                                                                'Penny,Rathausstr. 27 69126 Heidelberg',
                                                                'Kaufland,Eppelheimer Straße 78, 69123 Heidelberg',
                                                                'Kaufland,Kurfürsten-Anlage 61, 69115 Heidelberg',
                                                                'Kaufland,Hertzstraße 1, 69126 Heidelberg-Rohrbach',
                                                                'Edeka,Kurfürstenanlage 21-23, 69115 Heidelberg',
                                                                'Edeka,Hauptstraße 198, 69117 Heidelberg',
                                                                'Edeka,In der Neckarhelle 1-3, 69118 Heidelberg-Ziegelhausen'
                                                                'REWE Sahin Karaaslan GmbH & Co. KG,Furtwanglerstr. 15, 69121 Heidelberg',
                                                                'REWE Markt GmbH,Im Franzosengewann 3, 69124 Heidelberg / Kirchheim',
                                                                'REWE Sahin Karaaslan GmbH & Co. KG,Berliner Str. 41-49, 69120 Heidelberg',
                                                                'REWE Markt GmbH,Kurfürstenanlage 6, 69115 Heidelberg/Weststadt',
                                                                'REWE Manuela Schrein oHG,Am Grünen Hag 2, 69118 Heidelberg',
                                                                'REWE Karaaslan oHG,Ladenburger Str. 68, 69120 Heidelberg/Neuenheim',
                                                                'REWE Markt GmbH,Im Weiher 14, 69121 Heidelberg/Handschuhsheim',
                                                                'REWE Markt GmbH,Grenzhöfer Weg 29, 69123 Heidelberg',
                                                                'REWE Markt GmbH,Felix-Wankel-Strasse 20, 69126 Heidelberg / Rohrbach'])

    pricing = st.selectbox("By Price Level (optional):", [None, "Budget", "Premium", "Mittelklasse"])
    offer = st.selectbox("By Offer Level (optional):",
                         [None, "Normales Angebot", "Moderates Angebot", "Blockbuster Angebot"])

    if st.button("Search"):
        get_recommendations(search_query, selected_category, pricing, offer, selected_store, top_n)


show_page()
