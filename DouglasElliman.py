# Copyright (C) 2019 Chaoyue Zheng. All rights reserved.
'''
this is the first part of model --- data scraping
https://www.elliman.com
code is used to scrape all houses in Manhattan for sale
'''

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np


def pages(url):
    '''
    :param url: str; thr url for the first page of Manhattan sale houses
    'https://www.elliman.com/search/for-sale/search-1?sdid=1&sid=40355790&sk=1'
    :return: int; the page numbers for all Manhattan sale houses
    '''

    response = requests.get(url)
    if response.status_code != 200:
        return None
    # use bs4 to get results_page
    results_page = BeautifulSoup(response.content, 'lxml')
    list_ = []
    num = results_page.find('div', class_='w_description')
    for i in num.find_all('strong'):
        list_.append(str(i.get_text()))
    pages = int(int(list_[2].split()[0].replace(',', '')) / int(list_[1]))

    return pages


def get_house_info(url):
    '''
    :param url: each page url for Manhattan sale houses; the page number is shown in pages definition
    :return: house_url_l, house_name, image_housing_urls, house_price, house_extras, house_features, house_id, house_sq
    '''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/11.1.2 Safari/605.1.15',
        'Cookie': cookie}
    response = requests.get(url, headers=headers)

    try:
        if response.status_code == 200:
            results_page = BeautifulSoup(response.content, 'lxml')
            # base url
            base = "https://www.elliman.com"
            house_url_l = []
            house_name = []
            house_price = []
            house_extras = []
            house_features = []
            house_id = []
            house_sq = []
            image_url = []
            image_housing_urls = []

            try:
                for i in results_page.find_all('li', class_='listing_address first'):
                    house = i.find('a').get('href')
                    house_url = base + house
                    name = i.find('a').get_text()

                    # save all url into a list
                    house_url_l.append(house_url)
                    house_name.append(str(name))
            except:
                print('cannot find url and house name')

            # find house_price
            try:
                for i in results_page.find_all('li', class_="listing_price"):
                    try:
                        price = i.get_text()
                        price = price.replace('\n', '')
                        house_price.append(price)
                    except:
                        house_price.append('NaN')
            except:
                print('this page has no price')

            # find listing_extras
            try:
                for i in results_page.find_all('li', class_="listing_extras"):
                    try:
                        extras = i.get_text()
                        house_extras.append(extras)
                    except:
                        house_extras.append('no extras')

            except:
                print('this page has no extras')

            # find house_features
            try:
                for i in results_page.find_all('li', class_="listing_features"):
                    try:
                        features = i.get_text()
                        house_features.append(features)
                    except:
                        house_features.append('NaN')

            except:
                print('this page has no features')

            # find last listing_id
            try:
                for i in results_page.find_all('li', class_="last listing_id"):
                    try:
                        id_ = i.get_text()
                        id_ = id_.replace('Listing ID: ', '')
                        house_id.append(id_)
                    except:
                        house_id.append('NaN')
            except:
                print('this page has no id')

            # find appro sq:
            try:
                for i in results_page.find_all('div', class_='w_listitem_description'):
                    if i.find('li', class_=None) is not None:
                        a = i.find('li', class_=None)
                        house_sq.append(a.get_text())
                    else:
                        house_sq.append('NaN')

            except:
                print('this page has no description.')

            # find images
            try:
                for i in results_page.find_all('div', class_="w_listitem_utilities"):

                    a = i.find('a', class_='w_listitem_quickview')
                    try:
                        image_url.append(base + a.get('href').replace('#', ''))

                    except:
                        image_url.append('NaN')

                for i in image_url:
                    try:
                        image_housing_urls.append(image_urls(i))
                    except:
                        print('no images')
                        image_housing_urls.append('NaN')
            except:
                print("cannot find this page's image urls")

            return house_url_l, house_name, image_housing_urls, house_price, house_extras, house_features, house_id, house_sq

    except:
        print('somthing wrong')


def get_article(url):
    '''
    :param url: each house's url, get from get_house_info(url)
    :return: house's articles
    '''
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/11.1.2 Safari/605.1.15',
            'Cookie': Cookie}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            results_page = BeautifulSoup(response.content, 'lxml')
            results = results_page.find('div', class_='w_listitem_copy')
            article = results.find('p', class_=None).get_text()

        return article

    except:
        print('No articles')


