import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import datetime
from bs4 import BeautifulSoup
import requests
from random import randrange

headers = [
    {
        'authority': 'www.digikala.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'REDACTED',
    },
    {
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
        'cookie': 'REDACTED',
    }

]
fromPage = 1
toPage = 35
base_url = "https://www.digikala.com/treasure-hunt/products/?pageno={0}&sortby=4"


def getHeaders():
    return headers[randrange(0, 2)]


def main():
    executor = ThreadPoolExecutor(max_workers=20)
    for i in range(fromPage, toPage):
        executor.submit(download_primary_pages, i)

    # time.sleep(60)
    executor.shutdown(wait=True)


def download_primary_pages(i):
    print("Downloading {0}".format(i))
    response = requests.get(base_url.format(i), headers=getHeaders(), timeout=10)
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
    page = requests.get(url, headers=getHeaders(), timeout=10)
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
            requests.get(
                "http://digigaga.gencloud.xyz/public/tg.php?url=Core ({0},{1}) >>> ".format(fromPage, toPage) + url)
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
    img_data = requests.get(url=url, headers=getHeaders()).content
    u = urlparse(url)
    with open(os.path.basename(u.path), 'wb') as handler:
        handler.write(img_data)


if __name__ == "__main__":
    while True:
        requests.get("http://digigaga.gencloud.xyz/public/tg.php?url=Started Core ({0},{1}) >>>> ".format(fromPage,
                                                                                                          toPage) + str(
            datetime.datetime.now()))
        main()
        requests.get("http://digigaga.gencloud.xyz/public/tg.php?url=Finished Core ({0},{1}) >>>> ".format(fromPage,
                                                                                                           toPage) + str(
            datetime.datetime.now()))
