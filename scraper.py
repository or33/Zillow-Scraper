import requests
from bs4 import BeautifulSoup
import json
import time
import csv

class ZillowScraper():
    results= []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'cookie': 'zguid=23|%241a329e02-34d4-46ec-a6c2-34b3c370567c; zgsession=1|f3813fb3-7f8e-4001-9d7c-9a07a0046a01; zjs_user_id=null; zjs_anonymous_id=%221a329e02-34d4-46ec-a6c2-34b3c370567c%22; _pxvid=80aa333c-3b12-11eb-bd05-0242ac120007; _gcl_au=1.1.220536021.1607623798; KruxPixel=true; DoubleClickSession=true; _pin_unauth=dWlkPU5HUmpOVEkwWkdVdFl6UTRNaTAwTkRobExUZ3dPV1F0WVRrNVlqQXhZV1ZqWVRBMQ; KruxAddition=true; JSESSIONID=F86A287CCDD1F59101D38443E23F5212; ki_r=aHR0cHM6Ly93d3cuYmluZy5jb20v; G_ENABLED_IDPS=google; ki_s=; ki_t=1607690066882%3B1607690066882%3B1607690209516%3B1%3B7; search=6|1610282225773%7Crect%3D46.38943947655379%252C-68.63991187632276%252C38.96460071144565%252C-82.90016712367726%26disp%3Dmap%26mdm%3Dauto%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%0943%09%09%09%09%09%09; _uetsid=e9e734c03b1211ebb7e2c9a7a1002264; _uetvid=e9e78b103b1211eba22943593a2b4861; AWSALB=6T5cagrMXXIiGp3B3WJq7q9hCgpdPkfrYt7b/iWnNHz5Z5sbtheu6jGKJGCZTVP92CNHuMgN9tE1MZwu8B/fnBZCJWP4L4CqeWXhECvNvRowuM1AOXAU6DOhUROZ; AWSALBCORS=6T5cagrMXXIiGp3B3WJq7q9hCgpdPkfrYt7b/iWnNHz5Z5sbtheu6jGKJGCZTVP92CNHuMgN9tE1MZwu8B/fnBZCJWP4L4CqeWXhECvNvRowuM1AOXAU6DOhUROZ; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_rf=1; _pxff_fp=1; _pxff_bsco=1; _px3=8134ad3d2c6a50d0d24fdaee57f598576e15139070e0e407f6417f105ee17b71:2K72wcX3dkw5kFWP45ANDmvbOIDbnYy8YMZ6wXsYNRqJ3C7ZHZRIHPHoYb7zC9w0BkRXniEtbUs64t2x/eS2qg==:1000:yM6Rt0lXM7bQYWHKTo9ggxQ75ZFn7JqADvruTuxy3d/lwwRFYznx3Sy5pi3K9pz+v10BA7cUMGqzsL2Ny0hcOAL88h7WnIENk3JOuWlp0XhVPrG7g5umGesyEQRCZ8eKGtISYn/EfmmMMLs7RZwpLGnHBFwkfcOa7431uaC2n7I=',
        'referer': 'https://www.zillow.com/captchaPerimeterX/?url=%2fhomes%2ffor_sale%2f%3fsearchQueryState%3d%257B%2522pagination%2522%253A%257B%2522currentPage%2522%253A2%257D%252C%2522usersSearchTerm%2522%253A%2522new%2520york%2522%252C%2522mapBounds%2522%253A%257B%2522west%2522%253A-82.90016712367726%252C%2522east%2522%253A-68.63991187632276%252C%2522south%2522%253A38.96460071144565%252C%2522north%2522%253A46.38943947655379%257D%252C%2522mapZoom%2522%253A7%252C%2522isMapVisible%2522%253Afalse%252C%2522filterState%2522%253A%257B%2522ah%2522%253A%257B%2522value%2522%253Atrue%257D%252C%2522sort%2522%253A%257B%2522value%2522%253A%2522globalrelevanceex%2522%257D%257D%252C%2522isListVisible%2522%253Atrue%257D&uuid=df844260-3bad-11eb-b424-d580bcfbf4f1&vid=80aa333c-3b12-11eb-bd05-0242ac120007',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57'
    }

    def fetch(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        print(response.status_code)
        return response


    def parse(self, response):
        content = BeautifulSoup(response, 'html.parser')
        deck = content.find('ul', {'class': "photo-cards photo-cards_wow photo-cards_short"})
        for card in deck.contents:
            script = card.find('script', {'type': 'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])
                # print(script_json)
                self.results.append({
                'Name': script_json['name'],
                'Floor size in sqft': script_json['floorSize']['value'],
                'Street address': script_json['address']['streetAddress'],
                'Locality': script_json['address']['addressLocality'],
                'Region': script_json['address']['addressRegion'],
                'Postal code': script_json['address']['postalCode'],
                'Price': card.find('div', {'class': 'list-card-price'}).text,
                # 'Latitude': script_json['geo']['latitude'],
                # 'Longitude': script_json['geo']['longitude'],
                'Url': script_json['url'],
                })

        #print(self.results)


    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)




    def run(self):
        url = 'https://www.zillow.com/homes/for_sale/'
        newUrl = 'https://www.zillow.com/ny/'

        for page in range(1, 6):
            params = {
                'searchQueryState': '{"pagination":{"currentPage":%s},"usersSearchTerm":"new york","mapBounds":{"west":-82.90016712367726,"east":-68.63991187632276,"south":38.96460071144565,"north":46.38943947655379},"mapZoom":7,"isMapVisible":false,"filterState":{"ah":{"value":true},"sort":{"value":"globalrelevanceex"}},"isListVisible":true}' %page
            }
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv()





if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()




