# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:38:16 2022

@author: LauChein
"""

from flask import Flask
app = Flask(__name__)

import requests
try:
    import xml.etree.cElementTree as et
except:
    import xml.etree.ElementTree as et

@app.route('/weather/<city>')
def weather(city):
    user_key = "CWB-B501A7E8-AB81-4651-A143-8B9CC36067F3"
    doc_name = "F-C0032-001"
    
    cities = ["臺北", "新北", "桃園", "臺中", "台南", "高雄", "新竹", "嘉義", "基隆"]
    countries = ["苗栗", "彰化", "南投", "雲林", "屏東", "宜蘭", "花蓮", "臺東", "澎湖", "金門", "連江"]
    
    show_data = ''
    flagcity = False #檢查是否為縣市名稱
    city = city.replace('台', '臺')
    if city in cities:
        city += '市'
        flagcity = True
    elif city in countries:
        city += '縣'
        flagcity = True
    if flagcity :
        #由中央氣象局api導入
        api_link = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/%s?Authorizationkey=%s&format=XML" %(doc_name, user_key)
        report = requests.get(api_link).text
        #print(report)
        #xml_namespace = "{urn:cwb:gov:tw:cwbcommon:0.1}"
        root = et.fromstring(report)
        
        dataset = root.find('records')
        
        locations_info = dataset.findall('location')
        
        target_idx = -1
        
        for idx, ele in enumerate(locations_info):
            #print(idx, ele[0].text)
            locationName = ele[0].text#取得縣市名
            if locationName == city:
                target_idx = idx
                break
        if target_idx != -1:
            show_data='{'
            tlist = ['天氣狀況', '降雨機率', '最低溫', '舒適度', '最高溫']
            for i in range(5):
                element = locations_info[target_idx][i+1]
                #取得weatherElement
                timeblock = element[1] #取出目前時間點資料
                data = timeblock[2][0].text
                show_data = show_data + '"' + tlist[i] + '":"' + data + '",'
            show_data = show_data[:-1] + '}'
            
    else:
        show_data = '查無此縣市!'
    return show_data
    
if __name__ == '__main__':
    app.run()