def image_urls(url):
    '''
    :param url: each house's url, get from get_house_info(url)
    :return: house's articles
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/11.1.2 Safari/605.1.15',
        'Cookie': Cookie}
    image_urls = []
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        results_page = BeautifulSoup(response.content, 'lxml')
        image_text = results_page.find('p').get_text()
        image_text = image_text.replace('\\', '')

        a = json.loads(image_text)['photos']
        base_url = "https://www.elliman.com"

        for i in a:
            if 'http' not in i.get('full'):
                image_urls.append(base_url + i.get('full'))
            else:
                image_urls.append(i.get('full'))

    return image_urls


def all_info(url):
    '''

    :param url: housing url
    :return: all house info
    '''
    house_url_all = []
    house_name_all = []
    image_housing_urls_all = []
    house_price_all = []
    house_extras_all = []
    house_features_all = []
    house_id_all = []
    house_sq_all = []
    house_article = []
    for i in range(1, pages(url) + 1):

        url = f'https://www.elliman.com/search/for-sale/search-{i}?sdid=1&sid=40355790&sk=1'
        house_url_l, house_name, image_housing_urls, house_price, house_extras, house_features, house_id, house_sq = get_house_info(
            url)
        print(len(house_url_l))
        print(f"page{i} is finished")
        article = []
        for i in house_url_l:
            article.append(get_article(i))
        house_article.extend(article)
        house_url_all.extend(house_url_l)
        house_name_all.extend(house_name)
        image_housing_urls_all.extend(image_housing_urls)
        house_price_all.extend(house_price)
        house_extras_all.extend(house_extras)
        house_features_all.extend(house_features)
        house_id_all.extend(house_id)
        house_sq_all.extend(house_sq)

    return list(zip(house_url_all, house_name_all, image_housing_urls_all, house_price_all, house_extras_all,
                    house_features_all, house_id_all, house_sq_all, house_article))


def clean(datafile):
    df = pd.read_csv(datafile,
                     names=['house_index', 'house_url', 'house_address', 'image_url', 'house_price', 'house_extras',
                            'house_features', 'house_id', 'house_sq', 'house_article'])
    df = df[1:]
    df_1 = df.drop(['house_index'], axis=1)

    # process housing_features
    df_1['Beds'] = df_1['house_features'].apply(
        lambda x: 'NaN' if 'Beds' not in str(x) else x.split(' ')[x.split(' ').index('Beds') - 1])
    df_1['Baths'] = df_1['house_features'].apply(
        lambda x: 'NaN' if 'Baths' not in str(x) else x.split(' ')[x.split(' ').index('Baths') - 1])
    df_1['Half Bath'] = df_1['house_features'].apply(
        lambda x: 'NaN' if 'Half' not in str(x) else x.split(' ')[x.split(' ').index('Half') - 1])
    df_1 = df_1.drop(['house_features'], axis=1)

    # processing house_sq
    df_1['Approximate Sq. Feet'] = df_1['house_sq'].apply(
        lambda x: 'NaN' if 'Feet' not in str(x) else x.split(' ')[x.split(' ').index('Feet:') + 1])
    df_1['Approximate Exterior Sq. Ft'] = df_1['house_sq'].apply(
        lambda x: 'NaN' if 'Exterior' not in str(x) else x.split(' ')[x.split(' ').index('Ft:') + 1])
    df_1 = df_1.drop(['house_sq'], axis=1)

    # processing housing address
    df_1['house_address'] = df_1['house_address'].apply(lambda x: str(x).replace('Street', 'St'))
    df_1['house_address_split'] = df_1['house_address'].apply(lambda x: x.split(' - '))
    df_1['house_address1'] = df_1['house_address_split'].apply(lambda x: x[0])
    df_1['house_address2'] = df_1['house_address_split'].apply(lambda x: x[-1])
    df_1['house_address3'] = df_1['house_address1'].apply(lambda x: x.split(',')[-1] if ',' in str(x) else 'NaN')
    df_1['house_address1'] = df_1['house_address1'].apply(lambda x: x.split(',')[:-1] if ',' in str(x) else x)
    df_1.to_csv('manhattan_sale.csv')


if __name__ == '__main__':
    Cookie = #your own cookie

    manhattan_url = 'https://www.elliman.com/search/for-sale/search-1?sdid=1&sid=40355790&sk=1'
    Man_sale = np.array(all_info(manhattan_url), dtype=object)
    df_mansale = pd.DataFrame(Man_sale)
    df_mansale = df_mansale.rename(
        columns={0: 'house_url', 1: 'house_address', 2: 'image_url', 3: 'house_price', 4: 'house_extras',
                 5: 'house_features', 6: 'house_id', 7: 'house_sq', 8: 'house_article'})
    clean(df_mansale)