import os
import random
import time
import urllib
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests

headers = {
    'authority': 'www.digikala.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
    'cookie': '_xpid=822544423; _xpkey=feCS6YUWHHgRcCEPYYB7Wwxjb-ER5DLr; _ga=GA1.1.553239188.1600148022; tracker_global=4yQv7xDW; _conv_r=s%3Awww.google.com*m%3Aorganic*t%3A*c%3A; user_location=%7B%22city_id%22%3A1855%2C%22state_id%22%3A12%2C%22city_title%22%3A%22%5Cu0645%5Cu0634%5Cu0647%5Cu062f%22%2C%22state_title%22%3A%22%5Cu062e%5Cu0631%5Cu0627%5Cu0633%5Cu0627%5Cu0646%20%5Cu0631%5Cu0636%5Cu0648%5Cu06cc%22%7D; ins-storage-version=1613; cookiesession1=678B28678990123GHIJKLMNOPQRS121B; _uid_=a31e295f12f34df69a594bd664ca51c2; digikala-user-login=MGlmRC82eEtYM0F2bzRTTjQvN3ZGdz09%26aHhMcHl6RThtaU8yMVllWHg3bkJJaWNPbDJDaFgyUTNmeDA0cVZ6VWZSQjFYdkMvaGtSY2hoZDJvbUQ1Qjh2d0tPSjh5MXZzY0ZtbEJCV1BQYVZvWjZYSVRJQy9jV0plbHk0bDZJR1J4MDc2SmxycG1jYzBscGNhbTl4dE42MlM~; user_search_keywords=%5B%22%5Cu0633%5Cu06cc%5Cu0646%5Cu06cc%20%5Cu0647%5Cu0627%5Cu0631%5Cu062f%22%2C%22%5Cu062f%5Cu0627%5Cu06a9%20%5Cu0647%5Cu0627%5Cu0631%5Cu062f%22%2C%22%5Cu062a%5Cu0628%5Cu062f%5Cu06cc%5Cu0644%20ide%20%5Cu0628%5Cu0647%20sata%22%2C%22%5Cu0647%5Cu062f%5Cu0633%5Cu062a%20%5Cu0648%5Cu0627%5Cu0642%5Cu0639%5Cu06cc%5Cu062a%20%5Cu0645%5Cu062c%5Cu0627%5Cu0632%5Cu06cc%22%2C%22%5Cu0641%5Cu0644%5Cu0634%22%5D; PHPSESSID=hbs4ng47iv17udn2ick187eau77a9ubeo06cpgn83qo0t8e9su6q8g2n1rl2ibqe; sn_tracker_campaign={"u_medium":"Direct","u_source":"Direct","u_campaign":"Direct","u_term":"Direct","u_content":"Direct"}; tracker_session=4EmzDZog; recent_products=%5B5739338%2C3699809%2C1611335%2C2100123%2C4207277%2C6467668%2C4206464%2C4128879%2C4974240%2C2520497%2C1587788%2C322525%2C1150704%2C6619069%2C5070838%5D; TS011a822c=01023105914876daca8efa9fd31e1b77fca82b1cfec913c82c2f5a4dffffe21656a1cd034d226a9a9d8a38f8f014cf7f905d78cce938c5711cfa7b5ed3812f473ac2cf42859a9c276b72205faeeacb6e0cfb728a2010b315f50dab4102357fa41ed0c89fb2b97f96981a2350de90eaea7df0c4524bc9634f35dbba182337c1258de43ec8cdace9d061bec938f38b4e93a9ca1a7848; _conv_v=vi%3A1*sc%3A460*cs%3A1637916560*fs%3A1577092484*pv%3A1814*ps%3A1637914956*exp%3A%7B100023958.%7Bv.1-g.%7B%7D%7D-100024254.%7Bv.1000183223-g.%7B100022024.1-100022025.1%7D%7D-100024729.%7Bv.1-g.%7B%7D%7D-100024870.%7Bv.1-g.%7B%7D%7D-100025140.%7Bv.1-g.%7B%7D%7D%7D; _conv_s=si%3A460*sh%3A1637916560262-0.8521101689455239*pv%3A3; _ga_LR50FG4ELJ=GS1.1.1637914948.83.1.1637916844.26; _ga_4S04WR965Q=GS1.1.1637914948.371.1.1637916844.0',
}
fromPage = 24
toPage = 36
base_url = "https://www.digikala.com/treasure-hunt/products/?pageno={0}&sortby=4"


def main():
    executor = ThreadPoolExecutor(max_workers=10)
    for i in range(fromPage, toPage):
        executor.submit(download_primary_pages, i)

    # time.sleep(60)
    executor.shutdown(wait=True)

def download_primary_pages(i):
    print("Downloading {0}".format(i))
    response = requests.get(base_url.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    if response.status_code != 200:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(i)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    else:
        print("Downloaded {0}".format(i))
        links = soup.find("div", class_="c-listing").find_all("a",
                                                              class_="c-product-box__img c-promotion-box__image js-url js-product-item js-product-url")
        for l in links:
            download_product_page("https://www.digikala.com" + l["href"])

def download_product_page(url):
    # print("Downloading {0} Images".format(url))
    local_images = []
    page = requests.get(url, headers=headers)
    if page.status_code != 200:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(page)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    soup = BeautifulSoup(page.content, 'lxml')
    li = soup.findAll("li", class_="js-product-thumb-img")
    for l in li:
        img = l.find("img")
        local_images.append(img["data-src"])
        print(img["data-src"])
    for i in local_images:
        if "16379" in i:
            print("=>>>>>> EPOCH FOUND <<<<<<<=")
            print("=>>>>>> EPOCH FOUND <<<<<<<=")
            print("=>>>>>> EPOCH FOUND <<<<<<<=")
            print("=>>>>>> EPOCH FOUND <<<<<<<=")
            print("=>>>>>> EPOCH FOUND <<<<<<<=")
            print(i)
            print(url)
            download_image(i)
            requests.get("http://ip/telegram.php?url=" + url)
            print("=>>>>>> EPOCH FOUND <<<<<<<=")
            print("=>>>>>> EPOCH FOUND <<<<<<<=")
            print("=>>>>>> EPOCH FOUND <<<<<<<=")
            print("=>>>>>> EPOCH FOUND <<<<<<<=")
            print("=>>>>>> EPOCH FOUND <<<<<<<=")


def download_image(url):
    print("==============================")
    print("==============================")
    print("==============================")
    print("==============================")
    print("==============================")
    print(url)
    print("==============================")
    print("==============================")
    print("==============================")
    print("==============================")
    print("==============================")
    img_data = requests.get(url=url, headers=headers).content
    u = urlparse(url)
    with open(os.path.basename(u.path), 'wb') as handler:
        handler.write(img_data)


if __name__ == "__main__":
    while True:
        main()
