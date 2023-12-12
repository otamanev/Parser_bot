import requests
import re
import csv

from models import Items


class ParseWB:
    def __init__(self, url: str):
        self.brand_id = self.__get_brand_id(url)

    @staticmethod
    def __get_brand_id(url: str):
        regex = '(?<=catalog/).+(?=/)'
        brand_id = re.search(regex, url)[0]
        return brand_id

    def parse(self):
        self.__create_csv()
        response = requests.get('https://card.wb.ru/cards/v1/list?appType=1&curr=rub&dest=-5923914&spp=27&nm=170430451'
                                ';164400805;168219115;168433833;168334214;168218010;168443536;168669981;168697164;169160874'
                                ';173574395;168924581;176724952;177677917;165508849;168219114;168218008;168334213;168435023'
                                ';168449986;168674354;170430453;173574396;175845425;176167140;176170673;176724951;177677923'
                                ';168334212;168218007;168219113;162943800;168114719;168434546;168443924;168506934;168674521'
                                ';168697162;168834308;169160873;169697197;170430449;171438294;176167139;176170674;170102483'
                                ';176167141;176170672;160652377;170430452;171755139;176076725;176085558;176721622;177024888'
                                ';177677930;177961645;167896308;178708491;178853233;160652378;170430454;171752263;176206245'
                                ';176723465;177677927;167896128;178708494;178853119;165534195;170430456;171746628;176076724'
                                ';176085555;176206243;177558113;177677879;178628597;178708493;176076723;176085553;177024891')

        items_info = Items.model_validate(response.json()['data'])
        self.__get_images(items_info)
        self.__save_csv(items_info)

    def __create_csv(self):
        with open('wb_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'бренд', 'название', 'скидка',  'цена', 'изображение'])

    def __save_csv(self, items):
        with open('wb_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            for product in items.products:
                writer.writerow([product.id,
                                 product.brand,
                                 product.name,
                                 product.salePriceU,
                                 product.priceU,
                                 product.image_links])

    def __get_images(self, item_model: Items):
        for product in item_model.products:
            _shot_id = product.id//100000
            if 0 <= _shot_id <= 143:
                basket = '01'
            elif 144 <= _shot_id <= 287:
                basket = '02'
            elif 288 <= _shot_id <= 431:
                basket = '03'
            elif 432 <= _shot_id <= 719:
                basket = '04'
            elif 720 <= _shot_id <= 1007:
                basket = '05'
            elif 1008 <= _shot_id <= 1061:
                basket = '06'
            elif 1062 <= _shot_id <= 1115:
                basket = '07'
            elif 1116 <= _shot_id <= 1169:
                basket = '08'
            elif 1170 <= _shot_id <= 1313:
                basket = '09'
            elif 1314 <= _shot_id <= 1601:
                basket = '10'
            elif 1602 <= _shot_id <= 1655:
                basket = '11'
            elif 1656 <= _shot_id <= 1919:
                basket = '12'
            else:
                basket = '13'
            url = f'https://basket-{basket}.wb.ru/vol{_shot_id}/part{product.id//1000}/{product.id}/images/big/1.webp'
            res = requests.get(url=url)
            if res.status_code == 200:
                link_str = ''.join([f'https://basket-{basket}.wb.ru/vol{_shot_id}/part{product.id//1000}/{product.id}/images/big/{i}.webp;' for i in range(1, product.pics)])
                product.image_links = link_str
                link_str = ''


if __name__ == '__main__':
    ParseWB('https://www.wildberries.ru/catalog/170430451/detail.aspx').parse()
