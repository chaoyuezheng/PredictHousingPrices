# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 12:30:31 2019

@author: Chen Wang
"""
#queens
#bronx
#brooklyn
#new-york
#staten-island
import requests
from bs4 import BeautifulSoup
import math
import json

def NYT_sale(location):
    house_list=list()
    url= "https://www.nytimes.com/real-estate/homes-for-sale/?locations%5B%5D={0}-ny-usa&redirect=find-a-home".format(location)
    response = requests.get(url)
    if not response.status_code == 200:
        return None
    results_page = BeautifulSoup(response.content,'lxml')
    total = results_page.find('div',class_='listings-container')
    total_house=int(total.get("data-listings-total"))
    print('{0} houses avaiable'.format(total_house))
    page=math.ceil(total_house/24)
    for i in range(1,page+1):
        print('Page',i)
        house_page=webcrawler(location,i)
        if house_page==[]:
            return house_list
        house_list.extend(house_page)
    return house_list

def webcrawler(location,p):
    
    house_list=list()
    base="http://www.nytimes.com"
    try:
        url="https://www.nytimes.com/real-estate/homes-for-sale/?locations%5B%5D={0}-ny-usa&sortBy=dateposted-desc&p={1}".format(location,p)
        response = requests.get(url)
        results_page = BeautifulSoup(response.content,'lxml')
        houses = results_page.find_all('article',{'class':'listing-card-large'})
        for house in houses:
            #get url for every house
            house_url=base+house.get('data-url')
            house_response = requests.get(house_url)
            house_results_page = BeautifulSoup(house_response.content,'lxml')
            intro=house_results_page.find('div',class_="about-this-home",id="about-this-home").get_text().strip()
            #get info from table
            table_tag = house_results_page.find('div',class_="listing-section features")
            m=table_tag.find_all('td')
            bedroom=m[3].get_text().strip()
            #maintenance=m[5].get_text().strip()
            bathroom=m[7].get_text().strip()
            #Mon_tax=m[9].get_text().strip()
            room=m[15].get_text().strip()
            size=m[17].get_text().strip()
            Property_Type=m[23].get_text().strip()
            
            try:
                photo=[]
                a=house_results_page.find('div',{'class':'listing-container listing'})
                b=a.find('script',{'type':'application/json'})
                c=json.loads(b.get_text())
                for i in c['imageslideshow'].get('slides',{}):
                    photo.append(i['image_crops'].get('superJumbo',{}).get('url'))
            except:
                photo=[]
            agent=house_results_page.find('div',{'agent-particulars'}).find('a').get_text().strip()
            neighborhood =house.find('p',class_='listing-neighborhood').get_text().strip()
            price = house.find('p',class_='listing-price').get_text().strip()
            address=house.find('p',class_='listing-detail-text listing-address').get_text().strip()
                       
            house_list.append([house_url,neighborhood,price,address,bedroom,bathroom,Property_Type,agent,room,size,intro,photo])
        return house_list
    except:
        return []