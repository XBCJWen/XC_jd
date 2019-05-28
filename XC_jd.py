import csv
import json
import random
import time

import requests
from fake_useragent import UserAgent


class Main(object):
    def __init__(self):
        ua = UserAgent().random
        self.headers = {
            'User-Agent': ua,
        }
        headers=['hotel_total','id','name','sorce','url','lication']
        self.fp=open('XC.csv', 'a', encoding='utf_8_sig', newline='')
        self.fp_csv = csv.DictWriter(self.fp, headers)
        self.fp_csv.writeheader()

    def response_headler(self,url,data):
        response=requests.post(url=url,headers=self.headers,data=data)
        return response

    def parse_hotel_josn(self,data):
        jdata=json.loads(data.text)
        items=[]

        for datas  in jdata.get('hotelPositionJSON'):
            item={}
            item['hotel_total']=jdata.get('hotelAmount')
            item['id']=datas.get('id')
            item['name']= datas.get('name')
            item['sorce']= datas.get('score')
            item['url']= "https://hotels.ctrip.com/hotel" + datas.get('url')
            item['lication']= datas.get('address')
            items.append(item)
        return items



    def sava_data(self,data):
        for datas in data:
            with open('XC.txt','a',encoding='utf-8') as f:
                f.write(json.dumps(datas,ensure_ascii=False))
                f.write('\n')
                f.close()

        for datas in data:
            self.fp_csv.writerow(datas)

        


    def main(self):
        url='https://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
        data={              #所需的参数只要，cityname,cityid,citypy
            'cityName':'%E9%98%B3%E6%B1%9F',
            'cityId': '692',
            'cityPY': 'yangjiang',
            'page': 1
        }
        response=self.response_headler(url,data)
        data=self.parse_hotel_josn(response)
        self.sava_data(data)
        print(data)
        for page in range(1,int(data[0].get('hotel_total')/len(data))+1):
            data = {  # 所需的参数只要，cityname,cityid,citypy
                'cityName': '%E9%98%B3%E6%B1%9F',
                'cityId': '692',
                'cityPY': 'yangjiang',
                'page': page
            }
            item=self.response_headler(url,data)
            data=self.parse_hotel_josn(item)
            print(data)
            self.sava_data(data)
            time.sleep(random.randint(3,10))
        self.fp.close()

if __name__ == '__main__':
    c=Main()
    c.main()
