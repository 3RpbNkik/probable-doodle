from fake_useragent import UserAgent
import os
import re
import csv
import time
import random
import requests

bot_id = 'telegram_bot_id'

def find_all_anonce(string):
    new_list = re.findall('(?<=<a\ class="_109rpto\ _1anrh0x"\ href="/item/detail/)[\w\W]*?(?=/"\ data-item-index=)', string)
    return new_list

def open_page(string):
    referer = ['https://offerup.com/', 'https://www.google.com', 'https://duckduckgo.com/']
    user_agent = random.choice(UserAgent().data_browsers["chrome"])
    headers = {'User-Agent': f'{user_agent}', 'From': f'{random.choice(referer)}'}
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

def write_history_file(new_list):
    with open('history.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_list)

def read_history_file(id):
    with open('history.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        if os.stat('history.csv').st_size == 0:
            return False
        else:
            x = False
            for row in reader:
                if id == row[0]:
                    return True
            return x

def send_photo_and_description(bot_id, image, description):
    url = 'https://api.telegram.org/bot'
    method = '/sendPhoto?chat_id=@offer_autoandparts&photo='
    caption = '&caption='
    requests.get(f'{url}{bot_id}{method}{image}{caption}{description}')

def main():
    new_list = find_all_anonce(open_page("https://offerup.com/explore/k/cars-trucks/"))
    for id in new_list:
        if read_history_file(id) == False:
            item_list = parse_item(open_page(f'https://offerup.com/item/detail/{id}/'))
            href = item_list['href'].pop()
            name = item_list['name'].pop()
            price = item_list['price'].pop()[:-3]
            location = item_list['location'].pop()
            category = item_list['category'].pop()
            image = item_list['image'].pop()
            csv_line = [id, name, price, location, category, href]
            description = f'{name}  ${price}   {location}    {href}'
            write_history_file(csv_line)
            send_photo_and_description(bot_id, image, description)
            time.sleep(1)
    print('Done wait 120s')
    time.sleep(120)
    main()

main()