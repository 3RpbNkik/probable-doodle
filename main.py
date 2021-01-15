import requests
import re
import time
import random

def find_all_anonce(string):
    new_list = re.findall('(?<=<a\ class="_109rpto\ _1anrh0x"\ href="/item/detail/)[\w\W]*?(?=/"\ data-item-index=)', string)
    return new_list

def open_page(string):
    referer = ['https://offerup.com/', 'https://www.google.com', 'https://duckduckgo.com/']
    user_agent = ['User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'
    ]
    headers = {
        'User-Agent': f'{random.choice(user_agent)}',
        'From': f'{random.choice(referer)}'  # This is another valid field
    }
    response = requests.get(string, headers=headers)
    return response.text

def parse_item(string):
    item_href = re.findall('(?<="seo":\{"page":\{"url":")[\w\W]*?(?=/",")', string)
    item_name = re.findall('(?<="product":\{"title":")[\w\W]*?(?=",")', string)
    item_price = re.findall('(?<=\{"price":\{"amount":")[\w\W]*?(?=",")', string)
    item_location = re.findall('(?<="\ data-name="market-info">)[\w\W]*?(?=</a><span\ class=)', string)
    item_category = re.findall('(?<=,"topic":\{"id":")[\w\W]*?(?=","title":")', string)
    item_image = re.findall('(?<="photos":\[\{"images":\{"detail_full":\{"url":")[\w\W]*?(?=","width":)', string)
    pars_list = {"href":item_href, "name":item_name, "price":item_price, "location":item_location, "category":item_category, "image":item_image}
    return pars_list

new_list = find_all_anonce(open_page("https://offerup.com/explore/k/cars-trucks/"))
for id in new_list:
    print(parse_item(open_page(f'https://offerup.com/item/detail/{id}/')))
    time.sleep(2)
