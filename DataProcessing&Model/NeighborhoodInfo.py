# Copyright (C) 2019 Chaoyue Zheng. All rights reserved.

'''
To find the neighborhood price level according to restaurant levels and the distance between subway address and house address
'''
import requests


def info(query, api_key):
    query = query.replace(' ', '+')
    response_data = ''
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s' % (query, api_key)
    try:
        response = requests.get(url)
        if not response.status_code == 200:
            print("HTTP error", response.status_code)
        else:
            try:
                response_data = response.json()
            except:
                return ("Response not in valid JSON format")
    except:
        return ("Something went wrong with requests.get")
    results = response_data['results']
    return results


def neighborhood(query, api_key):
    '''
    :param query: housing address
    :param api_key: google api key
    :return: the nearest subway's latitude and longitude
    '''

    query = 'the nearest subway around ' + query
    results = info(query, api_key)
    try:
        return results[0]['geometry']['location']['lat'], results[0]['geometry']['location']['lng']
    except:
        return None


def restaurant(query, api_key=api_key1):
    '''

    :param query: housing address
    :param api_key: google map api key
    :return: to find restaurants' average price level near houses
    '''
    query = 'restaurants around ' + query
    results = info(query, api_key)
    n = len(results)
    if n == 0:
        return None
    else:
        j = n
        price_level = 0
        for i in range(n):
            if not results[i].get('price_level'):
                j -= 1
                if j == 0:
                    return None
            else:
                price_level = price_level + results[i].get('price_level')
        return price_level / j

