from bs4 import BeautifulSoup
import requests
import math
import pandas as pd
from datetime import datetime
from datetime import date
now = datetime.now()
today = now.strftime("%d/%m/%Y %H:%M")
csv_file = "data.csv"


def iterate_pages(page):
    req = requests.get(page)
    content = req.content
    soup = BeautifulSoup(content, 'html.parser')

    prices = []
    price = soup.find_all(class_='regular-price')
    for p in price:
        prices.append(p.text.strip().replace('€\xa0', ''))
    # print(prices)
    fietsen = []
    fiets = soup.find_all(class_="product-name")
    for f in fiets:
        fietsen.append(f.text.strip().replace('<h2 class="product-name">', '').replace('\n','').replace('  ',''))
    # print(fietsen)

    urls = soup.find_all("h2")
    url = []
    for h2 in urls:
    #     print(h2.a.text.strip())
    #     print(h2.a['href'])
        try:
            url.append(h2.a['href'])
        except:
            pass


    lst1 = dict(zip(fietsen, zip(prices,url)))
    df = pd.DataFrame(list(lst1.items()), columns=['fiets','price'])
    dfurl = df.price.apply(pd.Series)
    dfurl.columns = ['prices', 'url']
    dfurl
    dff = pd.concat([df, dfurl], axis='columns')
    dff['timestamp'] = today
    dff = dff[['fiets','prices', 'url', 'timestamp']]

    bikes = pd.read_csv(csv_file, index_col=0)
    nbikes = pd.concat([bikes, dff], sort=False)
    nbikes = nbikes.drop_duplicates()
    nbikes = nbikes.reset_index(drop=True)
    nbikes.to_csv(csv_file, sep=',', encoding='utf-8')


base_url = 'https://www.example.com/page-1'
init_page = requests.get(base_url)
init_page = init_page.content
soup = BeautifulSoup(init_page, 'html.parser')


resultaten = soup.find(class_='amount')
total = math.ceil(int(resultaten.text.strip().replace(' resultaten', ''))/24)
# total = int(resultaten.text.strip().replace(' resultaten', ''))
# print(total)

i = 1
while i < total+1:
    page ='https://www.example.com/page-' + str(i)
    iterate_pages(page)
    print(str(i) + ". " + page)
    i += 1
