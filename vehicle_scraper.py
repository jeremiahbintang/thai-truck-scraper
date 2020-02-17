# -*- coding: utf-8 -*-
# To initialise browser
from selenium import webdriver
# To search using parameters
from selenium.webdriver.common.by import By
# To wait for a page to eload
from selenium.webdriver.support.ui import WebDriverWait
# To spceify what to look when a page is loaded
from selenium.webdriver.support import expected_conditions as EC
# To handle timeout situation
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()

import json
import ast

provinces = ['กรุงเทพมหานคร', 'ระยอง', 'ชลบุรี', 'สมุทรปราการ', 'พระนครศรีอยุธยา']
data = dict()
vehicles = dict()
types = set()

for province in provinces:
    data = {}    
    with open(f'{province}/urls.json', "r") as file:
        urls = json.load(file)
    
    urls = ast.literal_eval(urls)
        
    with open(f"{province}/vehicles.json", "w") as file:
        for index, url in enumerate(urls):
            r = http.request('GET', url)
            soup = BeautifulSoup(r.data, features="lxml")
            
            name = soup.find(id="ContentPlaceHolder1_lblcomp_name2").get_text()
            car_table = soup.find(id="ContentPlaceHolder1_CarTypeTable")
            vehicles = {}
            for tr in car_table.find_all('tr'):
                v_type = ""
                v_count = ""
                for i, td in enumerate(tr.find_all('td')):
                    if i == 0:
                        v_type = td.string
                        types.update(v_type)
                    elif i == 1:
                        count = [int(s) for s in td.string.split() if s.isdigit()]

                        if len(count) > 1:
                            print(url)
                            print(count)
                            raise ValueError("Multiple counts")

                        v_count = count[0]
                    else:
                        print(url)
                        raise ValueError('different format')
                vehicles[v_type] = v_count
            if data.get(name):
                data[f"{name} - {i}"] = vehicles
            else:
                data[name] = vehicles
            print(index+1)

            file.write(json.dumps(data, ensure_ascii=False))
    print(types)

